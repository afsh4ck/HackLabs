#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────
# HackLabs – Despliegue Docker al estilo DockerLabs
# Uso: sudo bash deploy.sh
# ─────────────────────────────────────────────────────────────────

# ── Colores ──
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; DIM='\033[2m'; NC='\033[0m'

CONTAINER_NAME="hacklabs"
IMAGE_NAME="hacklabs:latest"
NET_NAME="hacklabs_net"
SHIM="macvlan0"

# ── Banner ──
clear
echo ""
printf "${RED}%s${NC}\n" '    __  __              __    __           __         '
printf "${RED}%s${NC}\n" '   / / / /____ _ _____ / /__ / /   ____ _ / /_   _____'
printf "${RED}%s${NC}\n" '  / /_/ // __ `// ___// //_// /   / __ `// __ \ / ___/'
printf "${RED}%s${NC}\n" ' / __  // /_/ // /__ / ,<  / /___/ /_/ // /_/ /(__  ) '
printf "${RED}%s${NC}\n" '/_/ /_/ \__,_/ \___//_/|_|/_____/\__,_//_.___//____/  '
echo ""
printf "  ${DIM}%s${NC}\n" 'Intentionally Vulnerable Labs · by afsh4ck'
printf "  ${RED}%s${NC}\n" '[!] ADVERTENCIA: Solo usar en entornos aislados y controlados'
echo ""

# ── Verificar root ──
[[ $EUID -ne 0 ]] && {
    printf "${RED}[✗] Ejecuta con privilegios root: sudo bash deploy.sh${NC}\n"
    exit 1
}

# ── Verificar Docker ──
command -v docker &>/dev/null || { printf "${RED}[✗] Docker no encontrado. Instálalo primero.${NC}\n"; exit 1; }
docker info &>/dev/null       || { printf "${RED}[✗] El servicio Docker no está activo.${NC}\n"; exit 1; }

log()  { printf "${GREEN}[+]${NC} %s\n" "$1"; }
warn() { printf "${YELLOW}[!]${NC} %s\n" "$1"; }
err()  { printf "${RED}[✗] %s${NC}\n" "$1"; exit 1; }

# ── Detectar interfaz de red ──
IFACE="eth0"
if ! ip link show "$IFACE" &>/dev/null; then
    IFACE=$(ip route | awk '/default/{print $5; exit}')
    [[ -z "$IFACE" ]] && err "No se detectó ninguna interfaz de red activa."
    warn "eth0 no disponible — usando $IFACE"
fi

SUBNET=$(ip -4 addr show "$IFACE" | grep -oP '(?<=inet\s)\d+\.\d+\.\d+\.\d+/\d+' | head -1)
[[ -z "$SUBNET" ]] && err "No se pudo detectar la subred de $IFACE."

GATEWAY=$(ip route | awk "/default.*$IFACE/{print \$3; exit}")
[[ -z "$GATEWAY" ]] && GATEWAY=$(ip route | awk '/default/{print $3; exit}')
[[ -z "$GATEWAY" ]] && err "No se pudo detectar la puerta de enlace."

NET_BASE=$(echo "$SUBNET" | grep -oP '^\d+\.\d+\.\d+')
log "Red detectada: $SUBNET en $IFACE (gateway $GATEWAY)"

# ── Seleccionar IP libre en rango .100–.199 ──
CONTAINER_IP=""
while read -r OCTET; do
    CANDIDATE="${NET_BASE}.${OCTET}"
    ping -c1 -W1 "$CANDIDATE" &>/dev/null 2>&1 || { CONTAINER_IP="$CANDIDATE"; break; }
done < <(shuf -i 100-199)
[[ -z "$CONTAINER_IP" ]] && err "No se encontró ninguna IP libre en ${NET_BASE}.100-199."
log "IP asignada al laboratorio: ${BOLD}${CONTAINER_IP}${NC}"

