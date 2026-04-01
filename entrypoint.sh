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

# ── Samba service con shares ───────────────────────────────────
echo '  [*] Configurando SMB...'
mkdir -p /var/run/samba /var/lib/samba/private /var/log/samba
mkdir -p /srv/smb/hacklabs /srv/smb/admin_backup
printf 'HL{smb_sh4r3_3num3r4ti0n_succ3ss}\n'  > /srv/smb/hacklabs/flag.txt
printf 'HackLabs internal file share.\n'        > /srv/smb/hacklabs/README.txt
printf 'HL{4dm1n_b4ckup_3xf1ltr4ti0n}\n'       > /srv/smb/admin_backup/root.txt
printf 'admin:Summer2019!\n'                    > /srv/smb/admin_backup/passwords.txt
chmod -R 755 /srv/smb/
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

[hacklabs]
   path = /srv/smb/hacklabs
   comment = HackLabs Files
   browseable = yes
   writable = no
   valid users = admin alice bob charlie dave

[admin_backup]
   path = /srv/smb/admin_backup
   comment = Admin Backup (Restricted)
   browseable = yes
   writable = no
   valid users = admin
SMBEOF

# ── FTP service (vsftpd real) ──────────────────────────────────
echo '  [*] Configurando FTP (vsftpd)...'
mkdir -p /var/run/vsftpd/empty
cat > /etc/vsftpd.conf << FTPEOF
listen=YES
listen_ipv6=NO
anonymous_enable=NO
local_enable=YES
write_enable=NO
local_umask=022
dirmessage_enable=YES
connect_from_port_20=YES
chroot_local_user=YES
allow_writeable_chroot=YES
secure_chroot_dir=/var/run/vsftpd/empty
pam_service_name=vsftpd
pasv_enable=YES
pasv_min_port=40000
pasv_max_port=40010
pasv_address=${IP}
user_config_dir=/etc/vsftpd/users
FTPEOF

# ── Crear usuarios del laboratorio ────────────────────────────
echo '  [*] Creando usuarios del laboratorio...'
for entry in "admin:password1" "alice:Password1" "bob:welcome1" "charlie:changeme" "dave:P@ssw0rd"; do
    u=$(echo "$entry" | cut -d: -f1)
    p=$(echo "$entry" | cut -d: -f2-)
    id "$u" >/dev/null 2>&1 || useradd -m -s /bin/bash "$u"
    printf '%s:%s\n' "$u" "$p" | chpasswd
    printf '%s\n%s\n' "$p" "$p" | smbpasswd -s -a "$u" 2>/dev/null || true
done

# ── Hostname ─────────────────────────────────────────────────
hostname hacklabs 2>/dev/null || true
echo 'hacklabs' > /etc/hostname 2>/dev/null || true

# ── Flags en los servicios (una por servicio, separadas) ─────
# SSH flag: solo en el home → visible al conectar por SSH
printf 'HL{ssh_brut3f0rc3_l0gin_succ3ss}\n' > /home/admin/user.txt
chmod 644 /home/admin/user.txt
for u in alice bob charlie dave; do
    printf 'HL{%s_ssh_l0gin_succ3ss}\n' "$u" > /home/${u}/user.txt 2>/dev/null || true
    chmod 644 /home/${u}/user.txt 2>/dev/null || true
done

# FTP flag: en un directorio dedicado → vsftpd hace chroot ahí (no visible por SSH)
mkdir -p /etc/vsftpd/users /home/admin/ftp
printf 'HL{ftp_cr3d3nti4ls_r3us3d}\n' > /home/admin/ftp/ftp_flag.txt
chmod 755 /home/admin/ftp
chmod 644 /home/admin/ftp/ftp_flag.txt
# Configurar vsftpd para que admin aterrice en /home/admin/ftp
printf 'local_root=/home/admin/ftp\n' > /etc/vsftpd/users/admin

# ── Privilege Escalation vulnerabilities (SSH) ─────────────────
echo '  [*] Configurando vectores de escalada de privilegios...'

# Flag de root (objetivo final para todos los vectores)
printf 'HL{r00t_pr1v3sc_succ3ss}\n' > /root/root.txt
chmod 600 /root/root.txt

# --- admin: sudo completo (necesario para verificar permisos en la máquina) ---
mkdir -p /etc/sudoers.d
printf 'admin ALL=(ALL) NOPASSWD: ALL\n' > /etc/sudoers.d/admin
chmod 440 /etc/sudoers.d/admin

# --- bob: sudo misconfiguration → vim (GTFOBins: sudo vim -c ':!/bin/bash') ---
printf 'bob ALL=(ALL) NOPASSWD: /usr/bin/vim\n' > /etc/sudoers.d/bob
chmod 440 /etc/sudoers.d/bob

# --- dave: sudo misconfiguration → find (GTFOBins: sudo find . -exec /bin/bash \; -quit) ---
printf 'dave ALL=(ALL) NOPASSWD: /usr/bin/find\n' > /etc/sudoers.d/dave
chmod 440 /etc/sudoers.d/dave

# --- alice: SUID en python3 (python3 -c 'import os; os.setuid(0); os.system("/bin/bash")') ---
chmod u+s /usr/bin/python3

# --- charlie: script de cron escribible world-writable ejecutado por root cada minuto ---
mkdir -p /opt/scripts
cat > /opt/scripts/cleanup.sh << 'CRONEOF'
#!/bin/bash
# Maintenance cleanup script - runs as root every minute
find /tmp -type f -mmin +60 -delete 2>/dev/null
CRONEOF
chown root:root /opt/scripts/cleanup.sh
chmod 777 /opt/scripts/cleanup.sh
printf '* * * * * root /opt/scripts/cleanup.sh\n' > /etc/cron.d/maintenance
chmod 644 /etc/cron.d/maintenance
# Pista en el home de charlie
printf 'Tip: check what runs automatically on this system...\n' > /home/charlie/note.txt
chmod 644 /home/charlie/note.txt 2>/dev/null || true

# Iniciar cron (necesario para el vector de charlie)
cron 2>/dev/null || true

echo '  [+] Vectores de privesc configurados.'

/usr/sbin/smbd 2>/dev/null &
/usr/sbin/vsftpd &
sleep 1
echo '  [+] FTP, SSH y SMB listos.'

# Run Flask (FTP/SSH/SMB handled by real system services above)
exec python /app/app.py
