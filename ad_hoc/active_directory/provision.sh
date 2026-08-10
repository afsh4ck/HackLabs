#!/bin/bash
# ──────────────────────────────────────────────────────────────────
# HackLabs – Provisión del dominio Active Directory vulnerable
#
# Crea el dominio HACKLABS.LOCAL con 15 debilidades, una por cada
# laboratorio de la categoría "Active Directory".
# Se ejecuta UNA sola vez, en el primer arranque del contenedor.
# ──────────────────────────────────────────────────────────────────
set -e

REALM="${AD_REALM:-HACKLABS.LOCAL}"
DOMAIN="${AD_DOMAIN:-HACKLABS}"
DCHOST="${AD_DC_HOSTNAME:-DC01}"
ADMINPW="${AD_ADMIN_PASSWORD:-Adm1nP@ss2024!}"
FORWARDER="${AD_DNS_FORWARDER:-1.1.1.1}"
IP="${AD_HOST_IP:-127.0.0.1}"

REALM_LOWER=$(echo "$REALM" | tr '[:upper:]' '[:lower:]')
HOST_LOWER=$(echo "$DCHOST" | tr '[:upper:]' '[:lower:]')
FQDN="${HOST_LOWER}.${REALM_LOWER}"
SHARES=/srv/shares

# ── 1. Provisión del dominio ──────────────────────────────────────
echo '  [*] samba-tool domain provision...'
rm -f /etc/samba/smb.conf
samba-tool domain provision \
    --use-rfc2307 \
    --realm="$REALM" \
    --domain="$DOMAIN" \
    --server-role=dc \
    --dns-backend=SAMBA_INTERNAL \
    --host-name="$DCHOST" \
    --host-ip="$IP" \
    --adminpass="$ADMINPW" \
    --option="dns forwarder=$FORWARDER" \
    >/dev/null

ln -sf /var/lib/samba/private/krb5.conf /etc/krb5.conf

# ── 2. Endurecimiento… al revés (configuración insegura a propósito) ──
echo '  [*] Aplicando configuración insegura del servidor...'
python3 - <<'PYEOF'
import re
path = '/etc/samba/smb.conf'
extra = """
	# ── HackLabs: opciones deliberadamente inseguras ──
	ntlm auth = yes
	ldap server require strong auth = no
	map to guest = Bad User
	guest account = nobody
	restrict anonymous = 0
	log level = 0
"""
with open(path) as fh:
    conf = fh.read()
conf = re.sub(r'(?m)^\[global\]\s*$', '[global]\n' + extra.rstrip(), conf, count=1)
with open(path, 'w') as fh:
    fh.write(conf)
PYEOF

# ── 3. Política de contraseñas débil (sin complejidad, sin bloqueo) ──
echo '  [*] Debilitando la política de contraseñas...'
samba-tool domain passwordsettings set \
    --complexity=off --history-length=0 \
    --min-pwd-age=0 --max-pwd-age=0 --min-pwd-length=1 >/dev/null
samba-tool domain passwordsettings set --account-lockout-threshold=0 >/dev/null

# ── 4. Usuarios del dominio ───────────────────────────────────────
echo '  [*] Creando usuarios del dominio...'
mkuser() {  # mkuser <sam> <password> <given> <surname> [description]
    samba-tool user create "$1" "$2" \
        --given-name="$3" --surname="$4" \
        --description="${5:-}" >/dev/null
}

mkuser 'svc.readonly'  'ReadOnly123!'      'Service' 'ReadOnly'   'Cuenta de servicio de solo lectura para inventario'
mkuser 'j.smith'       'Password123'       'John'    'Smith'      'Sales department'
mkuser 'm.wilson'      'Autumn2023!'       'Mary'    'Wilson'     'Marketing department'
mkuser 'p.taylor'      'Chang3M3!'         'Peter'   'Taylor'     'Logistics department'
mkuser 't.rodriguez'   'Welcome2024!'      'Tomas'   'Rodriguez'  'Cuenta temporal'
mkuser 'svc.backup'    'Welcome1'          'Service' 'Backup'     'Backup service account (legacy Kerberos)'
mkuser 'svc.mssql'     'ranger'            'Service' 'MSSQL'      'SQL Server service account'
mkuser 'svc.delegate'  'iloveyou1'         'Service' 'Delegate'   'Front-end web service account'
mkuser 'gpp.deploy'    'GPPstillStandingStrong2k18'   'GPP'     'Deploy'     'Cuenta de despliegue usada por GPO'
mkuser 'h.jones'       'Sup3rS3cur3!2024'  'Helen'   'Jones'      'Helpdesk supervisor'
mkuser 'm.davis'       'Xk9#mQ2$vL8wR3zP'  'Michael' 'Davis'      'Human Resources'
mkuser 'a.miller'      'Rr7$kW1pZ4tB9nGh'  'Anna'    'Miller'     'Finance department'

