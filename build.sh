#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE=(docker compose -f "$SCRIPT_DIR/docker-compose.yml" -f "$SCRIPT_DIR/docker-compose.metasploit.yml")

case "${1:-up}" in
  up|start|build)
    echo '[*] Building and starting HackLabs + Metasploit ActiveMQ target...'
    "${COMPOSE[@]}" up -d --build
    echo '[+] HackLabs:          http://127.0.0.1:5000'
    echo '[+] ActiveMQ OpenWire: 127.0.0.1:61616'
    echo '[+] ActiveMQ console:  http://127.0.0.1:8161'
    echo '[!] Keep this intentionally vulnerable environment on an isolated network.'
    ;;
  down|stop)
    echo '[*] Stopping HackLabs and the Metasploit target...'
    "${COMPOSE[@]}" down
    ;;
  status|ps)
    "${COMPOSE[@]}" ps
    ;;
  logs)
    if [[ -n "${2:-}" ]]; then
      "${COMPOSE[@]}" logs -f "$2"
    else
      "${COMPOSE[@]}" logs -f
    fi
    ;;
  *)
    echo "Usage: $0 [up|down|status|logs [service]]" >&2
    exit 2
    ;;
esac
