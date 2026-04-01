#!/bin/sh
set -e

echo ''
echo '    __  __              __    __           __         '
echo '   / / / /____ _ _____ / /__ / /   ____ _ / /_   _____'
echo '  / /_/ // __ `// ___// //_// /   / __ `// __ \ / ___/'
echo ' / __  // /_/ // /__ / ,<  / /___/ /_/ // /_/ /(__  ) '
echo '/_/ /_/ \__,_/ \___//_/|_|/_____/\__,_//_.___//____/  '
echo ''
echo '  Intentionally Vulnerable Labs by afsh4ck'
echo '  [!] WARNING: This app is INTENTIONALLY INSECURE. Use only in isolated environments.'
echo ''

# Re-init DB if missing (volume mount may have wiped it)
if [ ! -f /app/hacklabs.db ]; then
    echo '  [*] Initializing database...'
    python /app/init_db.py
fi

# Detect container IP
IP=$(hostname -i 2>/dev/null | awk '{print $1}')

echo '  ╔════════════════════════════════════════════════════════════╗'
printf '  ║  Target machine IP:  http://%-32s║\n' "${IP}"
echo '  ╚════════════════════════════════════════════════════════════╝'
echo ''
echo "  HTTP  →  http://${IP}"
echo "  FTP   →  ${IP}:21"
echo "  SSH   →  ${IP}:22"
echo "  SMB   →  ${IP}:445"
echo ''

# ── SSH service ────────────────────────────────────────────────
echo '  [*] Configurando SSH...'
mkdir -p /var/run/sshd /run/sshd
ssh-keygen -A 2>/dev/null || true
# Allow password auth and high connection volume from hydra
cat >> /etc/ssh/sshd_config << 'SSHEOF'
PasswordAuthentication yes
PermitRootLogin no
UsePAM no
StrictModes no
MaxAuthTries 100
MaxStartups 200:30:400
LoginGraceTime 120
SSHEOF
/usr/sbin/sshd
sleep 1

# ── Samba service ──────────────────────────────────────────────
echo '  [*] Configurando SMB...'
mkdir -p /var/run/samba /var/lib/samba/private /var/log/samba
cat > /etc/samba/smb.conf << 'SMBEOF'
[global]
   workgroup = WORKGROUP
   server string = HackLabs
   security = user
   map to guest = Never
   ntlm auth = ntlmv1-permitted
   lanman auth = no
   disable netbios = yes
   smb ports = 445
   min protocol = NT1
SMBEOF

# ── Create lab users (SSH password + Samba) ────────────────────
echo '  [*] Creando usuarios del laboratorio...'
for entry in "admin:password1" "alice:Password1" "bob:welcome1" "charlie:changeme" "dave:P@ssw0rd"; do
    u=$(echo "$entry" | cut -d: -f1)
    p=$(echo "$entry" | cut -d: -f2-)
    id "$u" >/dev/null 2>&1 || useradd -m -s /bin/bash "$u"
    printf '%s:%s\n' "$u" "$p" | chpasswd
    printf '%s\n%s\n' "$p" "$p" | smbpasswd -s -a "$u" 2>/dev/null || true
done

/usr/sbin/smbd 2>/dev/null &
sleep 1
echo '  [+] SSH y SMB listos.'

# Run Flask + FTP service (SSH/SMB handled by real system services above)
exec python /app/app.py