# La cuenta Guest habilitada permite sesiones nulas / anónimas
samba-tool user enable Guest >/dev/null 2>&1 || true

# ── 5. Grupos y anidamiento (camino de ataque para BloodHound) ────
echo '  [*] Creando grupos y anidamientos...'
for g in 'IT Support' 'Helpdesk' 'TIER0-LEGACY' 'Finance'; do
    samba-tool group add "$g" >/dev/null
done

samba-tool group addmembers 'Helpdesk'      'h.jones'      >/dev/null
samba-tool group addmembers 'TIER0-LEGACY'  'Helpdesk'     >/dev/null
samba-tool group addmembers 'Domain Admins' 'TIER0-LEGACY' >/dev/null
samba-tool group addmembers 'Finance'       'a.miller'     >/dev/null

# ── 6. SPNs (cuentas kerberoasteables) ────────────────────────────
echo '  [*] Registrando SPNs...'
samba-tool spn add "MSSQLSvc/${FQDN}:1433" 'svc.mssql'   >/dev/null
samba-tool spn add "HTTP/web.${REALM_LOWER}" 'svc.delegate' >/dev/null

# ── 7. Ajustes de bajo nivel: UAC, delegación, atributos con flags ──
echo '  [*] Aplicando atributos vulnerables (UAC, delegación, descripciones)...'
eval "$(python3 /seed_domain.py)"

# ── 7b. MachineAccountQuota utilizable: delega creación de equipos ────
# Por defecto ms-DS-MachineAccountQuota=10, pero el ACL por defecto de
# Samba en CN=Computers es más estricto que el de un AD real de Windows.
# Se concede CreateChild(computer) a "Authenticated Users" para que la
# cuota tenga efecto real (delegación habitual en dominios de producción).
samba-tool dsacl set \
    --objectdn="CN=Computers,${DN_BASE}" \
    --sddl="(OA;;CC;bf967a86-0de6-11d0-a285-00aa003049e2;;AU)" >/dev/null

# ── 8. ACLs abusables sobre objetos del directorio ────────────────
echo '  [*] Delegando ACLs inseguras...'

# svc.readonly → GenericAll sobre m.davis (permite resetear su contraseña)
samba-tool dsacl set \
    --objectdn="${DN_M_DAVIS}" \
    --sddl="(A;;GA;;;${SID_SVC_READONLY})" >/dev/null

# svc.readonly → WriteProperty sobre el atributo 'member' de "IT Support"
samba-tool dsacl set \
    --objectdn="${DN_IT_SUPPORT}" \
    --sddl="(OA;;WP;bf9679c0-0de6-11d0-a285-00aa003049e2;;${SID_SVC_READONLY})" >/dev/null

# "IT Support" → derechos de replicación (DCSync) sobre el dominio
samba-tool dsacl set \
    --objectdn="${DN_BASE}" \
    --sddl="(OA;;CR;1131f6aa-9c07-11d1-f79f-00c04fc2dcd2;;${SID_IT_SUPPORT})(OA;;CR;1131f6ad-9c07-11d1-f79f-00c04fc2dcd2;;${SID_IT_SUPPORT})(OA;;CR;89e95b76-444d-4c62-991a-0facbeda640c;;${SID_IT_SUPPORT})" \
    >/dev/null

# ── 9. Recursos compartidos con las flags ─────────────────────────
echo '  [*] Publicando recursos compartidos y flags...'
mkdir -p "$SHARES"/{public,jsmith,backup,sqldata,deploy,hr_private,it_share,secrets,finance,silver,vault,deleg,computers}

cat > "$SHARES/public/flag-ad-01.txt" <<'EOF'
================================================================
  HACKLABS.LOCAL – Recurso público del departamento de IT
================================================================

Este recurso está accesible sin autenticación (sesión nula).
Nunca publiques credenciales en un share anónimo.

  Flag: HL{4d_5mb_nu11_53ss10n_3num3r473d}
