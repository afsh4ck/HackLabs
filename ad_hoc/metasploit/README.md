# Metasploit target: ActiveMQ 5.18.2

This isolated target is intentionally vulnerable to CVE-2023-46604.

```bash
bash build.sh
bash build.sh status
```

OpenWire is exposed on TCP/61616 and the ActiveMQ console on TCP/8161. Use
`exploit/multi/misc/apache_activemq_rce_cve_2023_46604` with target `1` and
`cmd/linux/http/x64/meterpreter/reverse_tcp`. `LHOST` and `SRVHOST` must be an
address the target container can reach.

Stop and remove the target when finished:

```bash
bash build.sh down
```

Do not publish either port on an Internet-facing host.
