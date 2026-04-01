#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────
# HackLabs – Despliegue Docker al estilo DockerLabs
# Uso: sudo bash deploy.sh
# ─────────────────────────────────────────────────────────────────

# ── Colores (usando $'…' para que los escapes se resuelvan al asignar) ──
RED=$'\033[0;31m'; GREEN=$'\033[0;32m'; YELLOW=$'\033[1;33m'
CYAN=$'\033[0;36m'; BOLD=$'\033[1m'; DIM=$'\033[2m'; NC=$'\033[0m'

CONTAINER_NAME="hacklabs"
IMAGE_NAME="hacklabs:latest"
NET_NAME="hacklabs_net"
SHIM="macvlan0"

log()  { echo "${GREEN}[+]${NC} $1"; }
warn() { echo "${YELLOW}[!]${NC} $1"; }
err()  { echo "${RED}[✗] $1${NC}"; exit 1; }

# ── Banner ──
clear
echo ""
echo "${RED}    __  __              __    __           __         ${NC}"
echo "${RED}   / / / /____ _ _____ / /__ / /   ____ _ / /_   _____${NC}"
echo "${RED}  / /_/ // __ \`// ___// //_// /   / __ \`// __ \\ / ___/${NC}"
echo "${RED} / __  // /_/ // /__ / ,<  / /___/ /_/ // /_/ /(__  ) ${NC}"
echo "${RED}/_/ /_/ \\__,_/ \\___//_/|_|/_____/\\__,_//_.___//____/  ${NC}"
echo ""
echo "  ${DIM}Intentionally Vulnerable Labs · by afsh4ck${NC}"
echo "  ${RED}[!] ADVERTENCIA: Solo usar en entornos aislados y controlados${NC}"
echo ""

# ── Verificar root ──
[[ $EUID -ne 0 ]] && err "Ejecuta con privilegios root: ${YELLOW}sudo bash deploy.sh${NC}"

# ── Verificar Docker ──
if ! command -v docker &>/dev/null; then
    echo "${YELLOW}[!]${NC} Docker no está instalado en el sistema."
    read -rp "    ¿Deseas instalar Docker ahora? (y/n): " INSTALL_DOCKER
    if [[ "$INSTALL_DOCKER" =~ ^[yYsS]$ ]]; then
        log "Instalando Docker..."
        apt-get update -qq
        apt-get install -y -qq docker.io > /dev/null 2>&1 || err "Error al instalar Docker."
        systemctl enable --now docker > /dev/null 2>&1
        log "Docker instalado correctamente."
    else
        err "Docker es necesario para desplegar HackLabs."
    fi
fi

if ! docker info &>/dev/null; then
    echo "${YELLOW}[!]${NC} El servicio Docker no está activo."
    read -rp "    ¿Deseas iniciar Docker ahora? (y/n): " START_DOCKER
    if [[ "$START_DOCKER" =~ ^[yYsS]$ ]]; then
        systemctl start docker
        sleep 2
        docker info &>/dev/null || err "No se pudo iniciar Docker."
        log "Docker iniciado correctamente."
    else
        err "Docker debe estar activo para desplegar HackLabs."
    fi
fi

# ── Detectar interfaz de red ──
IFACE="eth0"
if ! ip link show "$IFACE" &>/dev/null; then
    IFACE=$(ip route | awk '/default/{print $5; exit}')
    [[ -z "$IFACE" ]] && err "No se detectó ninguna interfaz de red activa."
    warn "eth0 no disponible — usando ${BOLD}$IFACE${NC}"
fi

HOST_IP_CIDR=$(ip -4 addr show "$IFACE" | grep -oP '(?<=inet\s)\d+\.\d+\.\d+\.\d+/\d+' | head -1)
[[ -z "$HOST_IP_CIDR" ]] && err "No se pudo detectar la IP de $IFACE."

# Extraer componentes
HOST_IP=$(echo "$HOST_IP_CIDR" | cut -d/ -f1)
CIDR_MASK=$(echo "$HOST_IP_CIDR" | cut -d/ -f2)
NET_BASE=$(echo "$HOST_IP" | grep -oP '^\d+\.\d+\.\d+')

