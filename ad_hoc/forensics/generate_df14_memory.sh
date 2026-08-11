#!/bin/bash
# Genera la evidencia real de DF14 (Memoria: Proceso Malicioso): un volcado de memoria física
# GENUINO de una VM Linux mínima, analizable con Volatility3 de verdad (linux.pslist/psaux, etc.),
# junto con la tabla de símbolos (ISF) que Volatility3 necesita para esa build exacta del kernel.
#
# A diferencia de generate_evidence.py (instantáneo, determinista, sin dependencias pesadas),
# este script es lento (~5-10 min) y necesita Docker + conexión a internet, porque:
#   1. Descarga un kernel Debian estándar + su paquete de símbolos de depuración (~850MB, vía apt).
#   2. Compila dwarf2json (Go) y genera la ISF a partir del vmlinux con DWARF real.
#   3. Arranca ese kernel en QEMU (emulación por software, sin KVM) con un init minimalista
#      que planta procesos señuelo + un proceso malicioso disfrazado de hilo de kernel.
#   4. Vuelca la memoria física con pmemsave y la comprime.
#
# El resultado (memdump_server01.raw.xz + volatility3_symbols_debian-<kver>.json.xz, empaquetados
# en memdump_server01_hacklabs.zip) se commitea a evidence/forensic/ como asset estático -- este
# script NO se ejecuta en runtime ni en cada arranque del contenedor, solo cuando se quiere
# regenerar la evidencia desde cero (p.ej. si se quiere cambiar el proceso malicioso plantado).
#
# Requiere: docker (el usuario debe estar en el grupo docker), go (para compilar dwarf2json).
# Verificado en vivo el 2026-08-11/12 contra Debian 6.1.0-52-amd64 (bookworm).

set -euo pipefail

WORKDIR="$(mktemp -d)"
OUTDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../evidence/forensic" && pwd)"
FLAG="HL{m4l1c10u5_pr0c355_1n_r4m}"

echo "[*] Directorio de trabajo: $WORKDIR"
echo "[*] Salida final en: $OUTDIR"

# --- 1. dwarf2json ---------------------------------------------------------
echo "[*] Compilando dwarf2json..."
git clone --depth 1 https://github.com/volatilityfoundation/dwarf2json.git "$WORKDIR/dwarf2json" -q
( cd "$WORKDIR/dwarf2json" && go build )

# --- 2. Kernel estándar + símbolos de depuración (dentro de un contenedor) -
cat > "$WORKDIR/get_kernel.sh" << 'SCRIPT'
#!/bin/bash
set -e
apt-get update -qq
apt-get install -y -qq busybox-static gcc libc6-dev cpio gzip xz-utils linux-image-amd64 >/dev/null 2>&1
KVER=$(ls /boot/vmlinuz-* | head -1 | sed 's|/boot/vmlinuz-||')
echo "$KVER" > /work/kver.txt
cp /boot/vmlinuz-$KVER /work/vmlinuz

echo "deb http://deb.debian.org/debian-debug bookworm-debug main" >> /etc/apt/sources.list
apt-get update -qq
apt-get install -y -qq --download-only linux-image-${KVER}-dbg 2>&1 | tail -3
DEB=$(find /var/cache/apt/archives -name "linux-image-${KVER}-dbg*.deb")
dpkg-deb --fsys-tarfile "$DEB" | tar -x -f - -O "./usr/lib/debug/boot/vmlinux-${KVER}" > /work/vmlinux_dbg
echo "[*] vmlinux con DWARF: $(du -h /work/vmlinux_dbg)"
SCRIPT
docker run --rm -v "$WORKDIR:/work" -w /work debian:bookworm-slim bash get_kernel.sh
KVER="$(cat "$WORKDIR/kver.txt")"
echo "[*] Kernel objetivo: $KVER"

