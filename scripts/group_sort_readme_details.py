import re
from pathlib import Path

p = Path('README.md')
s = p.read_text(encoding='utf-8')
lines = s.splitlines()

# find start of section
start_idx = None
for i,l in enumerate(lines):
    if l.strip() == '### Detalle por laboratorio':
        start_idx = i
        break
if start_idx is None:
    raise SystemExit('Start marker not found')

# find index of next major section after start
end_section_idx = None
for i in range(start_idx+1, len(lines)):
    if lines[i].startswith('## '):
        end_section_idx = i
        break
if end_section_idx is None:
    raise SystemExit('End marker not found')

section_lines = lines[start_idx+1:end_section_idx]

# extract top-level <details>...</details> blocks using depth stack
blocks = []
stack = []
block_start = None
for idx, line in enumerate(section_lines):
    if '<details>' in line:
        if not stack:
            block_start = idx
        stack.append(idx)
    if '</details>' in line and stack:
        stack.pop()
        if not stack and block_start is not None:
            block_end = idx
            block = '\n'.join(section_lines[block_start:block_end+1])
            blocks.append(block)
            block_start = None

if not blocks:
    raise SystemExit('No blocks found')

# helper to extract summary text
def get_summary(block):
    m = re.search(r'<summary>(.*?)</summary>', block, re.S | re.I)
    if not m:
        return ''
    txt = m.group(1)
    # strip tags
    txt = re.sub(r'<.*?>', '', txt)
    return txt.strip()

# classify blocks
owasp = []
vulns = []
ia = []
others = []

for b in blocks:
    s = get_summary(b)
    key = s
    # OWASP labs start with A## or A0#
    if re.match(r'^A\d{2}\b', s):
        owasp.append((s, b))
    elif any(k in s.lower() for k in ['prompt injection','ai jailbreak','indirect prompt injection','ai jailbreak','indirect prompt']):
        ia.append((s, b))
    else:
        # consider vulnerability group: common names like CORS, CSRF, File Upload, XXE, XSS, JWT, SSTI, Path Traversal, Insecure Deserialization, Login Bruteforce, Open Redirect, Privilege Escalation, C2, etc.
        vulns.append((s, b))

# sort each group alphabetically by summary
owasp_sorted = [b for s,b in sorted(owasp, key=lambda x: x[0].lower())]
vulns_sorted = [b for s,b in sorted(vulns, key=lambda x: x[0].lower())]
ia_sorted = [b for s,b in sorted(ia, key=lambda x: x[0].lower())]

# reconstruct section: header + OWASP + vuln + IA
new_section = ['### Detalle por laboratorio', '']
for grp in (owasp_sorted, vulns_sorted, ia_sorted):
    for b in grp:
        new_section.append(b)
        new_section.append('')
new_section_str = '\n'.join(new_section).rstrip() + '\n'

# write new file content
new_lines = lines[:start_idx] + new_section_str.splitlines() + lines[end_section_idx:]

p.write_text('\n'.join(new_lines), encoding='utf-8')
print('Reordered groups: OWASP', len(owasp_sorted), 'Vulns', len(vulns_sorted), 'IA', len(ia_sorted))