EOF

cat > "$SHARES/public/IT_Onboarding.txt" <<'EOF'
Guía rápida de alta de equipos – Departamento de IT
---------------------------------------------------

Para inventariar un equipo nuevo, usa la cuenta de servicio de
solo lectura contra el LDAP del dominio:

    Usuario : svc.readonly
    Password: ReadOnly123!

Recuerda: esta cuenta NO debe usarse para tareas administrativas.
EOF

# ── Artefactos de "tráfico capturado" para AS-REP Roasting / Kerberoasting ──
# El KDC embebido de Samba no siempre completa en vivo el intercambio de
# preautenticación/TGS-REQ que estas técnicas necesitan (limitación conocida
# de Samba AD DC frente a Windows real). Estos hashes son artefactos VÁLIDOS
# y CRACKEABLES generados offline con las mismas primitivas criptográficas de
# Kerberos (RC4/etype23), verificados con hashcat -m 18200 / -m 13100, para
# que el ejercicio de cracking sea idéntico al de una red real.
cat > "$SHARES/public/captured_asrep.txt" <<'EOF'
# Traza de red capturada por el SOC (AS-REQ/AS-REP de svc.backup)
# Cuenta con "Do not require Kerberos preauthentication" activado.
$krb5asrep$23$svc.backup@HACKLABS.LOCAL:2b94fe92594d9a5c6e5e5738ca3aa9ad$92651af9ca4d25bf8a4305f38f6e53c84298ee902834dd314c6b054b6696755697e276107c542ce6f6855e4f2053409feaf732cad7b8697eb6cf601ec93c9acca7eaa3cc443fc30165f4bc54ab4a2e6bce174c578ae7c3fae3093d94ef77346c98f21628fb07759e55705e452c9091be94ed8f0e8fd696bde324deadfdc0743763399e1755337834bd64ceb9de64b31a0698217b0ead6f9769d7a98c29c67a6523e7fdf083a24a2109ddac8a8eb651126f49de4ad686a52d9c248bfec778f305d59ebb2862365c9d509670bc2457c329c52094320d9108ed700ec8de6202ab7eb37b82550e757be40dba881d887f1ed8
EOF

cat > "$SHARES/public/captured_tgs.txt" <<'EOF'
# Traza de red capturada por el SOC (TGS-REQ/TGS-REP para MSSQLSvc)
# svc.mssql tiene un SPN registrado: cualquier usuario autenticado
# puede solicitar este ticket de servicio.
$krb5tgs$23$*svc.readonly$HACKLABS.LOCAL$MSSQLSvc/dc01.hacklabs.local:1433*$f6341fbbc403555372cce9ae23d4fd1b$7d37d3e6d563844933f03e652805c4f22e46161694680a1dd4bfc2a6d30b119f727d9e14c93d2042f108dbae7870efeb462aefd7d22f3c5d41c4e668c400efda487e77a4eea1f1956a01631fe5ea55ab0a9418832399f20c4a7306cbfb6cf2e90ff275a2598fee6aee29388e0a1173045cc8a069928d588cded4deac1a80bd649cfa24bd0caaf7f3883e1186ff14c0f9daadee1fd6bcd785873b8a04707db818d7e8c0c51f5f70101d778f2ab76fb495a467bea8b80d9fa8e01c
EOF

# Script de verificación local para las tickets forjadas de los labs 12/13
# (Silver Ticket / Golden Ticket). Se publica junto al resto de artefactos
# para que sea descargable desde el mismo recurso anónimo.
cp /verify_ticket.py "$SHARES/public/verify_ticket.py"

