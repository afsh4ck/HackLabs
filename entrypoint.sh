#!/bin/sh
set -e

# ── Detect container IP ──
IP=$(hostname -i 2>/dev/null | awk '{print $1}')

echo ""
echo "  ██╗  ██╗ █████╗  ██████╗██╗  ██╗██╗      █████╗ ██████╗ ███████╗"
echo "  ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██║     ██╔══██╗██╔══██╗██╔════╝"
echo "  ███████║███████║██║     █████╔╝ ██║     ███████║██████╔╝███████╗"
echo "  ██╔══██║██╔══██║██║     ██╔═██╗ ██║     ██╔══██║██╔══██╗╚════██║"
echo "  ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║██████╔╝███████║"
echo "  ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝"
echo ""
echo "  [*] HackLabs – Intentionally Vulnerable Labs by afsh4ck"
echo "  [!] WARNING: This app is INTENTIONALLY INSECURE. Use only in isolated environments."
echo ""
echo "  ╔══════════════════════════════════════════════════════════════╗"
echo "  ║  Target machine IP:  http://${IP}                          ║"
echo "  ╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "  HTTP  →  http://${IP}  (port 80)"
echo "  FTP   →  ${IP}:21"
echo "  SSH   →  ${IP}:22"
echo "  SMB   →  ${IP}:445"
echo ""

# Re-init DB if missing (volume mount may have wiped it)
if [ ! -f /app/hacklabs.db ]; then
    echo "  [*] Initializing database..."
    python /app/init_db.py
fi

# Run Flask on port 80 via gunicorn
exec gunicorn --bind 0.0.0.0:80 --workers 2 --threads 4 --access-logfile - app:app
