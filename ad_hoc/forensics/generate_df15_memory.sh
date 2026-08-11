#!/bin/bash
# Genera la evidencia real de DF15 (Memoria: Credenciales en RAM): un volcado de memoria física
# GENUINO de una VM Linux mínima DISTINTA a la de DF14 (incidente/servidor independiente, ver
# ad_hoc/forensics/generate_df14_memory.sh), con una sesión bash real cuyo historial en memoria
# revela una contraseña en texto claro -- recuperable con el plugin linux.bash.Bash de verdad.
#
# Reutiliza el kernel Debian y la tabla de símbolos (ISF) ya generados por
# generate_df14_memory.sh (misma build de kernel = mismos símbolos; eso es infraestructura, no
# "la misma evidencia" -- el volcado, el escenario y el proceso plantado son propios de DF15).
# Si generate_df14_memory.sh no se ha ejecutado nunca, ejecútalo primero.
#
# Requiere: docker, la ISF de DF14 ya generada en evidence/forensic/memdump_server01_hacklabs.zip.
# Verificado en vivo el 2026-08-11/12 contra Debian 6.1.0-52-amd64 (bookworm).

set -euo pipefail

WORKDIR="$(mktemp -d)"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUTDIR="$REPO_ROOT/evidence/forensic"
FLAG="HL{cr3d5_l1ng3r_1n_m3m0ry}"

echo "[*] Directorio de trabajo: $WORKDIR"

# --- 1. Reutilizar kernel + ISF de DF14 (misma build, ya generados) -------
if [ ! -f "$OUTDIR/memdump_server01_hacklabs.zip" ]; then
    echo "[!] No se encuentra memdump_server01_hacklabs.zip -- ejecuta antes generate_df14_memory.sh" >&2
    exit 1
fi
unzip -p "$OUTDIR/memdump_server01_hacklabs.zip" "volatility3_symbols_debian-*.json.xz" > /dev/null 2>&1 || true
( cd "$WORKDIR" && unzip -q -o "$OUTDIR/memdump_server01_hacklabs.zip" "volatility3_symbols_debian-*.json.xz" )
ISF="$(ls "$WORKDIR"/volatility3_symbols_debian-*.json.xz)"
echo "[*] Reutilizando símbolos: $(basename "$ISF")"

cat > "$WORKDIR/get_kernel.sh" << 'SCRIPT'
#!/bin/bash
set -e
apt-get update -qq
apt-get install -y -qq linux-image-amd64 >/dev/null 2>&1
KVER=$(ls /boot/vmlinuz-* | head -1 | sed 's|/boot/vmlinuz-||')
cp /boot/vmlinuz-$KVER /work/vmlinuz
echo "$KVER" > /work/kver.txt
SCRIPT
docker run --rm -v "$WORKDIR:/work" -w /work debian:bookworm-slim bash get_kernel.sh
KVER="$(cat "$WORKDIR/kver.txt")"

# --- 2. Binario "sleeper" para los procesos señuelo -------------------------
cat > "$WORKDIR/sleeper.c" << 'EOF'
#include <unistd.h>
#include <sys/prctl.h>
#include <string.h>
#include <stdlib.h>
int main(int argc, char **argv){
    char *n = getenv("FAKE_COMM");
    if (n) {
        char name[16];
        strncpy(name, n, 15);
        name[15] = 0;
        prctl(PR_SET_NAME, name, 0, 0, 0);
    }
    for(;;) pause();
    return 0;
}
EOF

# --- 3. initramfs con bash REAL (busybox ash no vale para linux.bash) -----
# El truco de la FIFO: hay que lanzar el lector (bash) ANTES de abrir el extremo
# de escritura en el proceso principal, o el "exec 3>fifo" bloquea el script
# entero (deadlock clásico de FIFO) antes de que exista ningún lector.
cat > "$WORKDIR/init_template" << EOF
#!/bin/busybox sh
mount -t proc proc /proc
mount -t sysfs sysfs /sys
mount -t devtmpfs devtmpfs /dev

