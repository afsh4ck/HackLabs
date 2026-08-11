#!/usr/bin/env python3
"""Wrapper de impacket-getTGT que corrige un bug real de impacket.

CCache.fromTGT() no comprueba hasValue() en encASRepPart['starttime']
antes de convertirlo a texto (a diferencia de 'renew-till', que sí lo
hace dos líneas más abajo en el propio impacket/krb5/ccache.py). El
campo 'starttime' es OPCIONAL según RFC 4120 §5.4.2 y Samba lo omite
en el AS-REP; Windows AD casi siempre lo incluye, por eso el bug pasa
desapercibido contra un DC real. Sin este parche, impacket-getTGT
revienta con: Attempted "__str__" operation on ASN.1 schema object
(confirmado también en impacket 0.13.1 de PyPI, no es solo un
problema de empaquetado de Kali).

Uso: igual que impacket-getTGT, solo cambia el nombre del comando.
  python3 getTGT_fixed.py 'DOMINIO/usuario' -hashes ":$NT_HASH" -dc-ip <IP>
"""
import glob
import os
import runpy
import sys

import impacket.krb5.types as k5types

_last_valid_time = {}
_orig_from_asn1 = k5types.KerberosTime.__dict__['from_asn1'].__func__

def _patched_from_asn1(data):
    if not data.hasValue():
        if 'last' in _last_valid_time:
            return _last_valid_time['last']
        raise ValueError("Campo KerberosTime ausente sin valor de respaldo")
    result = _orig_from_asn1(data)
    _last_valid_time['last'] = result
    return result

k5types.KerberosTime.from_asn1 = staticmethod(_patched_from_asn1)

_candidates = [
    '/usr/share/doc/python3-impacket/examples/getTGT.py',  # Kali (impacket-scripts)
] + glob.glob(os.path.join(os.path.dirname(os.path.dirname(k5types.__file__)), '..', 'examples', 'getTGT.py')) \
  + glob.glob(sys.prefix + '/bin/getTGT.py')  # pip install impacket (venv)

real_script = next((p for p in _candidates if os.path.isfile(p)), None)
if real_script is None:
    sys.exit("No se encontró getTGT.py — instala impacket-scripts (Kali) o 'pip install impacket'.")

sys.argv[0] = real_script
runpy.run_path(real_script, run_name='__main__')
