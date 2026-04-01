# HackLabs - Ethical Hacking Training Platform
# ADVERTENCIA: Esta aplicación es INTENCIONALMENTE INSEGURA.
# Úsala SOLO en entornos controlados y aislados.

from flask import (Flask, request, render_template, redirect, url_for,
                   session, jsonify, make_response, g, send_file, render_template_string)
import sqlite3
import os
import hashlib
import subprocess
import xml.etree.ElementTree as ET
from io import StringIO
import re
import base64
import json
import hmac as _hmac
import pickle
import threading
import socket

app = Flask(__name__)
app.secret_key = 'hacklabs_super_insecure_secret_2024'

# Configuración intencionalmente insegura
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['SESSION_COOKIE_SECURE'] = False
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB uploads

DATABASE = os.path.join(os.path.dirname(__file__), 'hacklabs.db')
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')

# ─────────────────────────────────────────────
# Base de datos
# ─────────────────────────────────────────────

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init_db():
    db = sqlite3.connect(DATABASE)
    with open(os.path.join(os.path.dirname(__file__), 'database', 'schema.sql'), 'r') as f:
        db.executescript(f.read())
    db.close()

# ─────────────────────────────────────────────
# RUTAS PRINCIPALES
# ─────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lab/<lab_id>')
def lab(lab_id):
    # Labs that have dedicated routes with data – redirect to them
    dedicated = {
        'idor':            '/profile',
        'misconfig':       '/admin',
        'integrity':       '/integrity',
        'auth_failures':   '/login',
        'logging':         '/logging/login',
        'sqli':            '/sqli/search',
        'cmdi':            '/cmdi/ping',
        'insecure_design': '/recover',
        'ssrf':            '/ssrf',
        'xss':             '/xss/reflected',
        'csrf':            '/csrf/profile',
        'file_upload':     '/upload',
        'xxe':             '/xxe',
        'path_traversal':  '/files',
        'bruteforce':      '/bruteforce',
        'crypto':          '/crypto/login',
        'outdated':        '/outdated/search',
    }
    if lab_id in dedicated:
        return redirect(dedicated[lab_id])
    labs = get_lab_list()
    lab_info = next((l for l in labs if l['id'] == lab_id), None)
    if not lab_info:
        return render_template('index.html', error='Laboratorio no encontrado'), 404
    try:
        return render_template(f'labs/{lab_id}.html', lab=lab_info)
    except Exception:
        return render_template('index.html', error='Template no encontrado'), 404

def get_lab_list():
    return [
        # OWASP Top 10
        {'id': 'idor',            'title': 'A01 – Broken Access Control (IDOR)',          'category': 'OWASP Top 10', 'risk': 'critical'},
        {'id': 'crypto',          'title': 'A02 – Cryptographic Failures',                 'category': 'OWASP Top 10', 'risk': 'high'},
        {'id': 'sqli',            'title': 'A03 – SQL Injection',                          'category': 'OWASP Top 10', 'risk': 'critical'},
        {'id': 'cmdi',            'title': 'A03 – Command Injection',                      'category': 'OWASP Top 10', 'risk': 'critical'},
        {'id': 'insecure_design', 'title': 'A04 – Insecure Design',                        'category': 'OWASP Top 10', 'risk': 'medium'},
        {'id': 'misconfig',       'title': 'A05 – Security Misconfiguration',              'category': 'OWASP Top 10', 'risk': 'high'},
        {'id': 'outdated',        'title': 'A06 – Vulnerable & Outdated Components',       'category': 'OWASP Top 10', 'risk': 'medium'},
        {'id': 'auth_failures',   'title': 'A07 – Auth & Identification Failures',         'category': 'OWASP Top 10', 'risk': 'critical'},
        {'id': 'integrity',       'title': 'A08 – Software & Data Integrity Failures',     'category': 'OWASP Top 10', 'risk': 'high'},
        {'id': 'logging',         'title': 'A09 – Security Logging & Monitoring Failures', 'category': 'OWASP Top 10', 'risk': 'medium'},
        {'id': 'ssrf',            'title': 'A10 – Server-Side Request Forgery (SSRF)',     'category': 'OWASP Top 10', 'risk': 'high'},
        # Extras
        {'id': 'xss',             'title': 'XSS – Cross-Site Scripting',                   'category': 'Extras',       'risk': 'high'},
        {'id': 'csrf',            'title': 'CSRF – Cross-Site Request Forgery',            'category': 'Extras',       'risk': 'high'},
        {'id': 'file_upload',     'title': 'File Upload sin restricciones',                'category': 'Extras',       'risk': 'critical'},
        {'id': 'xxe',             'title': 'XXE – XML External Entity',                    'category': 'Extras',       'risk': 'high'},
        {'id': 'path_traversal',  'title': 'Path Traversal / LFI',                        'category': 'Extras',       'risk': 'high'},
        {'id': 'bruteforce',      'title': 'Bruteforce – Login / SSH / SMB',              'category': 'Extras',       'risk': 'medium'},
        {'id': 'ssti',            'title': 'SSTI – Server-Side Template Injection',        'category': 'Extras',       'risk': 'critical'},
        {'id': 'open_redirect',   'title': 'Open Redirect',                               'category': 'Extras',       'risk': 'medium'},
        {'id': 'jwt',             'title': 'JWT Manipulation',                             'category': 'Extras',       'risk': 'high'},
        {'id': 'deserialization', 'title': 'Insecure Deserialization',                    'category': 'Extras',       'risk': 'critical'},
        {'id': 'cors',            'title': 'CORS Misconfiguration',                        'category': 'Extras',       'risk': 'high'},
    ]

