# HackLabs

![hacklabs](https://github.com/user-attachments/assets/d4e40085-7b36-46b2-9be6-9c37f7c2140a)

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
- **Selector de dificultad** (Easy / Medium / Hard) que modifica las protecciones de cada lab en tiempo real

---

## 🛡️ Sistema de Dificultad

HackLabs incluye un **selector de dificultad** en la barra de navegación (similar a Mutillidae/DVWA) que ajusta las protecciones de **todos** los laboratorios en tiempo real. La dificultad seleccionada se mantiene entre labs y persiste durante toda la sesión.

| Nivel | Descripción | Color |
|-------|-------------|-------|
| **Easy** | Sin protección — vulnerabilidades completamente expuestas | 🟢 Verde |
| **Medium** | Filtros básicos — bypass posible con técnicas intermedias | 🟡 Ámbar |
| **Hard** | WAF / validación avanzada — requiere técnicas avanzadas de bypass | 🔴 Rojo |

### Detalle por laboratorio

<details>
<summary><strong>A01 — IDOR (Broken Access Control)</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Devuelve **todos** los campos del usuario (incluye `password_md5` y `password_plain`) |
| Medium | Oculta `password_plain` pero expone `password_md5` y `security_answer` |
| Hard | Solo datos básicos: `id`, `username`, `email`, `role` |

</details>

<details>
<summary><strong>A02 — Cryptographic Failures</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Hash MD5 expuesto en cookie sin `HttpOnly` ni salt |
| Medium | Cookie `HttpOnly` pero sigue siendo MD5 sin salt |
| Hard | SHA256 con salt estático `"hacklabs"` + cookie `HttpOnly` + `SameSite` |

</details>

<details>
<summary><strong>A03 — SQL Injection</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Sin filtro — inyección SQL directa con errores expuestos |
| Medium | WAF básico bloquea `UNION`, `SELECT`, `OR` (bypass: variaciones de mayúsculas) |
| Hard | Regex WAF agresivo + errores ocultos (bypass: ofuscación avanzada) |

</details>

<details>
<summary><strong>A03 — Command Injection</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Sin filtro — `shell=True` con inyección directa |
| Medium | Filtra `;` y `\|` (bypass: `&`, backticks, `$()`, newlines) |
| Hard | Filtra `;` `\|` `&` `` ` `` `$` `()` `{}` `<` `>` (bypass: `\n` newline) |

</details>

<details>
<summary><strong>A04 — Insecure Design (Password Recovery)</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Pregunta secreta visible + sin rate-limiting |
| Medium | Pregunta parcialmente censurada + 5 intentos / 30s |
| Hard | Pregunta oculta + 3 intentos / 60s + errores genéricos |

</details>

<details>
<summary><strong>A05 — Security Misconfiguration</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Panel `/admin` sin autenticación — acceso total |
| Medium | Requiere cookie `is_admin=true` (bypass: editar cookie) |
| Hard | Requiere header `X-Admin-Token: hacklabs-admin-2024` |

</details>

<details>
<summary><strong>A06 — Outdated Components</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Sin filtro XSS — inyección de tags directa |
| Medium | Filtra `<script>` pero no event handlers ni otros tags |
| Hard | Filtra `<` y `>` (bypass: atributos inline) |

</details>

<details>
<summary><strong>A07 — Authentication Failures</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Sin rate-limiting — brute force ilimitado |
| Medium | Límite: 10 intentos / 30 segundos |
| Hard | Límite: 5 intentos / 60 segundos + errores genéricos |

</details>

<details>
<summary><strong>A08 — Software & Data Integrity Failures</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Campo `role` editable vía API + todos los campos visibles |
| Medium | `role` bloqueado en PUT + vista sin campo role |
| Hard | Solo `email` editable + requiere header Authorization + vista mínima |

</details>

<details>
<summary><strong>A09 — Security Logging & Monitoring Failures</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Sin logging — el atacante es invisible |
| Medium | Solo registra logins exitosos con IP (fallos invisibles) |
| Hard | Registra éxitos y fallos pero sin IP (auditoría incompleta) |

</details>

<details>
<summary><strong>A10 — SSRF</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Sin filtro — SSRF a servicios internos directamente |
| Medium | Bloquea `localhost`, `127.0.0.1` (bypass: IP decimal, 0x7f000001) |
| Hard | Bloquea rangos privados (bypass: DNS rebinding, IPv6) |

</details>

<details>
<summary><strong>XSS — Reflected / Stored / DOM</strong></summary>

**Reflected & Stored:**

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Sin filtro — inyección XSS directa |
| Medium | Filtra `<script>` (bypass: event handlers `onerror`, `onload`) |
| Hard | Filtra `<` y `>` (bypass: inyección de atributos) |

**DOM XSS:**

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Sin CSP — DOM XSS vía JavaScript inseguro del cliente |
| Medium | CSP permite `'unsafe-inline'` (bypass: event handlers) |
| Hard | CSP estricto `script-src 'self'` (bypass: mutation XSS, DOM clobbering) |

</details>

<details>
<summary><strong>CSRF</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Sin protección CSRF + todos los campos del perfil visibles |
| Medium | Verificación de header `Referer` (bypass: supresión/manipulación) |
| Hard | Requiere header `X-CSRF-Token` en sesión (bypass: XSS para robar token) |

</details>

<details>
<summary><strong>File Upload</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Sin validación — cualquier archivo con nombre original |
| Medium | Blacklist de extensiones peligrosas (bypass: doble extensión `.php.jpg`) |
| Hard | Whitelist + verificación Content-Type (bypass: magic bytes) |

</details>

<details>
<summary><strong>XXE — XML External Entity</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Sin protección XXE — `resolve_entities` habilitado |
| Medium | Bloquea `<!DOCTYPE` literal (bypass: variaciones de mayúsculas/encoding) |
| Hard | Bloquea `DOCTYPE`, `ENTITY`, `SYSTEM`, `PUBLIC` (bypass: codificación UTF) |

</details>

<details>
<summary><strong>Path Traversal / LFI</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Sin filtro — `../` traversal directo |
| Medium | Filtra `../` una vez (bypass: `..\`, URL encoding `%2e%2e%2f`) |
| Hard | Filtra `../` y `..\` recursivamente (bypass: doble URL-encoding) |

</details>

<details>
<summary><strong>Bruteforce (HTTP + FTP)</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Sin rate-limiting — intentos ilimitados |
| Medium | Límite: 5 intentos / 30 segundos |
| Hard | Límite: 3 intentos / 60 segundos (+ delay de 1s en FTP) |

</details>

<details>
<summary><strong>SSTI — Server-Side Template Injection</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Sin filtro — inyección Jinja2 directa `{{ 7*7 }}` |
| Medium | Bloquea `{{ }}` (bypass: `{% print 7*7 %}`) |
| Hard | Bloquea `{{ }}`, `{% %}` y keywords peligrosos (bypass: filtros Jinja2, codificación) |

</details>

<details>
<summary><strong>Open Redirect</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Sin validación — redirección a cualquier URL |
| Medium | Bloquea `http://` y `https://` externos (bypass: `//`, `javascript:`) |
| Hard | Bloquea dominios externos y protocol-relative (bypass: `@`, encoding) |

</details>

<details>
<summary><strong>JWT Manipulation</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Acepta `alg=none` + secreto expuesto en la interfaz |
| Medium | Rechaza `alg=none` pero secreto débil (bypass: brute force con hashcat) |
| Hard | Rechaza `alg=none` + secreto fuerte (bypass: kid injection, jwt_tool) |

</details>

<details>
<summary><strong>Insecure Deserialization</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | `pickle.loads()` directo del input del usuario |
| Medium | Blacklist de keywords (`os`, `subprocess`, `system`, `popen`...) |
| Hard | Bloqueo de opcodes peligrosos de pickle (`R`, `i`, `c`, `0x81`) |

</details>

<details>
<summary><strong>CORS Misconfiguration</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Refleja cualquier Origin + `Access-Control-Allow-Credentials: true` |
| Medium | Solo permite orígenes `*.hacklabs.local` (bypass: subdominio) |
| Hard | Regex estricto (bypass: prefijo de dominio similar) |

</details>

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
