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
MSF_CONTAINER_NAME="hacklabs-metasploit"
MSF_IMAGE_NAME="hacklabs-metasploit:latest"
NET_NAME="hacklabs_net"
SHIM="macvlan0"

# ── Domain Controller vulnerable (categoría Active Directory) ──
# Exporta HL_SKIP_AD=1 para desplegar solo la web y saltarte el DC.
DC_CONTAINER_NAME="hacklabs-dc"
DC_IMAGE_NAME="hacklabs-dc:latest"
AD_REALM="HACKLABS.LOCAL"
AD_DOMAIN="HACKLABS"
AD_DC_HOSTNAME="DC01"
AD_ADMIN_PASSWORD='Adm1nP@ss2024!'
AD_FQDN="dc01.hacklabs.local"
DEPLOY_AD=1
[[ "${HL_SKIP_AD:-0}" == "1" ]] && DEPLOY_AD=0
DEPLOY_MSF=1

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

# ── Seleccionar IPs libres en rango .100–.199 (web + ActiveMQ + DC) ──
CONTAINER_IP=""
DC_IP=""
MSF_IP=""
NEEDED=1
[[ $DEPLOY_AD -eq 1 ]] && NEEDED=2
[[ $DEPLOY_MSF -eq 1 ]] && NEEDED=$((NEEDED + 1))
while read -r OCTET; do
    CANDIDATE="${NET_BASE}.${OCTET}"
    ping -c1 -W1 "$CANDIDATE" &>/dev/null 2>&1 && continue
    if [[ -z "$CONTAINER_IP" ]]; then
        CONTAINER_IP="$CANDIDATE"
    elif [[ $DEPLOY_MSF -eq 1 && -z "$MSF_IP" ]]; then
        MSF_IP="$CANDIDATE"
    elif [[ $DEPLOY_AD -eq 1 && -z "$DC_IP" ]]; then
        DC_IP="$CANDIDATE"
        break
    else
        break
    fi
done < <(shuf -i 100-199)
[[ -z "$CONTAINER_IP" ]] && err "No se encontró ninguna IP libre en ${NET_BASE}.100-199."
if [[ $DEPLOY_MSF -eq 1 && -z "$MSF_IP" ]]; then
    warn "No se encontró una IP libre para ActiveMQ — se continúa sin H04."
    DEPLOY_MSF=0
fi
if [[ $DEPLOY_AD -eq 1 && -z "$DC_IP" ]]; then
    warn "Solo se encontró una IP libre — el Domain Controller no se desplegará."
    DEPLOY_AD=0
fi
log "IP asignada al laboratorio: ${BOLD}${CONTAINER_IP}${NC}"
[[ $DEPLOY_MSF -eq 1 ]] && log "IP asignada al objetivo ActiveMQ: ${BOLD}${MSF_IP}${NC}"
[[ $DEPLOY_AD -eq 1 ]] && log "IP asignada al Domain Controller: ${BOLD}${DC_IP}${NC}"

# ── Limpiar instancias previas ──
warn "Limpiando instancias previas si existen..."
docker stop  "$DC_CONTAINER_NAME" &>/dev/null || true
docker rm    "$DC_CONTAINER_NAME" &>/dev/null || true
docker stop  "$MSF_CONTAINER_NAME" &>/dev/null || true
docker rm    "$MSF_CONTAINER_NAME" &>/dev/null || true
docker stop  "$CONTAINER_NAME" &>/dev/null || true
docker rm    "$CONTAINER_NAME" &>/dev/null || true
docker network rm "$NET_NAME"  &>/dev/null || true
ip link del  "$SHIM"           &>/dev/null || true

# ── Función de limpieza (Ctrl+C) ──
cleanup() {
    echo ""
    warn "Deteniendo el laboratorio..."
    docker stop  "$DC_CONTAINER_NAME" &>/dev/null || true
    docker rm    "$DC_CONTAINER_NAME" &>/dev/null || true
    docker stop  "$MSF_CONTAINER_NAME" &>/dev/null || true
    docker rm    "$MSF_CONTAINER_NAME" &>/dev/null || true
    docker stop  "$CONTAINER_NAME" &>/dev/null || true
    docker rm    "$CONTAINER_NAME" &>/dev/null || true
    docker network rm "$NET_NAME"  &>/dev/null || true
    ip link del  "$SHIM"           &>/dev/null || true
    sed -i -E "/[[:space:]](${AD_FQDN}|hacklabs\.local|dc01)([[:space:]]|\$)/Id" /etc/hosts &>/dev/null || true
    echo "${GREEN}[+] Laboratorio eliminado correctamente. ¡Hasta pronto!${NC}"
    echo ""
    exit 0
}
trap cleanup SIGINT SIGTERM

# ── Construir imagen Docker ──
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GIT_HASH=$(git -C "$SCRIPT_DIR" rev-parse --short HEAD 2>/dev/null || date +%s)
log "Construyendo imagen Docker..."
docker build -t "$IMAGE_NAME" --build-arg CACHEBUST="$GIT_HASH" "$SCRIPT_DIR" --quiet \
    || err "Error al construir la imagen Docker."

