## 2026-04-28 — i18n: titulos de labs traducibles en sidebar, cards y header

- fix(base.html): Los titulos de labs en el menu lateral ahora tienen `data-i18n` y se traducen al cambiar idioma.
- fix(index.html): Los titulos en las cards del index ahora tienen `data-i18n` y se traducen.
- fix(_lab_header.html): El titulo (h1) y el breadcrumb dentro de cada lab ahora tienen `data-i18n` y se traducen.
- feat(main.js): Nuevas claves ES/EN `lab_title_file_upload` y `lab_title_api_attacks` para los labs con titulo en español.
- El mecanismo escala: cualquier lab sin clave definida mantiene el texto del servidor sin afectarse.

## 2026-04-28 — File Upload: numeracion y reverse shell en resolucion

- fix(file_upload): Numeracion correcta en la resolucion: una sola `<ol>` por seccion con `<pre>` dentro de cada `<li>`, eliminando el hack `<ol start=N>` que mostraba siempre el numero 1.
- feat(file_upload): Pasos de reverse shell en las 3 dificultades (Easy, Medium, Hard): listener `nc -lvnp 4444` + bash one-liner via parametro `cmd`, con la IP del atacante auto-completada (`{{ client_ip }}`).
- feat(file_upload): Alternativa de reverse shell PHP directa (`fsockopen`) en Easy.

## 2026-04-28 — File Upload: resolucion por dificultad, traducciones y bypass doble extension

- feat(file_upload): Resolucion reescrita en ES/EN con pasos especificos para Easy, Medium y Hard.
- feat(file_upload): Los textos del modal de borrado ahora tienen data-i18n y se traducen con el idioma seleccionado.
- feat(main.js): Nuevas claves i18n ES/EN para el modal de borrado (upload_del_title, upload_del_irrev, upload_del_confirm, upload_del_cancel, upload_del_ok).
- fix(app.py): La ruta /uploads/<filename> ahora ejecuta como PHP cualquier archivo con .php en el nombre (re.search), incluyendo bypass de doble extension (.php.jpg, .php.png) necesario para Medium y Hard.

## 2026-04-28 — File Upload: webshells graficas, borrado funcional y errores PHP visibles

- feat(file_upload): Soporte completo para webshells graficas (P0wnyshell, Laudanum) mediante ejecucion con `php-cgi` y variables CGI completas (`REDIRECT_STATUS`, `PHP_SELF`, `SCRIPT_NAME`, `DOCUMENT_ROOT`, `SERVER_SOFTWARE`).
- feat(file_upload): PHP ejecutado siempre con `display_errors=On` y `error_reporting=32767`; los errores de PHP se muestran directamente en el navegador (incluido stderr).
- fix(file_upload): El boton de papelera no funcionaba porque el bloque `<script>` estaba fuera de `{% block content %}` y Jinja2 lo descartaba silenciosamente.
- fix(file_upload): La ruta `/uploads/delete/<filename>` estaba registrada en la primera instancia de Flask que era sobreescrita por una segunda; movida al app correcto.
- fix(file_upload): Eliminada llamada a `secure_filename` en el borrado, que alteraba nombres de archivo impidiendo encontrarlos.
- fix(file_upload): Ruta `/uploads/<filename>` ahora acepta GET, POST y PUT para compatibilidad con webshells que usan formularios internos.
- fix(Dockerfile): Agregados `php-cli` y `php-cgi` al contenedor Docker.

## 2026-04-28 — C2 Sliver: resolución Linux por defecto, enlaces destacados y multilenguaje

- feat(c2_sliver): La resolución del lab de C2 ahora usa por defecto implants de Linux y el ejemplo de transferencia usa la IP 10.9.13.63.
- feat(c2_sliver): Descripción y resolución multilenguaje (español/inglés) con sistema lang-content.
- feat(css): Los enlaces en las descripciones de los labs ahora son amarillos, peso light, sin subrayado por defecto y subrayado al pasar el ratón.
- fix(c2_sliver): Traducción correcta de la descripción según idioma seleccionado.


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
