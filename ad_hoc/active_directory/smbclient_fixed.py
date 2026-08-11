#!/usr/bin/env python3
"""Wrapper de impacket-smbclient que corrige el bug real de checksum de
impacket en el TGS-REQ (ver GetUserSPNs_fixed.py / guía de AD 05 para el
detalle completo): getKerberosTGS() nunca manda el checksum keyed que
RFC 4120 S5.5.1 exige en el Authenticator (key usage 6, sobre la
codificación "pelada" de KDC-REQ-BODY), y el KDC de Samba lo exige de
verdad -- sin él responde KRB_AP_ERR_INAPP_CKSUM. Con el checksum
añadido, smbclient -k consigue una sesión SMB real vía Kerberos.

Uso: igual que impacket-smbclient, solo cambia el nombre del comando.
  KRB5CCNAME=usuario.ccache python3 smbclient_fixed.py -k -no-pass dc01.hacklabs.local -dc-ip <IP>
"""
import datetime
import sys

from pyasn1.codec.der import encoder, decoder
from pyasn1.type.univ import noValue
from Cryptodome.Random import random as rand

import impacket.krb5.kerberosv5 as _k5
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


def _getKerberosTGS_fixed(serverName, domain, kdcHost, tgt, cipher, sessionKey, renew=False):
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

    res = decoder.decode(r, asn1Spec=TGS_REP())[0]
    spn = Principal()
    spn.from_asn1(res['ticket'], 'realm', 'sname')
    if spn.components[0] == serverName.components[0]:
        return r, newCipher, sessionKey, newSessionKey
    else:
        domain = spn.components[1]
        return _getKerberosTGS_fixed(serverName, domain, kdcHost, r, newCipher, newSessionKey)


# Parchea tanto el nombre del módulo (para "from impacket.krb5.kerberosv5
# import getKerberosTGS" que se ejecute DESPUÉS de este punto) como
# cualquier referencia ya importada localmente en otros módulos ya cargados.
_k5.getKerberosTGS = _getKerberosTGS_fixed

import runpy
real_script = '/usr/share/doc/python3-impacket/examples/smbclient.py'
sys.argv[0] = real_script
runpy.run_path(real_script, run_name='__main__')