if [[ $DEPLOY_AD -eq 1 ]]; then
    log "Construyendo imagen del Domain Controller (Samba AD DC)..."
    warn "La primera vez descarga ~400 MB de paquetes, puede tardar unos minutos."
    if ! docker build -t "$DC_IMAGE_NAME" "$SCRIPT_DIR/ad_hoc/active_directory" --quiet >/dev/null; then
        warn "No se pudo construir la imagen del Domain Controller — se continúa sin él."
        DEPLOY_AD=0
    fi
fi

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
[[ $DEPLOY_MSF -eq 1 ]] && ip route add "${MSF_IP}/32" dev "$SHIM" 2>/dev/null || true
[[ $DEPLOY_AD -eq 1 ]] && ip route add "${DC_IP}/32" dev "$SHIM" 2>/dev/null || true

# ── Iniciar contenedor ──
log "Iniciando contenedor HackLabs..."
docker run -d \
    --name "$CONTAINER_NAME" \
    --network "$NET_NAME" \
    --ip "$CONTAINER_IP" \
    --hostname hacklabs \
    --cap-add NET_ADMIN \
    -e MSF_TARGET_IP="${MSF_IP}" \
    -e AD_DC_IP="${DC_IP}" \
    -e AD_REALM="${AD_REALM}" \
    -e AD_DOMAIN="${AD_DOMAIN}" \
    -e AD_DC_HOSTNAME="${AD_DC_HOSTNAME}" \
    -v hacklabs_db:/app/data \
    -v hacklabs_uploads:/app/uploads \
    -v hacklabs_logs:/app/logs \
    "$IMAGE_NAME" > /dev/null \
    || err "No se pudo iniciar el contenedor."

# ── Iniciar objetivo ActiveMQ vulnerable (H04) ──
if [[ $DEPLOY_MSF -eq 1 ]]; then
    log "Construyendo imagen del objetivo ActiveMQ 5.18.2..."
    if ! docker build -t "$MSF_IMAGE_NAME" "$SCRIPT_DIR/ad_hoc/metasploit" --quiet >/dev/null; then
        warn "No se pudo construir ActiveMQ — se continúa sin H04."
        DEPLOY_MSF=0
    elif ! docker run -d \
        --name "$MSF_CONTAINER_NAME" \
        --network "$NET_NAME" \
        --ip "$MSF_IP" \
        --hostname metasploit-target \
        "$MSF_IMAGE_NAME" > /dev/null; then
        warn "No se pudo iniciar ActiveMQ — se continúa sin H04."
        DEPLOY_MSF=0
    fi
fi

# ── Iniciar el Domain Controller vulnerable ──
if [[ $DEPLOY_AD -eq 1 ]]; then
    log "Iniciando Domain Controller ${BOLD}${AD_FQDN}${NC}..."
    if docker run -d \
        --name "$DC_CONTAINER_NAME" \
        --network "$NET_NAME" \
        --ip "$DC_IP" \
        --hostname "$(echo "$AD_DC_HOSTNAME" | tr '[:upper:]' '[:lower:]')" \
        --cap-add SYS_ADMIN \
        -e AD_REALM="$AD_REALM" \
        -e AD_DOMAIN="$AD_DOMAIN" \
        -e AD_DC_HOSTNAME="$AD_DC_HOSTNAME" \
        -e AD_ADMIN_PASSWORD="$AD_ADMIN_PASSWORD" \
        -v hacklabs_dc_state:/var/lib/samba \
        -v hacklabs_dc_conf:/etc/samba \
        -v hacklabs_dc_shares:/srv/shares \
        "$DC_IMAGE_NAME" > /dev/null; then

        echo -n "${GREEN}[+]${NC} Provisionando el dominio ${AD_REALM}"
        for _ in $(seq 1 90); do
            if docker exec "$DC_CONTAINER_NAME" \
                 smbclient -N -L "//127.0.0.1" &>/dev/null; then
                break
            fi
            echo -n "."
            sleep 2
        done
        echo ""

        # Resolución de nombres en el host (Kerberos necesita el FQDN).
        # Se elimina primero CUALQUIER entrada previa que mencione el DC
        # (por FQDN, "hacklabs.local" o "dc01" sueltos, sin distinguir
        # mayúsculas/minúsculas) para sobreescribirla con la IP actual en
        # vez de acumular entradas obsoletas en cada redespliegue.
        sed -i -E "/[[:space:]](${AD_FQDN}|hacklabs\.local|dc01)([[:space:]]|\$)/Id" /etc/hosts 2>/dev/null || true
        printf '%s\t%s hacklabs.local dc01\n' "$DC_IP" "$AD_FQDN" >> /etc/hosts
        log "Añadida la entrada ${BOLD}${DC_IP} ${AD_FQDN}${NC} a /etc/hosts."
    else
        warn "No se pudo iniciar el Domain Controller — se continúa sin él."
        DEPLOY_AD=0
    fi
fi

# ── Esperar que el servicio HTTP esté listo ──
echo -n "${GREEN}[+]${NC} Esperando que el servicio arranque"
sleep 5
for _ in $(seq 1 30); do
    curl -sf --connect-timeout 1 "http://${CONTAINER_IP}" &>/dev/null && break
    echo -n "."
    sleep 1
