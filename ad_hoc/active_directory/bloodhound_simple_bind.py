#!/usr/bin/env python3
"""Wrapper de bloodhound-ce-python que fuerza bind LDAP SIMPLE en vez de NTLM/Kerberos.

Contra este Domain Controller (Samba AD DC), el bind NTLM de ldap3 (Sicily)
nunca completa (LDAPSessionTerminatedByServerError) y el bind Kerberos falla
por un bug real de Samba al firmar el PAC del ticket de servicio ldap/dc01
(KRB_AP_ERR_INAPP_CKSUM) -- verificado que ocurre dentro del propio KDC, no
en el cliente. El bind LDAP simple (usuario+contraseña en claro) SI funciona
de forma fiable contra este DC, igual que ya usan ldapsearch, bloodyAD y
certipy-ad -ldap-simple-auth en el resto de labs de esta categoria.

Con -c DCOnly el colector solo necesita LDAP (no toca SMB en member hosts),
así que forzar SIMPLE basta para una recolección completa y real, en el
formato OpenGraph que espera BloodHound CE.

Requiere el paquete 'bloodhound-ce' (no el 'bloodhound.py' legacy de apt):
  python3 -m venv ~/bhce-venv && ~/bhce-venv/bin/pip install bloodhound-ce

Uso: igual que bloodhound-ce-python, solo cambia el nombre del comando.
  ~/bhce-venv/bin/python bloodhound_simple_bind.py -d hacklabs.local \
    -u svc.readonly -p 'ReadOnly123!' -ns <IP_DC> -dc dc01.hacklabs.local \
    -c DCOnly --zip
"""
import ssl
import sys
from ldap3 import Server, Connection, ALL, SIMPLE, Tls

import bloodhound.ad.authentication as bh_auth


def _simple_bind_getLDAPConnection(self, hostname='', ip='', baseDN='', protocol='ldaps', gc=False):
    if gc:
        port = 3269 if protocol == 'ldaps' else 3268
    else:
        port = 636 if protocol == 'ldaps' else 389

    if protocol == 'ldaps':
        tls = Tls(validate=ssl.CERT_NONE)
        server = Server("ldaps://%s:%d" % (ip, port), use_ssl=True, get_info=ALL, tls=tls)
    else:
        server = Server("ldap://%s:%d" % (ip, port), get_info=ALL)

    userupn = '%s@%s' % (self.username, self.domain)
    conn = Connection(server, user=userupn, password=self.password,
                       authentication=SIMPLE, auto_referrals=False,
                       receive_timeout=60, auto_range=True)
    bound = conn.bind()
    if not bound:
        raise bh_auth.CollectionException('Could not authenticate to LDAP with simple bind: %s' % conn.result)
    return conn


bh_auth.ADAuthentication.getLDAPConnection = _simple_bind_getLDAPConnection

from bloodhound import main  # noqa: E402
sys.exit(main())