printf 'HL{4d_p455w0rd_5pr4y_5ucc355}\n'          > "$SHARES/jsmith/flag-ad-03.txt"
printf 'HL{4d_45r3p_r0457_cr4ck3d}\n'             > "$SHARES/backup/flag-ad-04.txt"
printf 'HL{4d_k3rb3r0457_5pn_cr4ck3d}\n'          > "$SHARES/sqldata/flag-ad-05.txt"
printf 'HL{4d_9pp_cp455w0rd_d3crypt3d}\n'         > "$SHARES/deploy/flag-ad-06.txt"
printf 'HL{4d_93n3r1c411_p455w0rd_r3537}\n'       > "$SHARES/hr_private/flag-ad-08.txt"
printf 'HL{4d_4dd53lf_pr1v1l3g3d_9r0up}\n'        > "$SHARES/it_share/flag-ad-09.txt"
printf 'HL{4d_dc5ync_n7d5_dump3d}\n'              > "$SHARES/secrets/flag-ad-10.txt"
printf 'HL{4d_p455_7h3_h45h_l473r41}\n'           > "$SHARES/finance/flag-ad-11.txt"
printf 'HL{4d_51lv3r_71ck37_f0r93d}\n'            > "$SHARES/silver/flag-ad-12.txt"
printf 'HL{4d_90ld3n_71ck37_d0m41n_0wn3d}\n'      > "$SHARES/vault/flag-ad-13.txt"
printf 'HL{4d_c0n57r41n3d_d3l394710n_4bu53d}\n'   > "$SHARES/deleg/flag-ad-14.txt"
printf 'HL{4d_m4ch1n3_4cc0un7_qu074_4bu53d}\n'    > "$SHARES/computers/flag-ad-15.txt"

# ── Volcado NTDS real para el lab de DCSync (AD10) ────────────────────
# Los clientes DCSync actuales (impacket-secretsdump, pypykatz) tienen
# incompatibilidades conocidas con la implementación DRSUAPI de Samba y
# no completan la replicación en vivo. Este fichero representa el
# resultado de una replicación DCSync exitosa: se genera leyendo los
# hashes REALES del dominio (samba-tool, acceso local del propio DC) y
# solo es legible por miembros de "IT Support" — el mismo grupo al que
# el ACL de DS-Replication-Get-Changes está delegado.
get_nt_hash() {  # get_nt_hash <sAMAccountName>
    samba-tool user getpassword "$1" --attributes=unicodePwd 2>/dev/null \
        | awk -F': ' '/^unicodePwd/{print $2}' \
        | python3 -c 'import sys,base64; print(base64.b64decode(sys.stdin.read().strip()).hex())'
}

ADMIN_NT=$(get_nt_hash Administrator)
KRBTGT_NT=$(get_nt_hash krbtgt)
DC_NT=$(get_nt_hash "${DCHOST}\$")
AMILLER_NT=$(get_nt_hash a.miller)
# El SID del dominio es el SID de Administrator sin su RID final (-500)
ADMIN_SID=$(samba-tool user show Administrator --attributes=objectSid 2>/dev/null \
    | awk -F': ' '/^objectSid/{print $2}')
DOMAIN_SID=${ADMIN_SID%-*}

cat > "$SHARES/secrets/ntds_dump.txt" <<EOF2
================================================================
  HACKLABS.LOCAL – Volcado NTDS (DCSync)
================================================================
Formato: dominio\\usuario:rid:LM:NT:::

  Nota: los clientes DCSync habituales (impacket-secretsdump con
  -just-dc, pypykatz smb dcsync) tienen incompatibilidades
  conocidas con la implementación DRSUAPI de Samba y no completan
  la replicación en vivo contra este laboratorio. Este fichero
  representa el resultado que obtendrías con una replicación
  DCSync exitosa (los mismos comandos SÍ funcionan contra un
  Domain Controller Windows real).

  Comando real que ejecutarías:
    impacket-secretsdump '${REALM_LOWER}/svc.readonly:ReadOnly123!'@${FQDN} -just-dc

HACKLABS\\Administrator:500:aad3b435b51404eeaad3b435b51404ee:${ADMIN_NT}:::
HACKLABS\\krbtgt:502:aad3b435b51404eeaad3b435b51404ee:${KRBTGT_NT}:::
HACKLABS\\a.miller:1108:aad3b435b51404eeaad3b435b51404ee:${AMILLER_NT}:::
HACKLABS\\${DCHOST}\$:1000:aad3b435b51404eeaad3b435b51404ee:${DC_NT}:::

  SID del dominio: ${DOMAIN_SID}

  Flag: HL{4d_dc5ync_n7d5_dump3d}
EOF2

cat > "$SHARES/secrets/nota_admin.txt" <<'EOF'
Recordatorio del administrador
------------------------------
El volcado de NTDS incluye el hash de a.miller (departamento
financiero). Ese hash abre el recurso \\DC01\finance sin conocer
la contraseña en claro.

El hash de krbtgt permite forjar Golden Tickets (control total del
dominio). El hash de la cuenta de máquina DC01$ permite forjar
Silver Tickets para los servicios que corren en este equipo.
EOF

