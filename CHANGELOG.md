## 2026-04-28 — 4 nuevos labs + mejoras a 6 labs existentes

### Nuevos labs
- feat(race_condition): Banco vulnerable con transferencias concurrentes. 3 dificultades: sin lock (easy), TOCTOU (medium), lock preciso (hard). Interfaz con ataque automatico via Promise.all. Flags por dificultad.
- feat(business_logic): Tienda con 3 vectores: manipulacion de precio en campo oculto (easy), cantidad negativa y coupon stacking (medium), bypass de flujo con redondeo entero (hard). Flag: `HL{bu51n355_l0g1c_0wn3d}`.
- feat(container_escape): Recon en vivo de vectores de escape (Docker socket, privileged, cgroups, root uid). Resolucion por dificultad: docker socket mount (easy), fdisk + chroot (medium), cgroup release_agent (hard).
- feat(oauth): Flujo OAuth 2.0 simulado. redirect_uri sin validacion (easy), solo dominio validado con bypass por path (medium), whitelist exacta (hard). Flag: `HL{0auth_r3d1r3ct_0wn3d}`.

### Mejoras a labs existentes
- feat(ssrf): Nuevo endpoint interno `/internal/cloud-metadata` simula AWS IMDSv1 con credenciales falsas. Flag: `HL{55rf_cl0ud_m3t4d4t4}`. Bypass por IP decimal (medium) e IPv6 (hard).
- feat(jwt): Hard mode con algorithm confusion RS256→HS256 usando la clave publica como secreto HMAC. Clave publica expuesta en `/jwt/jwks`. Flag: `HL{4lg_c0nfu510n_0wn3d}`.
- feat(path_traversal): Log poisoning via User-Agent en `logs/access.log`. Resolucion ampliada con bypasses `....//` y `%252e%252e%252f` para medium/hard.
- feat(sqli): Resolucion ampliada con blind SQLi boolean-based y time-based via `randomblob()` para hard mode.
- feat(file_upload): Ejecucion real de PHP via php-cgi, soporte de webshells graficas (P0wnyshell, Laudanum), bypass de doble extension (.php.jpg), pasos de reverse shell por dificultad con IP del atacante auto-completada.
- feat(c2_sliver): Resolucion en ES/EN con implants de Linux por defecto.


## 2026-04-27 — File Upload: ejecución real, borrado y mejoras UX

- feat(file_upload): Ahora los archivos PHP subidos se ejecutan realmente al acceder vía navegador, simulando un servidor vulnerable (webshells funcionales).
- feat(file_upload): Soporte para múltiples archivos subidos y persistentes hasta borrado manual.
- feat(file_upload): Papelera de borrado con confirmación y AJAX, sin recarga ni redirección.
- fix(file_upload): El botón de eliminar ahora funciona siempre, sin conflictos de ámbito ni formularios.
- fix(file_upload): Mensajes informativos de subida solo en texto plano, sin HTML.
- fix(file_upload): El área de selección de archivos ya no dispara doble selección.
- fix(file_upload): El label muestra correctamente todos los archivos seleccionados.
- fix(file_upload): Restaurada la detección de IP real en el banner y URLs.
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

## 2026-04-27 — API Attacks: dificultad real y mejoras

- feat(api_attacks): Los endpoints de la API ahora cambian su comportamiento según la dificultad seleccionada (easy, medium, hard):
  - `/api/v1/users`:
    - Easy: expone todos los datos y contraseñas.
    - Medium: oculta contraseñas, solo username/email.
    - Hard: solo username/email y requiere header Authorization.
  - `/api/v1/transfer`:
    - Medium: requiere campo `confirm`.
    - Hard: requiere header Authorization y confirmación.
  - `/api/v1/notes`:
    - Medium: la flag está oculta.
    - Hard: requiere header Authorization para ver la flag.
- docs: Actualizada la resolución del lab de API Attacks con ejemplos de comandos para cada dificultad.
- fix(api_attacks): Flag de API ahora usa formato `HL{...}` como el resto de flags.
- docs: Añadida la flag de API Attacks al README con ejemplo de uso.

---

### 2026-04-27 — Hotfixes y ajustes (detalle)

- fix(app): Evitar banner duplicado al ejecutar con el reloader de Flask.
  - El banner y los servicios simulados ahora se imprimen solo en el proceso hijo del reloader (WERKZEUG_RUN_MAIN), evitando duplicados en la salida.
- fix(api): Actualizadas las notas expuestas en `/api/v1/notes` para mostrar las credenciales reales del admin en los modos easy/medium/hard (`Username: admin, Password: password1`).
- fix(templates/routes): Reparada la plantilla `templates/labs/api_attacks.html` (se limpió contenido corrupto y se movió la resolución dentro del contenedor oculto `#resolution-data`).
- feat(routes): Añadida ruta dedicada `/api_attacks` para el laboratorio de API Attacks y corregida la lógica de mapeo para el sidebar (`current_lab_id`).
- fix(icons): Actualizados los mappings de iconos en `templates/base.html` y `templates/index.html` para mostrar el icono correcto en sidebar y tarjetas.

Prueba rápida local:
```bash
python3 app.py
curl -i 'http://localhost/api/v1/notes' -H 'Authorization: Bearer hacklabs-integrity-token'
```

Nota: Para probar localmente:
```bash
python app.py
# o (PowerShell)
$env:FLASK_APP='app.py'; $env:FLASK_ENV='development'; python -m flask run --host=127.0.0.1 --port=5000
```