# ── Limpiar instancias previas ──
warn "Limpiando instancias previas si existen..."
docker stop  "$CONTAINER_NAME" &>/dev/null || true
docker rm    "$CONTAINER_NAME" &>/dev/null || true
docker network rm "$NET_NAME"  &>/dev/null || true
ip link del  "$SHIM"           &>/dev/null || true

# ── Función de limpieza (Ctrl+C) ──
cleanup() {
    echo ""
    warn "Deteniendo el laboratorio..."
    docker stop  "$CONTAINER_NAME" &>/dev/null || true
    docker rm    "$CONTAINER_NAME" &>/dev/null || true
    docker network rm "$NET_NAME"  &>/dev/null || true
    ip link del  "$SHIM"           &>/dev/null || true
    printf "${GREEN}[+] Laboratorio eliminado correctamente. ¡Hasta pronto!${NC}\n\n"
    exit 0
}
trap cleanup SIGINT SIGTERM

# ── Construir imagen Docker ──
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
log "Construyendo imagen Docker (puede tardar unos minutos la primera vez)..."
docker build -t "$IMAGE_NAME" "$SCRIPT_DIR" --quiet \
    || err "Error al construir la imagen Docker."
log "Imagen construida correctamente."

# ── Crear red macvlan ──
log "Creando red macvlan '$NET_NAME'..."
docker network create \
    --driver macvlan \
    --subnet="$SUBNET" \
    --gateway="$GATEWAY" \
    --opt parent="$IFACE" \
    "$NET_NAME" > /dev/null \
    || err "No se pudo crear la red macvlan."

# ── Crear shim macvlan para que el host pueda alcanzar el contenedor ──
ip link add "$SHIM" link "$IFACE" type macvlan mode bridge 2>/dev/null || true
ip addr add "${NET_BASE}.200/32" dev "$SHIM"               2>/dev/null || true
ip link set "$SHIM" up
ip route add "${CONTAINER_IP}/32" dev "$SHIM"              2>/dev/null || true

# ── Iniciar contenedor ──
log "Iniciando contenedor HackLabs..."
docker run -d \
    --name "$CONTAINER_NAME" \
    --network "$NET_NAME" \
    --ip "$CONTAINER_IP" \
    --cap-add NET_ADMIN \
    "$IMAGE_NAME" > /dev/null \
    || err "No se pudo iniciar el contenedor."

# ── Esperar que el servicio HTTP esté listo ──
printf "${GREEN}[+]${NC} Esperando que el servicio arranque"
for i in $(seq 1 30); do
    curl -sf --connect-timeout 1 "http://${CONTAINER_IP}" &>/dev/null && break
    printf "."
    sleep 1
done
echo ""

# ── Panel de información ──
echo ""
echo -e "  ${GREEN}════════════════════════════════════════════════════${NC}"
echo -e "  ${BOLD}${GREEN}  ✓  Laboratorio desplegado correctamente${NC}"
echo -e "  ${GREEN}════════════════════════════════════════════════════${NC}"
echo ""
echo -e "  ${CYAN}${BOLD}  IP del objetivo:   ${CONTAINER_IP}${NC}"
echo ""
echo -e "  ${DIM}  HTTP  →  http://${CONTAINER_IP}${NC}"
echo -e "  ${DIM}  FTP   →  ftp://${CONTAINER_IP}  (puerto 21)${NC}"
echo -e "  ${DIM}  SSH   →  ssh user@${CONTAINER_IP}  (puerto 22)${NC}"
echo -e "  ${DIM}  SMB   →  //${CONTAINER_IP}/  (puerto 445)${NC}"
echo ""
echo -e "  ${DIM}  nmap -sV -p 21,22,80,445 ${CONTAINER_IP}${NC}"
echo ""
echo -e "  ${GREEN}════════════════════════════════════════════════════${NC}"
echo ""
echo -e "  ${YELLOW}  Presiona Ctrl+C para detener el laboratorio${NC}"
echo ""

# ── Bucle de espera ──
while true; do sleep 1; done
