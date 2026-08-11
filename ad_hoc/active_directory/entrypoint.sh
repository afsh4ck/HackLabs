#!/bin/bash
# ──────────────────────────────────────────────────────────────────
# HackLabs – Domain Controller vulnerable · entrypoint
# Provisiona el dominio la primera vez y arranca Samba en foreground.
# ──────────────────────────────────────────────────────────────────
set -e

MARKER=/var/lib/samba/.hacklabs_provisioned

IP=$(hostname -I 2>/dev/null | awk '{print $1}')
[ -z "$IP" ] && IP=$(hostname -i 2>/dev/null | awk '{print $1}')
export AD_HOST_IP="$IP"

REALM_LOWER=$(echo "$AD_REALM" | tr '[:upper:]' '[:lower:]')
HOST_LOWER=$(echo "$AD_DC_HOSTNAME" | tr '[:upper:]' '[:lower:]')

echo ''
echo '  ╔══════════════════════════════════════════════════════════════╗'
echo '  ║   HackLabs · Vulnerable Active Directory Domain Controller   ║'
echo '  ╚══════════════════════════════════════════════════════════════╝'
echo ''
printf '   Realm    : %s\n' "$AD_REALM"
printf '   NetBIOS  : %s\n' "$AD_DOMAIN"
printf '   DC       : %s.%s\n' "$HOST_LOWER" "$REALM_LOWER"
printf '   IP       : %s\n' "$IP"
echo ''
echo '   [!] Máquina INTENCIONADAMENTE vulnerable. Solo en redes aisladas.'
echo ''

SHARES_MARKER=/srv/shares/public/flag-ad-01.txt

if [ ! -f "$MARKER" ]; then
    echo '  [*] Primer arranque: provisionando el dominio (puede tardar ~1 min)...'
    /provision.sh
    touch "$MARKER"
    echo '  [+] Dominio provisionado.'
elif [ ! -f "$SHARES_MARKER" ]; then
    # El dominio ya está provisionado (/var/lib/samba y /etc/samba
    # persistidos), pero /srv/shares vive en un volumen Docker aparte y
    # está vacío/incompleto — p.ej. porque se recreó el contenedor sin
    # recrear ese volumen a la vez que los otros dos. Autorreparar sin
    # tocar el dominio AD ya existente.
    echo '  [*] Dominio provisionado pero recursos compartidos ausentes: regenerando /srv/shares...'
    /provision.sh --shares-only
else
    echo '  [*] Dominio ya provisionado, reutilizando la base de datos existente.'
fi

# /etc/hosts y resolv.conf apuntando al propio DC (necesario para Kerberos).
# Si la línea ya existe pero con una IP obsoleta (recreación del contenedor
# con nueva IP macvlan), hay que REEMPLAZARLA, no solo comprobar que existe.
if grep -q "${HOST_LOWER}\.${REALM_LOWER}" /etc/hosts 2>/dev/null; then
    sed -i "/${HOST_LOWER}\.${REALM_LOWER}/d" /etc/hosts
fi
printf '%s\t%s.%s %s\n' "$IP" "$HOST_LOWER" "$REALM_LOWER" "$HOST_LOWER" >> /etc/hosts
printf 'search %s\nnameserver 127.0.0.1\n' "$REALM_LOWER" > /etc/resolv.conf 2>/dev/null || true

echo ''
echo '  [+] Servicios expuestos: DNS/53 · Kerberos/88 · LDAP/389 · SMB/445 · kpasswd/464 · LDAPS/636 · GC/3268'
echo "  [+] Añade en tu Kali:  echo '${IP} ${HOST_LOWER}.${REALM_LOWER} ${REALM_LOWER} ${HOST_LOWER}' | sudo tee -a /etc/hosts"
echo ''

# ── Auto-reparación de los registros DNS propios del DC ─────────────
# La IP del contenedor puede cambiar en cada recreación (macvlan) aunque
# el dominio persista en los volúmenes montados. Samba no se re-registra
# solo, así que el apex del dominio (@) y/o el registro de DC01 pueden
# quedar apuntando a una IP muerta — rompiendo bloodhound-python, certipy
# y cualquier herramienta que resuelva el dominio por su propio DNS en
# vez de usar /etc/hosts. Arrancamos Samba en segundo plano, esperamos a
# que su DNS responda, comparamos y corregimos, y luego lo traemos a
# primer plano como PID 1 real (igual que exec, pero después de reparar).
samba --foreground --no-process-group --debuglevel=1 &
SAMBA_PID=$!
trap 'kill -TERM "$SAMBA_PID" 2>/dev/null' TERM INT

for i in $(seq 1 30); do
    samba-tool dns query 127.0.0.1 "$REALM_LOWER" "$HOST_LOWER" A -U "administrator%${AD_ADMIN_PASSWORD}" >/dev/null 2>&1 && break
    sleep 1
done

for name in "$REALM_LOWER" "$HOST_LOWER"; do
    old_ip=$(samba-tool dns query 127.0.0.1 "$REALM_LOWER" "$name" A -U "administrator%${AD_ADMIN_PASSWORD}" 2>/dev/null \
        | awk '/^ *A: /{print $2; exit}')
    if [ -n "$old_ip" ] && [ "$old_ip" != "$IP" ]; then
        echo "  [*] Registro DNS de '$name' obsoleto ($old_ip -> $IP): reparando..."
        samba-tool dns update 127.0.0.1 "$REALM_LOWER" "$name" A "$old_ip" "$IP" -U "administrator%${AD_ADMIN_PASSWORD}" >/dev/null 2>&1 \
            && echo "  [+] Registro DNS de '$name' actualizado." \
            || echo "  [!] No se pudo actualizar el registro DNS de '$name'."
    fi
done

wait "$SAMBA_PID"