FAKE_COMM="sshd"  exec -a "/usr/sbin/sshd"  /sleeper -D &
FAKE_COMM="cron"   exec -a "/usr/sbin/cron"   /sleeper -f &

mkfifo /fakehist
/bin/bash --norc --noprofile -i < /fakehist > /bashlog 2>&1 &
exec 3>/fakehist
echo 'whoami' >&3
sleep 1
echo 'cd /opt/backups' >&3
sleep 1
echo 'mysqldump -u root -pS3cr3tDBpass2024 -h 10.0.5.20 backup_db > backup.sql' >&3
sleep 1
echo 'ls -la' >&3
sleep 1
echo 'echo "backup ok - ticket ref ${FLAG}"' >&3
sleep 1

echo "=== MINIMAL INIT BOOTED OK ==="
sleep 3600
EOF

cat > "$WORKDIR/build_and_dump.sh" << 'SCRIPT'
#!/bin/bash
set -e
apt-get update -qq
apt-get install -y -qq busybox-static bash-static gcc libc6-dev cpio gzip qemu-system-x86 >/dev/null 2>&1
gcc -static -O2 -o /work/sleeper /work/sleeper.c

mkdir -p /tmp/initrd/{bin,proc,sys,dev,etc}
cp /bin/busybox /tmp/initrd/bin/busybox
cp /bin/bash-static /tmp/initrd/bin/bash
cp /work/sleeper /tmp/initrd/sleeper
cd /tmp/initrd
for cmd in sh cat ls mount poweroff echo sleep tr mkfifo; do ln -sf busybox bin/$cmd; done
cp /work/init_template init
chmod +x init
find . | cpio -o -H newc 2>/dev/null | gzip > /work/initrd.gz

MEM=96
cd /work
rm -f qmp.sock dump.raw
qemu-system-x86_64 \
  -kernel vmlinuz -initrd initrd.gz \
  -append "console=ttyS0 rdinit=/init panic=1" \
  -m ${MEM}M -nographic -no-reboot \
  -serial file:serial.log \
  -qmp unix:qmp.sock,server,nowait &
QPID=$!
sleep 25   # dar tiempo de sobra: bash + FIFO + 5 comandos escalonados (TCG es lento)
python3 - << PYEOF
import socket, json, time
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect("qmp.sock")
def send(cmd):
    s.sendall((json.dumps(cmd)+"\n").encode())
    time.sleep(0.3)
    return s.recv(65536)
send({"execute":"qmp_capabilities"})
send({"execute":"pmemsave","arguments":{"val":0,"size":${MEM}*1024*1024,"filename":"/work/dump.raw"}})
time.sleep(1)
PYEOF
kill $QPID 2>/dev/null || true
wait $QPID 2>/dev/null || true
xz -9e -T0 -c dump.raw > dump.raw.xz
rm -f dump.raw
SCRIPT
docker run --rm -v "$WORKDIR:/work" -w /work debian:bookworm-slim bash build_and_dump.sh

# --- 4. Verificación --------------------------------------------------------
echo "[*] Verificando con Volatility3 real (linux.bash)..."
if ! vol --symbol-dirs "$WORKDIR" -q -f "$WORKDIR/dump.raw.xz" linux.bash 2>&1 | grep -q "$FLAG"; then
    echo "[!] ERROR: la flag no aparece en linux.bash -- revisa el init/timing." >&2
    exit 1
fi
echo "[+] Verificado: linux.bash recupera el historial y la flag."

# --- 5. Empaquetado ----------------------------------------------------------
mv "$WORKDIR/dump.raw.xz" "$WORKDIR/memdump_dbserver01.raw.xz"
( cd "$WORKDIR" && zip -9 -X -q memdump_dbserver01_hacklabs.zip \
    memdump_dbserver01.raw.xz "$(basename "$ISF")" )
cp "$WORKDIR/memdump_dbserver01_hacklabs.zip" "$OUTDIR/"
ls -la "$OUTDIR/memdump_dbserver01_hacklabs.zip"
rm -rf "$WORKDIR"
echo "[+] Listo: $OUTDIR/memdump_dbserver01_hacklabs.zip"