chown -R root:root "$SHARES"
find "$SHARES" -type d -exec chmod 0755 {} +
find "$SHARES" -type f -exec chmod 0644 {} +

cat >> /etc/samba/smb.conf <<EOF

# ──────────────────────────────────────────────────────────────
#  HackLabs – Recursos compartidos de los laboratorios
# ──────────────────────────────────────────────────────────────
[public]
	path = $SHARES/public
	comment = Public IT resources (anonymous)
	read only = yes
	browseable = yes
	guest ok = yes

[jsmith]
	path = $SHARES/jsmith
	comment = Home directory - John Smith
	read only = yes
	browseable = yes
	valid users = j.smith

[backup]
	path = $SHARES/backup
	comment = Backup service repository
	read only = yes
	browseable = yes
	valid users = svc.backup

[sqldata]
	path = $SHARES/sqldata
	comment = SQL Server data export
	read only = yes
	browseable = yes
	valid users = svc.mssql

[deploy]
	path = $SHARES/deploy
	comment = Software deployment share
	read only = yes
	browseable = yes
	valid users = gpp.deploy

[hr_private]
	path = $SHARES/hr_private
	comment = Human Resources (private)
	read only = yes
	browseable = yes
	valid users = m.davis

[it_share]
	path = $SHARES/it_share
	comment = IT Support team share
	read only = yes
	browseable = yes
	valid users = @"$DOMAIN\\IT Support"

[secrets]
	path = $SHARES/secrets
	comment = Domain administration secrets
	read only = yes
	browseable = yes
	valid users = @"$DOMAIN\\IT Support"

[finance]
	path = $SHARES/finance
	comment = Finance department
	read only = yes
	browseable = yes
	valid users = @"$DOMAIN\\Finance"

[silver]
	path = $SHARES/silver
	comment = Restricted CIFS service data
	read only = yes
	browseable = yes
	valid users = @"$DOMAIN\\Domain Admins"

[vault]
	path = $SHARES/vault
	comment = Domain vault
	read only = yes
	browseable = yes
	valid users = @"$DOMAIN\\Domain Admins"

[deleg]
	path = $SHARES/deleg
	comment = Delegated front-end data
	read only = yes
	browseable = yes
	valid users = @"$DOMAIN\\Domain Admins" svc.delegate

[computers]
	path = $SHARES/computers
	comment = Machine provisioning share
	read only = yes
	browseable = yes
	valid users = @"$DOMAIN\\Domain Computers"
EOF

# ── 10. GPO con cpassword en SYSVOL (MS14-025) ────────────────────
echo '  [*] Plantando GPP cpassword en SYSVOL...'
GPO_GUID='{A2B3C4D5-1E6F-4A7B-8C9D-0E1F2A3B4C5D}'
GPO_DIR="/var/lib/samba/sysvol/${REALM_LOWER}/Policies/${GPO_GUID}"
mkdir -p "${GPO_DIR}/Machine/Preferences/Groups"

cat > "${GPO_DIR}/GPT.INI" <<'EOF'
[General]
Version=4
displayName=Deploy Local Admin
EOF

cat > "${GPO_DIR}/Machine/Preferences/Groups/Groups.xml" <<'EOF'
<?xml version="1.0" encoding="utf-8"?>
<Groups clsid="{3125E937-EB16-4b4c-9934-544FC6D24D26}">
  <User clsid="{DF5F1855-51E5-4d24-8B1A-D9BDE98BA1D1}"
        name="gpp.deploy"
        image="2"
        changed="2023-11-04 09:12:31"
        uid="{9A2B3C4D-5E6F-4071-8293-A4B5C6D7E8F9}">
    <Properties action="U"
                newName=""
                fullName="Deployment account"
                description="Cuenta usada por la GPO de despliegue"
                cpassword="edBSHOwhZLTjt/QS9FeIcJ83mjWA98gw9guKOhJOdcqh+ZGMeXOsQbCpZ3xUjTLfCuNH8pG5aSVYdYw/NglVmQ"
                changeLogon="0"
                noChange="1"
                neverExpires="1"
                acctDisabled="0"
                userName="gpp.deploy"/>
  </User>
</Groups>
EOF

chmod -R 0755 "$GPO_DIR"

echo '  [+] Provisión completada.'
