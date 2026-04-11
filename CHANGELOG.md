# Changelog

All notable changes to this repository are documented in this file.

## 2026-04-11 — Cambios recientes

- feat(labs): Añadido laboratorio "C2 – Sliver Command & Control".
  - Nuevo template: `templates/labs/c2_sliver.html` con instrucciones, resolución y ejemplos.
- feat(app): Ordenar la lista de labs alfabéticamente y exponer `client_ip` en el contexto de plantillas.
  - Añadida la entrada `c2_sliver` en `get_lab_list()`.
- feat(css): Añadido hover amarillo para enlaces en `.hl-card`, `.lang-content` y `.lab-section` (`static/css/style.css`).
- fix(templates): Reemplazados placeholders en la plantilla de Sliver:
  - `YOUR_KALI_IP` → `{{ client_ip }}`
  - Nombres de payload → `IMPLANT_NAME`
  - Transferencias: `scp ... admin@{{ target_ip }}:/tmp/`
  - Post-explotación orientada a Linux (comandos `ps`, `info`, `execute -o id`, `download /etc/shadow`).
- docs: Añadido enlace a la guía GitBook en referencias del lab.

Commit principal: "feat(labs): add C2 Sliver lab, templates and styles" (pushed to `main`).

---

Nota: Para probar localmente:
```bash
python app.py
# o (PowerShell)
$env:FLASK_APP='app.py'; $env:FLASK_ENV='development'; python -m flask run --host=127.0.0.1 --port=5000
```
