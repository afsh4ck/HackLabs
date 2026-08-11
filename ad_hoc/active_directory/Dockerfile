# ──────────────────────────────────────────────────────────────────
# HackLabs – Domain Controller vulnerable (Samba AD DC)
#
# Levanta un dominio Active Directory REAL (Kerberos KDC, LDAP, SMB,
# SYSVOL y DNS) preparado con 15 configuraciones inseguras, una por
# cada laboratorio de la categoría "Active Directory".
#
# ⚠ Solo para entornos aislados de laboratorio.
# ──────────────────────────────────────────────────────────────────
FROM debian:bookworm-slim

LABEL maintainer="afsh4ck" \
      description="HackLabs – Vulnerable Active Directory Domain Controller" \
      version="1.0"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        samba \
        samba-common-bin \
        samba-dsdb-modules \
        samba-vfs-modules \
        samba-ad-provision \
        winbind \
        libnss-winbind \
        krb5-user \
        krb5-config \
        ldb-tools \
        ldap-utils \
        smbclient \
        python3 \
        python3-samba \
        procps \
        iproute2 \
        iputils-ping \
        dnsutils \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Samba se arranca desde el entrypoint, nunca por systemd
RUN rm -f /etc/samba/smb.conf

# DNS · Kerberos · LDAP/LDAPS · SMB · kpasswd · GC · RPC endpoint mapper + dinámicos
EXPOSE 53/tcp 53/udp 88/tcp 88/udp 135/tcp 137/udp 138/udp 139/tcp \
       389/tcp 389/udp 445/tcp 464/tcp 464/udp 636/tcp 3268/tcp 3269/tcp \
       49152-49200/tcp

ENV AD_REALM=HACKLABS.LOCAL \
    AD_DOMAIN=HACKLABS \
    AD_DC_HOSTNAME=DC01 \
    AD_ADMIN_PASSWORD='Adm1nP@ss2024!' \
    AD_DNS_FORWARDER=1.1.1.1

COPY provision.sh /provision.sh
COPY seed_domain.py /seed_domain.py
COPY verify_ticket.py /verify_ticket.py
COPY bloodhound_simple_bind.py /bloodhound_simple_bind.py
COPY getTGT_fixed.py /getTGT_fixed.py
COPY GetUserSPNs_fixed.py /GetUserSPNs_fixed.py
COPY smbclient_fixed.py /smbclient_fixed.py
COPY entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /provision.sh /entrypoint.sh /seed_domain.py /verify_ticket.py /bloodhound_simple_bind.py /getTGT_fixed.py /GetUserSPNs_fixed.py /smbclient_fixed.py \
    && chmod +x /provision.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