echo "[*] Generando ISF con dwarf2json (puede tardar 1-2 min)..."
"$WORKDIR/dwarf2json/dwarf2json" linux --elf "$WORKDIR/vmlinux_dbg" > "$WORKDIR/linux_isf.json"
rm -f "$WORKDIR/vmlinux_dbg"   # ya no se necesita, y pesa ~600MB
xz -9 -c "$WORKDIR/linux_isf.json" > "$WORKDIR/volatility3_symbols_debian-${KVER}.json.xz"
echo "[*] ISF comprimida: $(du -h "$WORKDIR/volatility3_symbols_debian-${KVER}.json.xz")"

# --- 3. Binario "sleeper" (permite fijar comm/argv0 vía prctl) -------------
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

# --- 4. initramfs minimalista con los procesos señuelo + el malicioso -----
cat > "$WORKDIR/init_template" << EOF
#!/bin/busybox sh
mount -t proc proc /proc
mount -t sysfs sysfs /sys

FAKE_COMM="sshd"            exec -a "/usr/sbin/sshd"                 /sleeper -D &
FAKE_COMM="cron"             exec -a "/usr/sbin/cron"                 /sleeper -f &
FAKE_COMM="rsyslogd"         exec -a "/usr/sbin/rsyslogd"             /sleeper -n &
FAKE_COMM="systemd-journal"  exec -a "/lib/systemd/systemd-journald"  /sleeper &
FAKE_COMM="kworker/u4:2"     exec -a "/dev/shm/.systemd/kworker"      /sleeper --connect 185.220.101.47:443 --beacon 60 --id ${FLAG} &

echo "=== MINIMAL INIT BOOTED OK ==="
sleep 3600
EOF

cat > "$WORKDIR/build_initrd.sh" << 'SCRIPT'
#!/bin/bash
set -e
apt-get update -qq
apt-get install -y -qq busybox-static gcc libc6-dev cpio gzip qemu-system-x86 >/dev/null 2>&1
gcc -static -O2 -o /work/sleeper /work/sleeper.c

mkdir -p /tmp/initrd/{bin,proc,sys,dev,etc}
cp /bin/busybox /tmp/initrd/bin/busybox
cp /work/sleeper /tmp/initrd/sleeper
cd /tmp/initrd
for cmd in sh cat ls mount poweroff echo sleep tr; do ln -sf busybox bin/$cmd; done
cp /work/init_template init
chmod +x init
find . | cpio -o -H newc 2>/dev/null | gzip > /work/initrd.gz

# --- 5. Arranque en QEMU (TCG, sin KVM) + volcado de memoria física -------
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
sleep 20   # dar tiempo de sobra a que el init termine de plantar los procesos (TCG es lento)
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
ls -la dump.raw.xz
SCRIPT
docker run --rm -v "$WORKDIR:/work" -w /work debian:bookworm-slim bash build_initrd.sh

# --- 6. Verificación (falla el script si Volatility3 no encuentra al proceso) --
echo "[*] Verificando con Volatility3 real..."
if ! vol --symbol-dirs "$WORKDIR" -q -f "$WORKDIR/dump.raw.xz" linux.psaux 2>&1 | grep -q "$FLAG"; then
    echo "[!] ERROR: la flag no aparece en linux.psaux -- revisa el init/timing." >&2
    exit 1
fi
echo "[+] Verificado: linux.pslist/psaux encuentran el proceso malicioso y la flag."

# --- 7. Empaquetado final ---------------------------------------------------
mv "$WORKDIR/dump.raw.xz" "$WORKDIR/memdump_server01.raw.xz"
( cd "$WORKDIR" && zip -9 -X -q memdump_server01_hacklabs.zip \
    memdump_server01.raw.xz "volatility3_symbols_debian-${KVER}.json.xz" )
cp "$WORKDIR/memdump_server01_hacklabs.zip" "$OUTDIR/"
ls -la "$OUTDIR/memdump_server01_hacklabs.zip"
rm -rf "$WORKDIR"
echo "[+] Listo: $OUTDIR/memdump_server01_hacklabs.zip"
