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

# Run Flask + simulated services (FTP/SSH/SMB threads start in app.py __main__)
exec python /app/app.py