done
echo ""
if [[ $DEPLOY_MSF -eq 1 ]]; then
    echo -n "${GREEN}[+]${NC} Esperando ActiveMQ OpenWire/Jetty"
    for _ in $(seq 1 30); do
        if curl -sf --connect-timeout 1 "http://${MSF_IP}:8161/" &>/dev/null; then break; fi
        echo -n "."
        sleep 1
    done
    echo ""
fi

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
if [[ $DEPLOY_MSF -eq 1 ]]; then
    echo "  ${CYAN}${BOLD}  ActiveMQ H04:      ${MSF_IP}${NC}"
    echo "  ${DIM}  OpenWire → ${MSF_IP}:61616${NC}"
    echo "  ${DIM}  Consola → http://${MSF_IP}:8161${NC}"
    echo "  ${DIM}  nmap -sV -p 61616,8161 ${MSF_IP}${NC}"
    echo ""
fi
if [[ $DEPLOY_AD -eq 1 ]]; then
    echo "  ${CYAN}${BOLD}  Domain Controller:  ${DC_IP}   (${AD_FQDN})${NC}"
    echo ""
    echo "  ${DIM}  Dominio  →  ${AD_REALM}  ·  NetBIOS: ${AD_DOMAIN}${NC}"
    echo "  ${DIM}  Servicios →  DNS/53 · Kerberos/88 · LDAP/389 · SMB/445 · LDAPS/636${NC}"
    echo "  ${DIM}  Foothold  →  svc.readonly (publicado en el recurso //${DC_IP}/public)${NC}"
    echo ""
    echo "  ${DIM}  nxc smb ${DC_IP} -u '' -p '' --shares${NC}"
    echo "  ${DIM}  nmap -sV -p 53,88,135,139,389,445,464,636,3268 ${DC_IP}${NC}"
    echo ""
    echo "  ${GREEN}════════════════════════════════════════════════════${NC}"
    echo ""
fi
echo "  ${YELLOW}  Presiona Ctrl+C para detener el laboratorio${NC}"
echo ""

# ── Abrir Firefox ──
# Si Firefox ya está abierto en la sesión del usuario, abrir nueva pestaña
# en ESA sesión (mismo perfil logueado, extensiones, etc.).
_BROWSER_USER="${SUDO_USER:-}"
if [[ -n "$_BROWSER_USER" ]]; then
    _FF=$(command -v firefox-esr 2>/dev/null || command -v firefox 2>/dev/null)
    if [[ -n "$_FF" ]]; then
        _URL="http://${CONTAINER_IP}"
        _FF_PID=$(pgrep -u "$_BROWSER_USER" -x firefox | head -1)
        [[ -z "$_FF_PID" ]] && _FF_PID=$(pgrep -u "$_BROWSER_USER" -x firefox-esr | head -1)

        # Intenta heredar entorno gráfico de la sesión real del usuario.
        _DISPLAY=":0"
        _DBUS=""
        if [[ -n "$_FF_PID" ]] && [[ -r "/proc/${_FF_PID}/environ" ]]; then
            _ENV_DUMP=$(tr '\0' '\n' < "/proc/${_FF_PID}/environ" 2>/dev/null || true)
            _DISPLAY=$(printf '%s\n' "$_ENV_DUMP" | awk -F= '/^DISPLAY=/{print $2; exit}')
            _DBUS=$(printf '%s\n' "$_ENV_DUMP" | awk -F= '/^DBUS_SESSION_BUS_ADDRESS=/{print substr($0,index($0,$2)); exit}')
            [[ -z "$_DISPLAY" ]] && _DISPLAY=":0"
        fi

        if [[ -n "$_FF_PID" ]]; then
            # Firefox ya abierto: fuerza nueva pestaña en la sesión existente.
            if [[ -n "$_DBUS" ]]; then
                sudo -u "$_BROWSER_USER" env DISPLAY="$_DISPLAY" \
                    DBUS_SESSION_BUS_ADDRESS="$_DBUS" \
                    HOME="/home/${_BROWSER_USER}" \
                    "$_FF" --new-tab "$_URL" &>/dev/null &
            else
                sudo -u "$_BROWSER_USER" env DISPLAY="$_DISPLAY" \
                    HOME="/home/${_BROWSER_USER}" \
                    "$_FF" --new-tab "$_URL" &>/dev/null &
            fi
        else
            # No hay Firefox abierto: abrir con perfil normal del usuario.
            sudo -u "$_BROWSER_USER" env DISPLAY="$_DISPLAY" \
                HOME="/home/${_BROWSER_USER}" \
                "$_FF" "$_URL" &>/dev/null &
        fi
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
    if [[ $DEPLOY_MSF -eq 1 ]] && ! docker inspect -f '{{.State.Running}}' "$MSF_CONTAINER_NAME" &>/dev/null 2>&1; then
        echo ""
        warn "El objetivo ActiveMQ se ha detenido inesperadamente."
        break
    fi
    sleep 5
done
