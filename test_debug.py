import urllib.request
BASE = 'http://127.0.0.1:5000'
opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler())
req = urllib.request.Request(BASE + '/lab/file_upload')
with opener.open(req, timeout=5) as r:
    body = r.read().decode()
    print('has Subir:', 'Subir' in body)
    print('has Upload:', 'Upload' in body)
    print('has file_upload:', 'file_upload' in body)
    idx = body.find('Subir archivo')
    print('subir idx:', idx)
    idx2 = body.find('Upload')
    print('Upload idx:', idx2)
    print('snippet:', body[500:700])