@app.context_processor
def inject_labs():
    path = request.path.rstrip('/')
    # Map URL path to lab id for sidebar active state
    path_to_lab = {
        '/profile':        'idor',
        '/admin':          'misconfig',
        '/integrity':      'integrity',
        '/login':          'auth_failures',
        '/logging/login':  'logging',
        '/sqli/search':    'sqli',
        '/cmdi/ping':      'cmdi',
        '/recover':        'insecure_design',
        '/ssrf':           'ssrf',
        '/xss/reflected':  'xss',
        '/xss/stored':     'xss',
        '/xss/dom':        'xss',
        '/csrf/profile':   'csrf',
        '/upload':         'file_upload',
        '/xxe':            'xxe',
        '/files':          'path_traversal',
        '/bruteforce':         'bruteforce',
        '/bruteforce/login':   'bruteforce',
        '/crypto/login':   'crypto',
        '/outdated/search':'outdated',
        '/ssti':           'ssti',
        '/open_redirect':  'open_redirect',
        '/jwt':            'jwt',
        '/deserialization':'deserialization',
        '/cors':           'cors',
        '/cors/data':      'cors',
    }
    current_lab_id = path_to_lab.get(path, '')
    if not current_lab_id and path.startswith('/lab/'):
        current_lab_id = path[5:]

    # Detect real host for TARGET_IP replacement
    host_header = request.host          # e.g. "192.168.1.147" or "localhost:5000"
    target_ip   = host_header.split(':')[0]   # just IP/hostname
    target_port = request.host.split(':')[1] if ':' in request.host else ('80' if not request.is_secure else '443')
    if target_port == '80':
        target_base = f'http://{target_ip}'
        target_hydra = target_ip            # hydra default port 80
    else:
        target_base = f'http://{target_ip}:{target_port}'
        target_hydra = f'{target_ip} -s {target_port}'

    return {
        'all_labs': get_lab_list(),
        'current_lab_id': current_lab_id,
        'target_ip': target_ip,
        'target_port': target_port,
        'target_base': target_base,
        'target_hydra': target_hydra,
    }

# ─────────────────────────────────────────────
# A01 – IDOR (Broken Access Control)
# ─────────────────────────────────────────────

@app.route('/profile')
def profile():
    # VULNERABLE: no se verifica si el usuario autenticado puede ver este perfil
    user_id = request.args.get('id', '')
    profile = None
    error = None

    if user_id:
        db = get_db()
        try:
            profile = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        except Exception as e:
            error = str(e)

    return render_template('labs/idor.html',
                           lab=next(l for l in get_lab_list() if l['id'] == 'idor'),
                           profile=profile,
                           queried_id=user_id,
                           error=error)

# ─────────────────────────────────────────────
# A02 – Cryptographic Failures
# ─────────────────────────────────────────────

@app.route('/crypto/login', methods=['GET', 'POST'])
def crypto_login():
    lab = next(l for l in get_lab_list() if l['id'] == 'crypto')
    message = None
    weak_hash = None

    username = request.values.get('username', '')
    password = request.values.get('password', '')

    if username and password:
        # VULNERABLE: MD5 sin salt
        weak_hash = hashlib.md5(password.encode()).hexdigest()

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ? AND password_md5 = ?",
            (username, weak_hash)
        ).fetchone()

        if user:
            resp = make_response(render_template('labs/crypto.html', lab=lab,
                                                  message='Login exitoso', success=True,
                                                  weak_hash=weak_hash, username=username))
            # VULNERABLE: hash MD5 expuesto en cookie sin HttpOnly real
            resp.set_cookie('auth_token', weak_hash, httponly=False)
            resp.set_cookie('username', username, httponly=False)
            return resp
        else:
            message = 'Credenciales incorrectas'

    return render_template('labs/crypto.html', lab=lab, message=message, weak_hash=weak_hash)

# ─────────────────────────────────────────────
# A03 – SQL Injection
# ─────────────────────────────────────────────

@app.route('/sqli/search')
def sqli_search():
    lab = next(l for l in get_lab_list() if l['id'] == 'sqli')
    q = request.args.get('q', '')
    results = []
    sql_error = None
    executed_query = None

    if q:
        # VULNERABLE: concatenación directa de cadena
        executed_query = f"SELECT * FROM products WHERE name LIKE '%{q}%' OR description LIKE '%{q}%'"
        try:
            db = get_db()
            results = db.execute(executed_query).fetchall()
        except Exception as e:
            sql_error = str(e)  # VULNERABLE: error SQL expuesto al usuario

    return render_template('labs/sqli.html', lab=lab, results=results,
                           sql_error=sql_error, query=q, executed_query=executed_query)

# ─────────────────────────────────────────────
# A03 – Command Injection
# ─────────────────────────────────────────────