# Calcular la dirección de red correcta (para Docker macvlan)
IFS='.' read -r O1 O2 O3 O4 <<< "$HOST_IP"
if [[ "$CIDR_MASK" -eq 24 ]]; then
    NETWORK_ADDR="${O1}.${O2}.${O3}.0"
elif [[ "$CIDR_MASK" -eq 16 ]]; then
    NETWORK_ADDR="${O1}.${O2}.0.0"
elif [[ "$CIDR_MASK" -eq 8 ]]; then
    NETWORK_ADDR="${O1}.0.0.0"
else
    NETWORK_ADDR="${O1}.${O2}.${O3}.0"
fi
SUBNET="${NETWORK_ADDR}/${CIDR_MASK}"

GATEWAY=$(ip route | awk "/default.*$IFACE/{print \$3; exit}")
[[ -z "$GATEWAY" ]] && GATEWAY=$(ip route | awk '/default/{print $3; exit}')
[[ -z "$GATEWAY" ]] && err "No se pudo detectar la puerta de enlace."

log "Red detectada: ${BOLD}$SUBNET${NC} en ${BOLD}$IFACE${NC} (gateway ${BOLD}$GATEWAY${NC})"

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
    echo "${GREEN}[+] Laboratorio eliminado correctamente. ¡Hasta pronto!${NC}"
    echo ""
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
log "Creando red macvlan '${BOLD}$NET_NAME${NC}'..."
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
echo -n "${GREEN}[+]${NC} Esperando que el servicio arranque"
for _ in $(seq 1 30); do
    curl -sf --connect-timeout 1 "http://${CONTAINER_IP}" &>/dev/null && break
    echo -n "."
    sleep 1
done
echo ""

# ── Panel de información ──
echo ""
echo "  ${GREEN}════════════════════════════════════════════════════${NC}"
echo "  ${BOLD}${GREEN}  ✓  Laboratorio desplegado correctamente${NC}"
echo "  ${GREEN}════════════════════════════════════════════════════${NC}"
echo ""
echo "  ${CYAN}${BOLD}  IP del objetivo:   ${CONTAINER_IP}${NC}"
echo ""
echo "  ${DIM}  HTTP  →  http://${CONTAINER_IP}${NC}"
echo "  ${DIM}  FTP   →  ftp://${CONTAINER_IP}  (puerto 21)${NC}"
echo "  ${DIM}  SSH   →  ssh user@${CONTAINER_IP}  (puerto 22)${NC}"
echo "  ${DIM}  SMB   →  //${CONTAINER_IP}/  (puerto 445)${NC}"
echo ""
echo "  ${DIM}  nmap -sV -p 21,22,80,445 ${CONTAINER_IP}${NC}"
echo ""
echo "  ${GREEN}════════════════════════════════════════════════════${NC}"
echo ""
echo "  ${YELLOW}  Presiona Ctrl+C para detener el laboratorio${NC}"
echo ""

# ── Abrir navegador ──
# deploy.sh corre como root; hay que lanzar Firefox como el usuario original
_BROWSER_USER="${SUDO_USER:-}"
if [[ -n "$_BROWSER_USER" ]]; then
    # Obtener DISPLAY del usuario original (sesión gráfica activa)
    _DISPLAY=$(grep -z DISPLAY /proc/$(pgrep -u "$_BROWSER_USER" -n)/environ 2>/dev/null | tr -d '\0' | sed 's/DISPLAY=//')
    [[ -z "$_DISPLAY" ]] && _DISPLAY=":0"
    if command -v firefox &>/dev/null; then
        sudo -u "$_BROWSER_USER" DISPLAY="$_DISPLAY" firefox --new-tab "http://${CONTAINER_IP}" &>/dev/null &
    elif command -v xdg-open &>/dev/null; then
        sudo -u "$_BROWSER_USER" DISPLAY="$_DISPLAY" xdg-open "http://${CONTAINER_IP}" &>/dev/null &
    fi
fi

# ── Mantener el script activo hasta Ctrl+C ──
while true; do
    # Verificar que el contenedor sigue corriendo
    if ! docker inspect -f '{{.State.Running}}' "$CONTAINER_NAME" &>/dev/null 2>&1; then
        echo ""
        warn "El contenedor se ha detenido inesperadamente."
        break
    fi
    sleep 5
done
