# HackLabs

![hacklabs](https://github.com/user-attachments/assets/80c3a812-944c-4b6a-a40c-61242d3d019e)

**Plataforma de entrenamiento en hacking ético** — Similar a Mutillidae/DVWA pero con interfaz moderna y guías de explotación. Cubre el **OWASP Top 10 (2021)** completo + vulnerabilidades extra avanzadas.

> ⚠️ **ADVERTENCIA**: Esta aplicación es intencionalmente insegura. Úsala SOLO en entornos aislados (máquina virtual, red local sin internet). Nunca la expongas públicamente.

---

## 🎯 Características

- **22 laboratorios** cubriendo OWASP Top 10 + extras avanzados
- Guías de resolución paso a paso (ES/EN)
- Filtros de labs por criticidad (Critical / High / Medium)
- Soporte **bilingüe** (Español / English)
- Interfaz moderna oscura con **Tailwind CSS** + **Phosphor Icons**
- Compatible con **Burp Suite, sqlmap, hydra, tplmap, jwt_tool** y demás herramientas de Kali Linux

---

## 🧪 Laboratorios disponibles

### OWASP Top 10 (2021)

| # | Lab | Riesgo | Técnica |
|---|-----|--------|---------|
| A01 | IDOR – Broken Access Control | 🟠 High | `/profile?id=N` sin autenticación |
| A02 | Cryptographic Failures | 🟠 High | Contraseñas MD5 en cookie/respuesta |
| A03 | SQL Injection | 🔴 Critical | UNION-based, error-based, `sqlmap` |
| A03 | Command Injection | 🔴 Critical | Campo ping → RCE |
| A04 | Insecure Design | 🟡 Medium | Preguntas secretas predecibles |
| A05 | Security Misconfiguration | 🟡 Medium | `/admin` sin auth, `.git` expuesto |
| A06 | Outdated Components | 🟡 Medium | jQuery vulnerable con XSS |
| A07 | Auth Failures | 🟠 High | Sin rate-limiting, credenciales por defecto |
| A08 | Integrity Failures | 🟠 High | `PUT /api/user` sin validación de propiedad |
| A09 | Logging Failures | 🟡 Medium | Acciones críticas sin auditoría |
| A10 | SSRF | 🟠 High | `/fetch?url=` → recursos internos |

### Extras

| Lab | Riesgo | Técnica |
|-----|--------|---------|
| XSS (Reflected/Stored/DOM) | 🟠 High | Cross-Site Scripting |
| CSRF | 🟠 High | Cambio de contraseña sin token |
| File Upload | 🔴 Critical | Subida de webshell sin restricciones |
| XXE | 🟠 High | XML External Entity |
| Path Traversal / LFI | 🟠 High | `../../etc/passwd` |
| Bruteforce (HTTP/SSH/SMB) | 🟡 Medium | Hydra, Medusa, CrackMapExec |
| **SSTI** | 🔴 Critical | Jinja2 `render_template_string` → RCE |
| **Open Redirect** | 🟡 Medium | Parámetro URL sin whitelist |
| **JWT Manipulation** | 🟠 High | `alg=none`, secreto débil (hashcat) |
| **Insecure Deserialization** | 🔴 Critical | Python `pickle.loads()` → RCE |
| **CORS Misconfiguration** | 🟠 High | Reflejo de Origin + Allow-Credentials |

---

## 🚀 Despliegue

### ⭐ Opción 1 — Docker con IP propia en LAN (recomendado)

Despliega HackLabs como si fuera una máquina vulnerable real: con su propia IP en tu red local, escaneable con `nmap` y atacable con todas las herramientas de Kali.

**Requisitos:** Docker instalado y ejecutándose en Kali Linux.

```bash
git clone https://github.com/afsh4ck/HackLabs.git
cd HackLabs
sudo bash deploy.sh
```

El script detecta automáticamente tu red (`eth0`), asigna una **IP aleatoria** al laboratorio dentro del rango `.100–.199` y muestra el resultado:

```
    __  __              __    __           __
   / / / /____ _ _____ / /__ / /   ____ _ / /_   _____
  / /_/ // __ `// ___// //_// /   / __ `// __ \ / ___/
 / __  // /_/ // /__ / ,<  / /___/ /_/ // /_/ /(__  )
/_/ /_/ \__,_/ \___//_/|_|/_____/\__,_//_.___//____/

  ════════════════════════════════════════════════════
  ✓  Laboratorio desplegado correctamente
  ════════════════════════════════════════════════════

  IP del objetivo:   192.168.1.147

  HTTP  →  http://192.168.1.147
  FTP   →  192.168.1.147:21
  SSH   →  192.168.1.147:22
  SMB   →  192.168.1.147:445

  nmap -sV -p 21,22,80,445 192.168.1.147

  Presiona Ctrl+C para detener el laboratorio
```

Pulsa **Ctrl+C** para detener y eliminar el contenedor automáticamente.

> **Nota:** El script necesita `sudo` para crear la red macvlan (interfaz de red propia). El puerto 445 (SMB) puede estar ocupado en Windows; en Linux/Docker funciona correctamente.

---

### Opción 2 — Local sin Docker (desarrollo / pruebas rápidas)

**Requisitos:** Python 3.8+

```bash
git clone https://github.com/afsh4ck/HackLabs.git
cd HackLabs

# Instalación automática
chmod +x setup.sh && ./setup.sh

# O manual:
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python init_db.py
python app.py
```

Accede en: **http://localhost:5000**

---

## 🔑 Credenciales de prueba

| Usuario | Contraseña | Hash MD5 | Rol |
|---------|-----------|----------|-----|
| admin | admin123 | `0192023a7bbd73250516f069df18b500` | admin |
| alice | password | `5f4dcc3b5aa765d61d8327deb882cf99` | user |
| bob | 123456 | `e10adc3949ba59abbe56e057f20f883e` | user |
| charlie | qwerty | `d8578edf8458ce06fbc5bb76a58c5ca4` | user |
| dave | letmein | `0d107d09f5bbe40cade3de5c71e9e9b7` | manager |

---

## 🛠️ Herramientas compatibles

Todos los labs están diseñados para ser explotados con herramientas nativas de **Kali Linux**:

```
Burp Suite · sqlmap · hydra · medusa · ncrack · crackmapexec
tplmap · jwt_tool · hashcat · john · curl · ffuf · nikto
wfuzz · gobuster · metasploit · nmap
```

---

## 📁 Estructura del proyecto

```
HackLabs/
├── app.py                  # Aplicación Flask principal
├── init_db.py              # Inicialización de la base de datos
├── requirements.txt        # Dependencias Python
├── setup.sh                # Instalación local automática
├── deploy.sh               # ⭐ Despliegue Docker estilo DockerLabs
├── Dockerfile              # Imagen Docker
├── docker-compose.yml      # Compose con macvlan (IP propia en LAN)
├── entrypoint.sh           # Entrypoint: muestra banner + IP al arrancar
├── .dockerignore           # Excluye archivos innecesarios del build
├── hacklabs.db             # Base de datos SQLite (generada)
├── static/
│   ├── css/style.css       # Estilos CSS + variables de color
│   ├── js/main.js          # JS: i18n, sidebar, highlight, modal
│   ├── files/              # Archivos para path traversal
│   └── uploads/            # Subidas de archivos (file upload lab)
└── templates/
    ├── base.html           # Layout base con sidebar + navbar
    ├── index.html          # Home con tarjetas de labs y filtros
    ├── _lab_header.html    # Cabecera reutilizable de cada lab
    └── labs/               # 22 templates individuales de labs
```

---

## ⚙️ Variables de configuración

Edita `app.py` para cambiar:

```python
app.secret_key = 'hacklabs-insecure-key'   # No cambiar (intencional)
DATABASE = 'hacklabs.db'
UPLOAD_FOLDER = 'static/uploads'
JWT_SECRET = 'secret123'                    # Secreto débil intencional
```

---

## 🎓 Uso recomendado

1. Despliega HackLabs en una **máquina virtual Kali Linux** con red NAT/solo-anfitrión
2. Accede desde el navegador o desde la máquina host
3. Abre Burp Suite como proxy (127.0.0.1:8080)
4. Selecciona un laboratorio, lee la descripción y explota la vulnerabilidad
5. Pulsa **"Ver resolución"** para ver la guía paso a paso si te quedas atascado

---

## 📸 Screenshots

> Coming soon

---

## 📄 Licencia

MIT License — Uso libre para fines educativos.

---

<div align="center">
  <strong>Made with ❤️ by <a href="https://www.instagram.com/afsh4ck/">afsh4ck</a></strong><br/>
  <a href="https://h4ckercademy.com/">Hacking Academy</a>
</div>