@app.route('/cmdi/ping', methods=['GET', 'POST'])
def cmdi_ping():
    lab = next(l for l in get_lab_list() if l['id'] == 'cmdi')
    output = None
    host = request.values.get('host', '')

    if host:
        try:
            # VULNERABLE: shell=True permite inyección de comandos
            cmd = f"ping -c 2 {host}" if os.name != 'nt' else f"ping -n 2 {host}"
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=10
            )
            output = result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            output = "Timeout: el comando tardó demasiado."
        except Exception as e:
            output = f"Error: {e}"

    return render_template('labs/cmdi.html', lab=lab, output=output, host=host)

# ─────────────────────────────────────────────
# A04 – Insecure Design (Password Recovery)
# ─────────────────────────────────────────────

@app.route('/recover', methods=['GET', 'POST'])
def recover_step1():
    lab = next(l for l in get_lab_list() if l['id'] == 'insecure_design')
    question = None
    username = ''
    error = None

    if request.method == 'POST':
        username = request.form.get('username', '')
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user:
            question = user['security_question']
        else:
            error = 'Usuario no encontrado'

    return render_template('labs/insecure_design.html', lab=lab,
                           question=question, username=username, error=error)

@app.route('/recover/answer', methods=['POST'])
def recover_answer():
    lab = next(l for l in get_lab_list() if l['id'] == 'insecure_design')
    username = request.form.get('username', '')
    answer = request.form.get('answer', '')
    db = get_db()
    # VULNERABLE: comparación en texto plano, sin rate-limiting
    user = db.execute(
        "SELECT * FROM users WHERE username = ? AND security_answer = ?",
        (username, answer)
    ).fetchone()
    if user:
        return render_template('labs/insecure_design.html', lab=lab,
                               success=True, password=user['password_plain'],
                               username=username)
    return render_template('labs/insecure_design.html', lab=lab,
                           error='Respuesta incorrecta', username=username)

# ─────────────────────────────────────────────
# A05 – Security Misconfiguration
# ─────────────────────────────────────────────

@app.route('/admin')
def admin_panel():
    lab = next(l for l in get_lab_list() if l['id'] == 'misconfig')
    db = get_db()
    # VULNERABLE: panel admin sin autenticación
    users = db.execute("SELECT * FROM users").fetchall()
    return render_template('labs/misconfig.html', lab=lab, users=users, admin=True)

@app.route('/debug/error')
def debug_error():
    # VULNERABLE: stack trace completo expuesto al usuario
    raise Exception("DEBUG: Error interno del servidor - Versión Flask 2.3.0 | Python 3.11 | SQLite 3.39 | Ruta: /var/www/hacklabs/app.py")

@app.errorhandler(500)
def internal_error(e):
    # VULNERABLE: información de stack trace expuesta
    import traceback
    return f"""
    <pre style='background:#1a1a2e;color:#e94560;padding:20px;font-family:monospace'>
    ERROR 500 – Stack Trace Expuesto (A05)
    {traceback.format_exc()}
    Server: HackLabs/1.0 Python/3.11 Flask/2.3
    DB Path: {DATABASE}
    </pre>
    """, 500

@app.route('/.git/config')
def git_config():
    # VULNERABLE: repositorio git expuesto
    return """[core]
	repositoryformatversion = 0
	filemode = true
	bare = false
[remote "origin"]
	url = http://internal-git.hacklabs.local/hacklabs.git
	fetch = +refs/heads/*:refs/remotes/origin/*
[branch "main"]
	remote = origin
	merge = refs/heads/main
""", 200, {'Content-Type': 'text/plain'}

# ─────────────────────────────────────────────
# A06 – Vulnerable & Outdated Components
# ─────────────────────────────────────────────

@app.route('/outdated/search')
def outdated_search():
    lab = next(l for l in get_lab_list() if l['id'] == 'outdated')
    q = request.args.get('q', '')
    # VULNERABLE: parámetro reflejado sin sanitización + jQuery 1.6.1 cargado en template
    return render_template('labs/outdated.html', lab=lab, query=q)

# ─────────────────────────────────────────────
# A07 – Authentication & Identification Failures
# ─────────────────────────────────────────────

@app.route('/login', methods=['GET', 'POST'])
def login():
    lab = next(l for l in get_lab_list() if l['id'] == 'auth_failures')
    message = None
    success = False

    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        password_hash = hashlib.md5(password.encode()).hexdigest()
        db = get_db()
        # VULNERABLE: sin rate-limit, sin CAPTCHA, sin bloqueo de cuenta
        user = db.execute(
            "SELECT * FROM users WHERE username = ? AND password_md5 = ?",
            (username, password_hash)
        ).fetchone()
        # NO se registra ningún log de intento fallido (A09)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            success = True
            message = f'Bienvenido, {user["username"]} (rol: {user["role"]})'
        else:
            message = 'Credenciales incorrectas'

    return render_template('labs/auth_failures.html', lab=lab, message=message, success=success)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ─────────────────────────────────────────────
# A08 – Software & Data Integrity Failures
# ─────────────────────────────────────────────

