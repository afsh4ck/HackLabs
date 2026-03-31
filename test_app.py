import urllib.request, urllib.parse, json

BASE = 'http://127.0.0.1:5000'
ok = []
fail = []

def check(label, url, method='GET', data=None, expect_in=None, expect_status=200):
    try:
        if data:
            body = urllib.parse.urlencode(data).encode()
            req = urllib.request.Request(url, data=body, method=method)
            req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        else:
            req = urllib.request.Request(url, method=method)
        req.add_header('User-Agent', 'HackLabs-Test/1.0')
        opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler())
        with opener.open(req, timeout=5) as r:
            status = r.status
            body_text = r.read().decode('utf-8', errors='replace')
    except urllib.error.HTTPError as e:
        status = e.code
        body_text = e.read().decode('utf-8', errors='replace')
    except Exception as e:
        fail.append('  FAIL  ' + label + ': ' + str(e))
        return

    passed = (status == expect_status)
    if expect_in and passed:
        passed = (expect_in in body_text)
    tag = 'PASS' if passed else 'FAIL'
    (ok if passed else fail).append('  ' + tag + '  [' + str(status) + '] ' + label)

# ── /lab/* redirects ──────────────────────────────────
check('GET /lab/idor',            BASE + '/lab/idor',            expect_in='Broken Access Control')
check('GET /lab/sqli',            BASE + '/lab/sqli',            expect_in='SQL Injection')
check('GET /lab/cmdi',            BASE + '/lab/cmdi',            expect_in='Command Injection')
check('GET /lab/crypto',          BASE + '/lab/crypto',          expect_in='Cryptographic')
check('GET /lab/insecure_design', BASE + '/lab/insecure_design', expect_in='mascota')
check('GET /lab/misconfig',       BASE + '/lab/misconfig',       expect_in='admin123')
check('GET /lab/outdated',        BASE + '/lab/outdated',        expect_in='jQuery')
check('GET /lab/auth_failures',   BASE + '/lab/auth_failures',   expect_in='Login')
check('GET /lab/integrity',       BASE + '/lab/integrity',       expect_in='alice')
check('GET /lab/logging',         BASE + '/lab/logging',         expect_in='logging')
check('GET /lab/ssrf',            BASE + '/lab/ssrf',            expect_in='SSRF')
check('GET /lab/xss',             BASE + '/lab/xss',             expect_in='XSS')
check('GET /lab/csrf',            BASE + '/lab/csrf',            expect_in='CSRF')
check('GET /lab/file_upload',     BASE + '/lab/file_upload',     expect_in='Upload')
check('GET /lab/xxe',             BASE + '/lab/xxe',             expect_in='XXE')
check('GET /lab/path_traversal',  BASE + '/lab/path_traversal',  expect_in='Traversal')
check('GET /lab/bruteforce',      BASE + '/lab/bruteforce',      expect_in='Hydra')

# ── A01 IDOR ──────────────────────────────────────────
check('IDOR id=1 (admin)',        BASE + '/profile?id=1',        expect_in='admin')
check('IDOR id=2 (alice)',        BASE + '/profile?id=2',        expect_in='alice')

# ── A03 SQLi ─────────────────────────────────────────
q_union = "' UNION SELECT 1,username,password_plain,4,5 FROM users--"
check('SQLi UNION dump users',    BASE + '/sqli/search?q=' + urllib.parse.quote(q_union), expect_in='admin123')

q_all = "' OR '1'='1"
check('SQLi OR 1=1 all rows',     BASE + '/sqli/search?q=' + urllib.parse.quote(q_all),   expect_in='Kali')

# ── A07 Auth Failures ────────────────────────────────
check('Login admin OK',           BASE + '/login', method='POST',
      data={'username': 'admin', 'password': 'admin123'}, expect_in='Bienvenido')
check('Login wrong creds',        BASE + '/login', method='POST',
      data={'username': 'admin', 'password': 'wrong'},    expect_in='incorrectas')

# ── A02 Crypto ───────────────────────────────────────
check('Crypto login OK (MD5)',    BASE + '/crypto/login', method='POST',
      data={'username': 'alice', 'password': 'password'}, expect_in='5f4dcc3b')

# ── A05 Misconfig ────────────────────────────────────
check('Admin panel sin auth',     BASE + '/admin',       expect_in='admin123')
check('/.git/config expuesto',    BASE + '/.git/config', expect_in='remote')
check('API /api/users sin auth',  BASE + '/api/users',   expect_in='alice')

# ── A08 Integrity PUT ────────────────────────────────
try:
    req = urllib.request.Request(BASE + '/api/user/3', method='PUT',
          data=json.dumps({'role': 'admin'}).encode())
    req.add_header('Content-Type', 'application/json')
    with urllib.request.urlopen(req, timeout=5) as r:
        body = r.read().decode()
    tag = 'PASS' if 'admin' in body else 'FAIL'
    (ok if tag == 'PASS' else fail).append('  ' + tag + '  [200] PUT /api/user/3 escalada a admin')
except Exception as e:
    fail.append('  FAIL  PUT /api/user/3: ' + str(e))

# ── Path Traversal ───────────────────────────────────
check('Path traversal readme.txt',     BASE + '/files?file=readme.txt', expect_in='HackLabs')
check('Path traversal schema.sql',     BASE + '/files?file=' + urllib.parse.quote('../../database/schema.sql'), expect_in='CREATE TABLE')

# ── SSRF ─────────────────────────────────────────────
ssrf_target = urllib.parse.quote('http://127.0.0.1:5000/api/users')
check('SSRF fetch recurso interno',    BASE + '/ssrf?url=' + ssrf_target, expect_in='alice')

# ── XSS Reflected ────────────────────────────────────
xss_payload = urllib.parse.quote('<b>xss-test</b>')
check('XSS reflected tag in output',   BASE + '/xss/reflected?q=' + xss_payload, expect_in='<b>xss-test</b>')

# ── CSRF ─────────────────────────────────────────────
check('CSRF change-password (no token)', BASE + '/csrf/change-password', method='POST',
      data={'user_id': '3', 'new_password': 'hacked123'}, expect_in='ok')

# ── A04 Insecure Design ──────────────────────────────
check('Recover step1 user exists',   BASE + '/recover', method='POST',
      data={'username': 'admin'}, expect_in='mascota')
check('Recover answer correct',      BASE + '/recover/answer', method='POST',
      data={'username': 'admin', 'answer': 'rex'}, expect_in='admin123')
check('Recover wrong answer',        BASE + '/recover/answer', method='POST',
      data={'username': 'admin', 'answer': 'wronganswer'}, expect_in='incorrecta')

# ── XSS Stored ───────────────────────────────────────
check('XSS stored page loads',       BASE + '/xss/stored', expect_in='HackLabs')

# ── XXE ──────────────────────────────────────────────
check('XXE normal XML parsed',       BASE + '/xxe', method='POST',
      data={'xml_data': '<user><name>TestUser</name><email>t@t.com</email></user>'},
      expect_in='TestUser')

# ── CMDi page ────────────────────────────────────────
check('CMDi page loads',             BASE + '/cmdi/ping', expect_in='Command Injection')

# ── print results ────────────────────────────────────
total = len(ok) + len(fail)
print()
print('=' * 56)
print('  RESULTADOS: ' + str(len(ok)) + ' PASS  /  ' + str(len(fail)) + ' FAIL  (total=' + str(total) + ')')
print('=' * 56)
for l in ok:
    print(l)
if fail:
    print()
    print('  --- FALLOS ---')
    for l in fail:
        print(l)
print()
