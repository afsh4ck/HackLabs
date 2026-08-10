#!/usr/bin/env python3
"""HackLabs – ajustes de bajo nivel sobre la base de datos del dominio.

Aplica las debilidades que `samba-tool` no expone directamente
(userAccountControl, delegación restringida, atributos con flags) y
escribe por stdout las variables de shell (DN_* y SID_*) que
`provision.sh` necesita para delegar las ACLs abusables.
"""

import ldb
from samba.auth import system_session
from samba.param import LoadParm
from samba.samdb import SamDB

SMB_CONF = '/etc/samba/smb.conf'

# userAccountControl
NORMAL_ACCOUNT = 0x0200            # 512
DONT_EXPIRE_PASSWORD = 0x10000     # 65536
DONT_REQUIRE_PREAUTH = 0x400000    # 4194304   → AS-REP Roasting
TRUSTED_TO_AUTH_FOR_DELEGATION = 0x1000000   # 16777216 → transición de protocolo

lp = LoadParm()
lp.load(SMB_CONF)
samdb = SamDB(session_info=system_session(), lp=lp)
base_dn = samdb.domain_dn()


def _entry(sam_account_name, attrs):
    res = samdb.search(base=base_dn, scope=ldb.SCOPE_SUBTREE,
                       expression='(sAMAccountName=%s)' % sam_account_name,
                       attrs=attrs)
    if not res:
        raise SystemExit('objeto no encontrado en el dominio: %s' % sam_account_name)
    return res[0]


def dn_of(sam_account_name):
    return str(_entry(sam_account_name, ['distinguishedName']).dn)


def sid_of(sam_account_name):
    entry = _entry(sam_account_name, ['objectSid'])
    return samdb.schema_format_value('objectSid', entry['objectSid'][0]).decode('utf-8')


def set_attrs(sam_account_name, values):
    entry = _entry(sam_account_name, ['distinguishedName'])
    msg = ldb.Message()
    msg.dn = entry.dn
    for name, value in values.items():
        msg[name] = ldb.MessageElement(str(value), ldb.FLAG_MOD_REPLACE, name)
    samdb.modify(msg)


# ── 1. svc.backup sin pre-autenticación Kerberos → AS-REP Roasting ──
set_attrs('svc.backup', {
    'userAccountControl': NORMAL_ACCOUNT | DONT_EXPIRE_PASSWORD | DONT_REQUIRE_PREAUTH,
})

# ── 2. svc.delegate con delegación restringida + transición de protocolo ──
realm = samdb.domain_dns_name()
set_attrs('svc.delegate', {
    'userAccountControl': NORMAL_ACCOUNT | DONT_EXPIRE_PASSWORD | TRUSTED_TO_AUTH_FOR_DELEGATION,
    'msDS-AllowedToDelegateTo': 'cifs/dc01.%s' % realm,
})

# ── 3. Credencial filtrada en el atributo description (LDAP enum) ──
set_attrs('t.rodriguez', {
    'description': 'Cuenta temporal creada por Helpdesk. Password inicial: '
                   'Welcome2024! - HL{4d_ld4p_d35cr1p710n_l34k}',
})

# ── 4. Flag del camino de ataque, en las notas del grupo anidado ──
set_attrs('TIER0-LEGACY', {
    'info': 'Grupo heredado con pertenencia a Domain Admins. '
            'Pendiente de retirada. HL{4d_bl00dh0und_p47h_70_d4}',
})

# ── 5. Variables de shell para provision.sh ────────────────────────
exports = {
    'DN_BASE': base_dn,
    'DN_M_DAVIS': dn_of('m.davis'),
    'DN_IT_SUPPORT': dn_of('IT Support'),
    'SID_SVC_READONLY': sid_of('svc.readonly'),
    'SID_IT_SUPPORT': sid_of('IT Support'),
}
for key, value in exports.items():
    print("%s='%s'" % (key, value.replace("'", "'\\''")))
