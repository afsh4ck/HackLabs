#!/usr/bin/env python3
"""Descifra un ticket .ccache forjado con impacket-ticketer y comprueba su identidad,
sin necesidad de que el KDC/servicio lo valide en vivo. Si la verificación es correcta,
imprime la flag del lab (AD12 Silver Ticket o AD13 Golden Ticket, según el SPN del
ticket) -- solo se puede llegar a este punto si el descifrado tiene éxito, lo cual
exige conocer de verdad el hash NT correcto, así que leer este script no basta para
obtener la flag sin haber completado el ataque."""
import sys
from impacket.krb5.ccache import CCache
from impacket.krb5.crypto import Key, _enctype_table
from impacket.krb5.asn1 import EncTicketPart
from impacket.krb5 import types
from pyasn1.codec.der import decoder

FLAGS = {
    'silver': 'HL{4d_51lv3r_71ck37_f0r93d}',
    'golden': 'HL{4d_90ld3n_71ck37_d0m41n_0wn3d}',
}

def verify(ccache_path, nthash_hex, expect_user):
    ccache = CCache.loadFile(ccache_path)
    creds = ccache.credentials[0]
    ticket = types.Ticket()
    ticket.from_asn1(creds.ticket['data'])
    from impacket.krb5.asn1 import Ticket as TicketASN1
    tkt_asn1 = TicketASN1()
    ticket.to_asn1(tkt_asn1)
    sname = '/'.join(str(c) for c in tkt_asn1['sname']['name-string'])
    enctype = int(tkt_asn1['enc-part']['etype'])
    cipher = _enctype_table[enctype]
    key = Key(enctype, bytes.fromhex(nthash_hex))
    plain = cipher.decrypt(key, 2, bytes(tkt_asn1['enc-part']['cipher']))
    encTicketPart = decoder.decode(plain, asn1Spec=EncTicketPart())[0]
    cname = '/'.join(str(c) for c in encTicketPart['cname']['name-string'])
    print('Ticket descifrado correctamente con la clave proporcionada.')
    print('Identidad reclamada (cname):', cname)
    print('Servicio (sname):', sname)
    print('Realm:', str(encTicketPart['crealm']))
    if cname.lower() != expect_user.lower():
        print('La identidad no coincide con la esperada.')
        return False

    print('OK: la clave descifra el ticket y confirma la identidad forjada.')
    ticket_kind = 'golden' if sname.split('/')[0].lower() == 'krbtgt' else 'silver'
    print('Tipo de ticket detectado (por el SPN):', 'Golden Ticket' if ticket_kind == 'golden' else 'Silver Ticket')
    print('Flag:', FLAGS[ticket_kind])
    return True

if __name__ == '__main__':
    ok = verify(sys.argv[1], sys.argv[2], sys.argv[3])
    sys.exit(0 if ok else 1)
