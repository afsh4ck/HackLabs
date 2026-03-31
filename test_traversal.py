import urllib.request, urllib.parse

BASE = 'http://127.0.0.1:5000'

paths = [
    '../database/schema.sql',
    '..\\database\\schema.sql',
    '../database/schema.sql',
]

for path in paths:
    url = BASE + '/files?file=' + urllib.parse.quote(path)
    try:
        with urllib.request.urlopen(url, timeout=4) as r:
            body = r.read().decode()
            found = 'CREATE TABLE' in body or 'schema' in body.lower()
            print(repr(path), '->', 'FOUND' if found else 'page ok but no content')
    except Exception as e:
        print(repr(path), '-> ERROR:', str(e))
