#!/usr/bin/env bash
# HackLabs – Script de instalación para Kali Linux
# Uso: chmod +x setup.sh && ./setup.sh

set -e

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
info()  { echo -e "${GREEN}[*]${NC} $1"; }
warn()  { echo -e "${YELLOW}[!]${NC} $1"; }
error() { echo -e "${RED}[✗]${NC} $1"; exit 1; }

echo ""
echo -e "${RED}  ██╗  ██╗ █████╗  ██████╗██╗  ██╗██╗      █████╗ ██████╗ ███████╗${NC}"
echo -e "${RED}  ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██║     ██╔══██╗██╔══██╗██╔════╝${NC}"
echo -e "${RED}  ███████║███████║██║     █████╔╝ ██║     ███████║██████╔╝███████╗${NC}"
echo -e "${RED}  ██╔══██║██╔══██║██║     ██╔═██╗ ██║     ██╔══██║██╔══██╗╚════██║${NC}"
echo -e "${RED}  ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║██████╔╝███████║${NC}"
echo -e "${RED}  ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝${NC}"
echo ""
warn "Aplicación INTENCIONALMENTE VULNERABLE. Úsala solo en entornos aislados."
echo ""

# Verificar Python 3
command -v python3 &>/dev/null || error "Python 3 no encontrado. Instálalo con: sudo apt install python3"
info "Python 3 encontrado: $(python3 --version)"

# Crear entorno virtual
if [ ! -d "venv" ]; then
  info "Creando entorno virtual..."
  python3 -m venv venv
fi

# Activar entorno virtual
source venv/bin/activate
info "Entorno virtual activado."

# Instalar dependencias
info "Instalando dependencias Python..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
info "Dependencias instaladas."

# Crear directorios necesarios
mkdir -p uploads logs static/files
info "Directorios creados."

# Inicializar base de datos
info "Inicializando base de datos..."
python3 init_db.py

echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}  Instalación completada exitosamente   ${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo -e "  Ejecutar la aplicación:"
echo -e "  ${YELLOW}source venv/bin/activate && python app.py${NC}"
echo ""
echo -e "  Acceder en: ${GREEN}http://localhost:5000${NC}"
echo ""
echo -e "  Credenciales por defecto:"
echo -e "  ${YELLOW}admin / admin123${NC}  (administrador)"
echo -e "  ${YELLOW}alice / password${NC}  (usuario normal)"
echo ""
