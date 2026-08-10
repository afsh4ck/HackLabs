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

if [ ! -f "$MARKER" ]; then
    echo '  [*] Primer arranque: provisionando el dominio (puede tardar ~1 min)...'
    /provision.sh
    touch "$MARKER"
    echo '  [+] Dominio provisionado.'
else
    echo '  [*] Dominio ya provisionado, reutilizando la base de datos existente.'
fi

# /etc/hosts y resolv.conf apuntando al propio DC (necesario para Kerberos)
grep -q "${HOST_LOWER}.${REALM_LOWER}" /etc/hosts 2>/dev/null || \
    printf '%s\t%s.%s %s\n' "$IP" "$HOST_LOWER" "$REALM_LOWER" "$HOST_LOWER" >> /etc/hosts
printf 'search %s\nnameserver 127.0.0.1\n' "$REALM_LOWER" > /etc/resolv.conf 2>/dev/null || true

echo ''
echo '  [+] Servicios expuestos: DNS/53 · Kerberos/88 · LDAP/389 · SMB/445 · kpasswd/464 · LDAPS/636 · GC/3268'
echo "  [+] Añade en tu Kali:  echo '${IP} ${HOST_LOWER}.${REALM_LOWER} ${REALM_LOWER} ${HOST_LOWER}' | sudo tee -a /etc/hosts"
echo ''

exec samba --foreground --no-process-group --debuglevel=1