@app.route('/api/user/<int:user_id>', methods=['GET'])
def api_get_user(user_id):
    db = get_db()
    user = db.execute("SELECT id, username, email, role FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify(dict(user))

@app.route('/api/user/<int:user_id>', methods=['PUT'])
def api_update_user(user_id):
    # VULNERABLE: no se verifica que el usuario autenticado sea el propietario
    # ni se valida la firma de integridad
    data = request.get_json(silent=True) or {}
    allowed_fields = ['email', 'role', 'username']  # VULNERABLE: 'role' no debería ser editable
    updates = {k: v for k, v in data.items() if k in allowed_fields}

    if not updates:
        return jsonify({'error': 'Sin campos para actualizar'}), 400

    set_clause = ', '.join(f"{k} = ?" for k in updates)
    values = list(updates.values()) + [user_id]
    db = get_db()
    db.execute(f"UPDATE users SET {set_clause} WHERE id = ?", values)
    db.commit()
    user = db.execute("SELECT id, username, email, role FROM users WHERE id = ?", (user_id,)).fetchone()
    return jsonify({'message': 'Usuario actualizado', 'user': dict(user)})

@app.route('/integrity')
def integrity_lab():
    lab = next(l for l in get_lab_list() if l['id'] == 'integrity')
    db = get_db()
    users = db.execute("SELECT id, username, email, role FROM users").fetchall()
    return render_template('labs/integrity.html', lab=lab, users=users)

# ─────────────────────────────────────────────
# A09 – Security Logging & Monitoring Failures
# ─────────────────────────────────────────────

@app.route('/logging/login', methods=['GET', 'POST'])
def logging_login():
    lab = next(l for l in get_lab_list() if l['id'] == 'logging')
    message = None
    success = False

    username = request.values.get('username', '')
    password = request.values.get('password', '')

    if username and password:
        password_hash = hashlib.md5(password.encode()).hexdigest()
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ? AND password_md5 = ?",
            (username, password_hash)
        ).fetchone()
        # VULNERABLE: NO se registra ningún evento (ni éxito ni fallo)
        if user:
            success = True
            message = f'Login exitoso como {username}'
        else:
            message = 'Credenciales incorrectas (no hay ningún registro de este intento)'

    # Mostrar el archivo de log vacío como evidencia
    log_path = os.path.join(os.path.dirname(__file__), 'logs', 'access.log')
    log_content = ''
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            log_content = f.read()
    else:
        log_content = '(archivo de log inexistente o vacío — no se registra nada)'

    return render_template('labs/logging.html', lab=lab, message=message,
                           success=success, log_content=log_content)

# ─────────────────────────────────────────────
# A10 – SSRF
# ─────────────────────────────────────────────

@app.route('/ssrf')
def ssrf():
    lab = next(l for l in get_lab_list() if l['id'] == 'ssrf')
    url = request.args.get('url', '')
    content = None
    error = None

    if url:
        try:
            import urllib.request
            import json as _json
            # VULNERABLE: sin whitelist, permite acceso a recursos internos
            req = urllib.request.Request(url, headers={'User-Agent': 'HackLabs/1.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                raw = response.read().decode('utf-8', errors='replace')[:5000]
                # Pretty-print JSON responses
                try:
                    parsed = _json.loads(raw)
                    content = _json.dumps(parsed, indent=2, ensure_ascii=False)
                except Exception:
                    content = raw
        except Exception as e:
            error = str(e)

    return render_template('labs/ssrf.html', lab=lab, url=url, content=content, error=error)

# ─────────────────────────────────────────────
# XSS – Cross-Site Scripting
# ─────────────────────────────────────────────

@app.route('/xss/reflected')
def xss_reflected():
    lab = next(l for l in get_lab_list() if l['id'] == 'xss')
    q = request.args.get('q', '')
    # VULNERABLE: q se refleja sin sanitizar (ver template con |safe)
    return render_template('labs/xss.html', lab=lab, tab='reflected', query=q)

@app.route('/xss/stored', methods=['GET', 'POST'])
def xss_stored():
    lab = next(l for l in get_lab_list() if l['id'] == 'xss')
    if request.method == 'POST':
        comment = request.form.get('comment', '')
        author = request.form.get('author', 'Anónimo')
        db = get_db()
        # VULNERABLE: se guarda sin sanitizar
        db.execute("INSERT INTO comments (author, body) VALUES (?, ?)", (author, comment))
        db.commit()
        return redirect(url_for('xss_stored'))
    db = get_db()
    comments = db.execute("SELECT * FROM comments ORDER BY id DESC").fetchall()
    return render_template('labs/xss.html', lab=lab, tab='stored', comments=comments)

@app.route('/xss/dom')
def xss_dom():
    lab = next(l for l in get_lab_list() if l['id'] == 'xss')
    return render_template('labs/xss.html', lab=lab, tab='dom')

# ─────────────────────────────────────────────
# CSRF
# ─────────────────────────────────────────────

@app.route('/csrf/profile')
def csrf_profile():
    lab = next(l for l in get_lab_list() if l['id'] == 'csrf')
    user_id = request.args.get('id', '2')
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    return render_template('labs/csrf.html', lab=lab, user=user)

@app.route('/csrf/change-password', methods=['POST'])
def csrf_change_password():
    # VULNERABLE: sin token CSRF, cualquier origen puede enviar este formulario
    user_id = request.form.get('user_id', '')
    new_password = request.form.get('new_password', '')
    if user_id and new_password:
        new_hash = hashlib.md5(new_password.encode()).hexdigest()
        db = get_db()
        db.execute("UPDATE users SET password_md5 = ?, password_plain = ? WHERE id = ?",
                   (new_hash, new_password, user_id))
        db.commit()
        return jsonify({'status': 'ok', 'message': f'Contraseña cambiada para user_id={user_id}', 'new_hash': new_hash})
    return jsonify({'status': 'error', 'message': 'Faltan parámetros'}), 400

# ─────────────────────────────────────────────
# File Upload
# ─────────────────────────────────────────────

@app.route('/upload', methods=['GET', 'POST'])
def file_upload():
    lab = next(l for l in get_lab_list() if l['id'] == 'file_upload')
    message = None
    uploaded_path = None

    if request.method == 'POST':
        f = request.files.get('file')
        if f and f.filename:
            # VULNERABLE: sin validación de tipo, sin rename seguro
            filename = f.filename
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            f.save(save_path)
            uploaded_path = f'/uploads/{filename}'
            message = f'Archivo subido: {filename}'

    uploaded_files = os.listdir(UPLOAD_FOLDER) if os.path.exists(UPLOAD_FOLDER) else []
    return render_template('labs/file_upload.html', lab=lab, message=message,
                           uploaded_path=uploaded_path, uploaded_files=uploaded_files)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # VULNERABLE: sirve cualquier archivo, incluyendo scripts
    return send_file(os.path.join(UPLOAD_FOLDER, filename))

# ─────────────────────────────────────────────
# XXE – XML External Entity
# ─────────────────────────────────────────────

@app.route('/xxe', methods=['GET', 'POST'])
def xxe():
    lab = next(l for l in get_lab_list() if l['id'] == 'xxe')
    result = None
    error = None
    xml_input = request.values.get('xml_data', '')

    if xml_input:
        try:
            # VULNERABLE: parser sin deshabilitar entidades externas
            tree = ET.fromstring(xml_input)
            name = tree.findtext('name', default='(vacío)')
            email = tree.findtext('email', default='(vacío)')
            result = {'name': name, 'email': email}
        except ET.ParseError as e:
            error = f'Error XML: {e}'
        except Exception as e:
            error = str(e)

    return render_template('labs/xxe.html', lab=lab, result=result,
                           error=error, xml_input=xml_input)

# ─────────────────────────────────────────────
# Path Traversal / LFI
# ─────────────────────────────────────────────

@app.route('/files')
def path_traversal():
    lab = next(l for l in get_lab_list() if l['id'] == 'path_traversal')
    filename = request.args.get('file', '')
    content = None
    error = None

    if filename:
        try:
            # VULNERABLE: sin normalización de ruta (permite ../../)
            base_path = os.path.join(os.path.dirname(__file__), 'static', 'files')
            full_path = os.path.join(base_path, filename)
            # No se verifica que full_path esté dentro de base_path
            with open(full_path, 'r', errors='replace') as f:
                content = f.read()
        except FileNotFoundError:
            error = f'Archivo no encontrado: {filename}'
        except PermissionError:
            error = 'Sin permisos para leer el archivo'
        except Exception as e:
            error = str(e)

    return render_template('labs/path_traversal.html', lab=lab, filename=filename,
                           content=content, error=error)

# ─────────────────────────────────────────────
# Bruteforce info lab
# ─────────────────────────────────────────────

@app.route('/bruteforce')
def bruteforce():
    lab = next(l for l in get_lab_list() if l['id'] == 'bruteforce')
    return render_template('labs/bruteforce.html', lab=lab)

@app.route('/bruteforce/login', methods=['GET', 'POST'])
def bruteforce_login():
    username = request.values.get('username', '')
    password = request.values.get('password', '')
    db = get_db()
    pw_hash = hashlib.md5(password.encode()).hexdigest()
    user = db.execute('SELECT * FROM users WHERE username=? AND password_md5=?', (username, pw_hash)).fetchone()
    lab = next(l for l in get_lab_list() if l['id'] == 'bruteforce')
    if user:
        bf_result = f'Login correcto. Bienvenido, {username} (rol: {user["role"]}).'
        return render_template('labs/bruteforce.html', lab=lab, bf_result=bf_result, bf_success=True)
    bf_result = 'Credenciales incorrectas.'
    return render_template('labs/bruteforce.html', lab=lab, bf_result=bf_result, bf_success=False)

@app.route('/bruteforce/ftp', methods=['GET', 'POST'])
def bruteforce_ftp():
    username = request.values.get('username', '')
    password = request.values.get('password', '')
    if not username or not password:
        return 'Login failed.\r\n', 401
    db = get_db()
    pw_hash = hashlib.md5(password.encode()).hexdigest()
    user = db.execute('SELECT * FROM users WHERE username=? AND password_md5=?', (username, pw_hash)).fetchone()
    if user:
        return f'230 Login successful. Welcome {username}.\r\n', 200
    return '530 Login incorrect.\r\n', 401

# ─────────────────────────────────────────────
# API: lista de usuarios (para practicar enumeration)
# VULNERABLE: sin autenticación
# ─────────────────────────────────────────────

@app.route('/api/users')
def api_users():
    db = get_db()
    users = db.execute("SELECT id, username, email, role FROM users").fetchall()
    return jsonify([dict(u) for u in users])

# ─────────────────────────────────────────────
# SSTI – Server-Side Template Injection
# VULNERABLE: render_template_string con input de usuario
# ─────────────────────────────────────────────

@app.route('/ssti', methods=['GET', 'POST'])
def ssti():
    lab = next(l for l in get_lab_list() if l['id'] == 'ssti')
    result = None
    template_input = request.values.get('template', '')
    if template_input:
        try:
            result = render_template_string(template_input)
        except Exception as e:
            result = f'Error: {e}'
    return render_template('labs/ssti.html', lab=lab, result=result, template_input=template_input)

# ─────────────────────────────────────────────
# Open Redirect
# VULNERABLE: redirección sin whitelist
# ─────────────────────────────────────────────

@app.route('/open_redirect')
def open_redirect():
    lab = next(l for l in get_lab_list() if l['id'] == 'open_redirect')
    url = request.args.get('url', '')
    if url:
        return redirect(url)
    return render_template('labs/open_redirect.html', lab=lab)

# ─────────────────────────────────────────────
# JWT Manipulation
# VULNERABLE: acepta alg=none, secreto débil
# ─────────────────────────────────────────────

JWT_SECRET = 'secret123'

def _b64enc(data):
    return base64.urlsafe_b64encode(json.dumps(data, separators=(',',':')).encode()).rstrip(b'=').decode()

def _b64dec(s):
    return json.loads(base64.urlsafe_b64decode(s + '=='))

@app.route('/jwt', methods=['GET', 'POST'])
def jwt_lab():
    lab = next(l for l in get_lab_list() if l['id'] == 'jwt')
    token = decoded = error = None
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'generate':
            username = request.form.get('username', 'guest')
            role = request.form.get('role', 'user')
            header  = _b64enc({'alg': 'HS256', 'typ': 'JWT'})
            payload = _b64enc({'sub': username, 'role': role, 'iat': 1700000000})
            sig_input = f'{header}.{payload}'.encode()
            sig = base64.urlsafe_b64encode(
                _hmac.new(JWT_SECRET.encode(), sig_input, hashlib.sha256).digest()
            ).rstrip(b'=').decode()
            token = f'{header}.{payload}.{sig}'
        elif action == 'verify':
            raw = request.form.get('token', '')
            try:
                parts = raw.split('.')
                h_data = _b64dec(parts[0])
                p_data = _b64dec(parts[1])
                alg = h_data.get('alg', 'HS256')
                if alg.lower() == 'none':
                    decoded = p_data
                    decoded['_vuln'] = 'alg=none accepted — no signature verified!'
                else:
                    sig_input = f'{parts[0]}.{parts[1]}'.encode()
                    expected = base64.urlsafe_b64encode(
                        _hmac.new(JWT_SECRET.encode(), sig_input, hashlib.sha256).digest()
                    ).rstrip(b'=').decode()
                    decoded = p_data if parts[2] == expected else None
                    if not decoded:
                        error = 'Firma inválida.'
            except Exception as e:
                error = str(e)
    return render_template('labs/jwt.html', lab=lab, token=token, decoded=decoded,
                           error=error, secret=JWT_SECRET)

# ─────────────────────────────────────────────
# Insecure Deserialization
# VULNERABLE: pickle.loads con input de usuario
# ─────────────────────────────────────────────

@app.route('/deserialization', methods=['GET', 'POST'])
def deserialization():
    lab = next(l for l in get_lab_list() if l['id'] == 'deserialization')
    result = error = None
    example = base64.b64encode(pickle.dumps({'user': 'admin', 'role': 'admin', 'logged_in': True})).decode()
    data = request.values.get('data', '')
    if data:
        try:
            obj = pickle.loads(base64.b64decode(data))
            result = str(obj)
        except Exception as e:
            error = str(e)
    return render_template('labs/deserialization.html', lab=lab, result=result,
                           error=error, example=example)

# ─────────────────────────────────────────────
# CORS Misconfiguration
# VULNERABLE: Access-Control-Allow-Origin refleja cualquier origen
# ─────────────────────────────────────────────

@app.route('/cors')
def cors_lab():
    lab = next(l for l in get_lab_list() if l['id'] == 'cors')
    return render_template('labs/cors.html', lab=lab)

@app.route('/cors/data')
def cors_data():
    origin = request.headers.get('Origin', '*')
    data = {'secret': 'FLAG{cors_misconfigured_4cc3ss}', 'users': ['admin', 'alice', 'bob'], 'internal': True}
    resp = jsonify(data)
    resp.headers['Access-Control-Allow-Origin'] = origin
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    return resp

# ─────────────────────────────────────────────
# Inicialización
# ─────────────────────────────────────────────

# ─────────────────────────────────────────────
# Account system (platform users, separate from labs)
# ─────────────────────────────────────────────

def ensure_account_table():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS account_users (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        username      TEXT NOT NULL UNIQUE,
        email         TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL
    )''')
    db.commit()

@app.route('/account/register', methods=['GET', 'POST'])
def account_register():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm', '')

        if not username or not email or not password:
            error = 'Todos los campos son obligatorios.'
        elif password != confirm:
            error = 'Las contraseñas no coinciden.'
        elif len(password) < 6:
            error = 'La contraseña debe tener al menos 6 caracteres.'
        else:
            ensure_account_table()
            pw_hash = hashlib.sha256(password.encode()).hexdigest()
            try:
                db = get_db()
                db.execute('INSERT INTO account_users (username, email, password_hash) VALUES (?,?,?)',
                           (username, email, pw_hash))
                db.commit()
                session['app_user']      = username
                session['app_email']     = email
                session['app_user_type'] = 'account'
                return redirect(url_for('index'))
            except sqlite3.IntegrityError:
                error = 'El usuario o email ya existe.'

    return render_template('account/register.html', error=error)


@app.route('/account/login', methods=['GET', 'POST'])
def account_login():
    error = None
    next_url = request.args.get('next', url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        next_url = request.form.get('next', url_for('index'))

        db = get_db()

        # 1) Check platform account_users (SHA-256)
        ensure_account_table()
        pw_sha256 = hashlib.sha256(password.encode()).hexdigest()
        user = db.execute(
            'SELECT * FROM account_users WHERE username=? AND password_hash=?',
            (username, pw_sha256)
        ).fetchone()

        if user:
            session['app_user']      = user['username']
            session['app_email']     = user['email']
            session['app_user_type'] = 'account'
            return redirect(next_url)

        # 2) Fall back to lab users table (MD5)
        pw_md5 = hashlib.md5(password.encode()).hexdigest()
        lab_user = db.execute(
            'SELECT * FROM users WHERE username=? AND password_md5=?',
            (username, pw_md5)
        ).fetchone()

        if lab_user:
            session['app_user']      = lab_user['username']
            session['app_email']     = lab_user['email']
            session['app_user_type'] = 'lab'
            return redirect(next_url)

        error = 'Usuario o contraseña incorrectos.'

    return render_template('account/login.html', error=error, next=next_url)


@app.route('/account/logout')
def account_logout():
    session.pop('app_user', None)
    session.pop('app_email', None)
    return redirect(url_for('index'))


@app.route('/account/profile', methods=['GET', 'POST'])
def account_profile():
    if not session.get('app_user'):
        return redirect(url_for('account_login', next=request.url))

    success = None
    error   = None
    ensure_account_table()
    db = get_db()
    is_lab_user = session.get('app_user_type') == 'lab'

    if is_lab_user:
        # Lab users: show full personal data, no password change allowed
        user = db.execute('SELECT * FROM users WHERE username=?',
                          (session['app_user'],)).fetchone()
        if request.method == 'POST':
            error = 'Las contraseñas de los usuarios del sistema no se pueden cambiar.'
        return render_template('account/profile.html', user=user,
                               success=success, error=error, is_lab_user=True)

    # Platform account users
    user = db.execute('SELECT * FROM account_users WHERE username=?',
                      (session['app_user'],)).fetchone()

    if request.method == 'POST':
        new_username = request.form.get('username', '').strip()
        new_email    = request.form.get('email', '').strip()
        new_password = request.form.get('password', '')
        confirm      = request.form.get('confirm', '')

        if not new_username or not new_email:
            error = 'El usuario y email son obligatorios.'
        elif new_password and new_password != confirm:
            error = 'Las contraseñas no coinciden.'
        elif new_password and len(new_password) < 6:
            error = 'La contraseña debe tener al menos 6 caracteres.'
        else:
            try:
                if new_password:
                    pw_hash = hashlib.sha256(new_password.encode()).hexdigest()
                    db.execute('UPDATE account_users SET username=?, email=?, password_hash=? WHERE username=?',
                               (new_username, new_email, pw_hash, session['app_user']))
                else:
                    db.execute('UPDATE account_users SET username=?, email=? WHERE username=?',
                               (new_username, new_email, session['app_user']))
                db.commit()
                session['app_user']  = new_username
                session['app_email'] = new_email
                success = 'Perfil actualizado correctamente.'
                user = db.execute('SELECT * FROM account_users WHERE username=?',
                                  (new_username,)).fetchone()
            except sqlite3.IntegrityError:
                error = 'El usuario o email ya está en uso.'

    return render_template('account/profile.html', user=user, success=success,
                           error=error, is_lab_user=False)


# ─────────────────────────────────────────────
# Servicios simulados reales: FTP / SSH / SMB
# Escaneables con nmap; FTP es bruteforceable con hydra -M ftp
# ─────────────────────────────────────────────

def _ftp_auth(username, password):
    pw_hash = hashlib.md5(password.encode()).hexdigest()
    con = sqlite3.connect(DATABASE)
    try:
        row = con.execute('SELECT 1 FROM users WHERE username=? AND password_md5=?',
                          (username, pw_hash)).fetchone()
        return row is not None
    finally:
        con.close()

def _handle_ftp_client(conn, addr):
    try:
        conn.sendall(b'220 HackLabs FTP Server ready (vsFTPd 3.0.5)\r\n')
        username = None
        while True:
            try:
                data = conn.recv(1024)
            except Exception:
                break
            if not data:
                break
            cmd = data.decode('utf-8', errors='ignore').strip()
            up = cmd.upper()
            if up.startswith('USER '):
                username = cmd[5:].strip()
                conn.sendall(b'331 Please specify the password.\r\n')
            elif up.startswith('PASS ') and username:
                password = cmd[5:].strip()
                if _ftp_auth(username, password):
                    conn.sendall(b'230 Login successful.\r\n')
                else:
                    conn.sendall(b'530 Login incorrect.\r\n')
                    username = None
            elif up.startswith('PASS '):
                conn.sendall(b'503 Login with USER first.\r\n')
            elif up == 'QUIT':
                conn.sendall(b'221 Goodbye.\r\n')
                break
            elif up == 'SYST':
                conn.sendall(b'215 UNIX Type: L8\r\n')
            elif up.startswith('FEAT'):
                conn.sendall(b'211-Features:\r\n211 End\r\n')
            elif up.startswith(('OPTS', 'TYPE', 'MODE')):
                conn.sendall(b'200 OK\r\n')
            else:
                conn.sendall(b'530 Please login with USER and PASS.\r\n')
    except Exception:
        pass
    finally:
        conn.close()

def _handle_ssh_client(conn, addr):
    """Sends real SSH banner — nmap -sV identifies it as OpenSSH."""
    try:
        conn.sendall(b'SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.6\r\n')
        conn.recv(256)
    except Exception:
        pass
    finally:
        conn.close()

def _handle_smb_client(conn, addr):
    """Responds to SMB negotiate probe — nmap -sV identifies it as SMB/CIFS."""
    _SMB_RESP = (
        b'\x00\x00\x00\x31'          # NetBIOS session (length 49)
        b'\xffSMB'                    # SMB magic
        b'\x72'                        # SMB_COM_NEGOTIATE
        b'\x00\x00\x00\x00'          # Status OK
        b'\x88\x01\xc8\x00'          # Flags / Flags2
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # Signature + reserved
        b'\xff\xff\x00\x00\x00\x00\x00\x00'           # TID PID UID MID
        b'\x01\x00\x00'               # WordCount=1, DialectIndex=0
        b'\x00\x00'                   # ByteCount=0
    )
    try:
        conn.recv(256)
        conn.sendall(_SMB_RESP)
        conn.recv(256)
    except Exception:
        pass
    finally:
        conn.close()

def _tcp_service(port, handler, name):
    try:
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(('0.0.0.0', port))
        srv.listen(20)
        print(f'[+] Servicio {name} escuchando en :{port}')
        while True:
            try:
                conn, addr = srv.accept()
                threading.Thread(target=handler, args=(conn, addr), daemon=True).start()
            except Exception:
                pass
    except PermissionError:
        print(f'[!] {name}:{port} — permiso denegado (requiere root/admin o Docker)')
    except OSError as e:
        print(f'[!] {name}:{port} — no disponible: {e}')

def start_simulated_services():
    for port, handler, name in [
        (21,  _handle_ftp_client, 'FTP'),
        (22,  _handle_ssh_client, 'SSH'),
        (445, _handle_smb_client, 'SMB'),
    ]:
        threading.Thread(target=_tcp_service, args=(port, handler, name), daemon=True).start()


if __name__ == '__main__':
    # ── ANSI colors ──────────────────────────────────────
    R  = '\033[0;31m'   # red
    G  = '\033[0;32m'   # green
    Y  = '\033[1;33m'   # yellow
    C  = '\033[0;36m'   # cyan
    B  = '\033[1m'      # bold
    D  = '\033[2m'      # dim
    NC = '\033[0m'      # reset

    # ── Init ─────────────────────────────────────────────
    if not os.path.exists(DATABASE):
        print(f"{Y}[*] Inicializando base de datos...{NC}")
        init_db()
        print(f"{G}[+] Base de datos lista.{NC}")
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), 'logs'), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), 'static', 'files'), exist_ok=True)

    _port = int(os.environ.get('APP_PORT', 5000))

    # En local (puerto 5000) mostrar localhost; en Docker (puerto 80) detectar IP real
    if _port == 5000:
        _ip = '127.0.0.1'
    else:
        try:
            _sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            _sock.connect(('8.8.8.8', 80))
            _ip = _sock.getsockname()[0]
            _sock.close()
        except Exception:
            _ip = '127.0.0.1'

    start_simulated_services()

    # ── Banner ───────────────────────────────────────────
    print()
    print(f"{R}    __  __              __    __           __         {NC}")
    print(f"{R}   / / / /____ _ _____ / /__ / /   ____ _ / /_   _____{NC}")
    print(f"{R}  / /_/ // __ `// ___// //_// /   / __ `// __ \\ / ___/{NC}")
    print(f"{R} / __  // /_/ // /__ / ,<  / /___/ /_/ // /_/ /(__  ) {NC}")
    print(f"{R}/_/ /_/ \\__,_/ \\___//_/|_|/_____/\\__,_//_.___//____/  {NC}")
    print()
    print(f"  {G}════════════════════════════════════════════════════{NC}")
    print(f"  {B}{G}  ✓  Laboratorio iniciado correctamente{NC}")
    print(f"  {G}════════════════════════════════════════════════════{NC}")
    print()
    _url = f"http://{_ip}" if _port == 80 else f"http://{_ip}:{_port}"
    print(f"  {C}{B}  IP del servidor:   {_ip}{NC}")
    print()
    print(f"  {D}  HTTP  →  {_url}{NC}")
    print(f"  {D}  FTP   →  ftp://{_ip}  (puerto 21){NC}")
    print(f"  {D}  SSH   →  ssh user@{_ip}  (puerto 22){NC}")
    print(f"  {D}  SMB   →  //{_ip}/  (puerto 445){NC}")
    print()
    print(f"  {D}  nmap -sV -p 21,22,80,445 {_ip}{NC}")
    print()
    print(f"  {G}════════════════════════════════════════════════════{NC}")
    print()
    print(f"  {Y}  ⚠  Solo usar en entornos aislados / laboratorio{NC}")
    print(f"  {Y}  Presiona Ctrl+C para detener HackLabs{NC}")
    print()

    app.run(host='0.0.0.0', port=_port, debug=True, use_reloader=False)
