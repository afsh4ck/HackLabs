// ── HackLabs main.js ──────────────────────────────────────────────

// ── Translations ─────────────────────────────────────────────────
const T = {
  es: {
    home:            'Inicio',
    logout:          'Salir',
    footer_warning:  'Solo para uso educativo en entornos aislados',
    modal_title:     'Resolución del laboratorio',
    btn_resolution:  'Ver resolución',
    close:           'Cerrar',
    cat_owasp_top_10:       'OWASP Top 10',
    cat_extras:            'Extras',
    cat_vulnerabilidades:  'Vulnerabilidades',
    cat_ia_attacks:        'IA Attacks',
    labs:            'Labs',
    resolution_steps:'Pasos de explotación',
    tools_label:     'Herramientas',
    // Home
    badge_text:      'Intencionalmente Vulnerable · Solo uso educativo',
    filter_label:    'Filtrar:',
    filter_all:      'Todos',
    open_lab:        'Abrir lab',
    test_credentials:'Usuarios y Contraseñas',
    col_username:    'Usuario',
    col_password:    'Contraseña',
    col_hash:        'Hash MD5',
    col_role:        'Rol',
    stat_total:      'Total Labs',
    stat_critical:   'Críticos',
    stat_high:       'Altos',
    stat_medium:     'Medios',
    hero_by:         'Plataforma de hacking ético por',
    hero_rest:       'Practica el OWASP Top 10 (2021) y más con Burp Suite, sqlmap, hydra y otras herramientas de Kali Linux.',
    lab_cat_count:   'labs',
    // A05 Misconfig
    misconfig_title: 'Configuraciones inseguras',
    misconfig_item1: 'Panel de administración accesible sin autenticación',
    misconfig_item2: 'Repositorio Git expuesto',
    misconfig_item3: 'Stack trace completo del servidor expuesto en errores',
    misconfig_item4: 'API interna de usuarios accesible sin autenticación',
    misconfig_hint:  'Usa herramientas de fuzzing de directorios para descubrir los endpoints expuestos.',
    misconfig_admin_panel: 'Panel de administración — Sin autenticación',
    // Shared form labels
    lbl_username:    'Usuario',
    lbl_password:    'Contraseña',
    lbl_search:      'Buscar',
    lbl_search_products: 'Buscar productos',
    lbl_host_ip:     'Host / IP',
    lbl_output:      'Salida',
    lbl_result:      'Resultado',
    lbl_target_url:  'URL de destino',
    lbl_file_path:   'Ruta del archivo',
    lbl_xml_payload: 'Payload XML',
    lbl_jwt_token:   'Token JWT',
    // Shared buttons
    btn_login:       'Iniciar sesión',
    btn_search:      'Buscar',
    btn_render:      'Renderizar',
    btn_fetch:       'Obtener',
    gh_star_tooltip: 'Poner estrella en GitHub',
    btn_read:        'Leer',
    btn_ping:        'Ping',
    btn_upload:      'Subir archivo',
    btn_parse_xml:   'Parsear XML',
    btn_go:          'Ir a destino',
    btn_change_pw:   'Cambiar contraseña',
    btn_post_comment:'Publicar comentario',
    btn_continue:    'Continuar',
    btn_verify:      'Verificar',
    btn_send_put:    'Enviar PUT',
    btn_launch_csrf: 'Lanzar CSRF',
    // Shared placeholders
    ph_search:       'Buscar...',
    ph_search_products: 'Buscar productos...',
    ph_redirect_url: 'https://ejemplo.com/dashboard',
    ph_comment_name: 'Nombre',
    ph_new_email:    'nuevo@email.com',
    // SSTI
    ssti_label:      'Entrada de plantilla',
    ssti_rendered:   'Salida renderizada',
    // Open Redirect
    or_desc:         'Este portal redirige a los usuarios tras completar acciones. El parámetro de destino no está validado.',
    or_examples:     'Ejemplos',
    or_comment1:     '# Redirección a sitio externo (phishing)',
    or_comment2:     '# Bypass de filtros básicos',
    // JWT
    jwt_generate:    'Generar Token',
    jwt_btn_gen:     'Generar JWT',
    jwt_secret_used: 'Secreto usado:',
    jwt_verify:      'Verificar / Manipular Token',
    jwt_btn_verify:  'Verificar',
    jwt_decoded:     'Payload decodificado',
    // Deserialization
    deser_title:     'Deserializar objeto Python (pickle)',
    deser_label:     'Payload (base64 pickle)',
    deser_ph:        'Introduce un objeto pickle serializado en base64...',
    deser_btn:       'Deserializar',
    deser_example:   'Ejemplo seguro (dict):',
    deser_result:    'Resultado',
    // CORS
    cors_api_title:  'API de datos internos',
    cors_api_desc:   'La API devuelve datos sensibles y refleja cualquier cabecera Origin con Access-Control-Allow-Credentials: true.',
    cors_comment1:   '# Endpoint vulnerable',
    cors_comment2:   '# Probar con curl (observa las cabeceras CORS)',
    cors_btn:        'Hacer petición cross-origin',
    cors_response:   'Respuesta:',
    cors_poc_title:  'PoC – Página maliciosa',
    // XSS
    xss_tab_reflected: 'Reflejado',
    xss_tab_stored:  'Almacenado',
    xss_tab_dom:     'DOM-based',
    xss_results_for: 'Resultados para:',
    xss_name_ph:     'Nombre',
    xss_btn_post:    'Publicar comentario',
    xss_dom_label:   'Salida dinámica (desde fragmento URL):',
    xss_dom_hint:    'Añade un fragmento a la URL: #<img src=x onerror=alert(1)>',
    // CSRF
    csrf_user_label: 'Usuario:',
    csrf_id_label:   'ID:',
    csrf_role_label: 'Rol:',
    csrf_new_pw:     'Nueva contraseña',
    csrf_ph_new_pw:  'Introduce una contraseña',
    csrf_btn_change: 'Cambiar contraseña',
    csrf_attack_title: 'Ataque CSRF — Auto-envío',
    csrf_victim_id:  'ID de usuario víctima',
    csrf_btn_launch: 'Lanzar CSRF',
    // File Upload
    // Lab titles (only labs whose default title is not already in Spanish/neutral)
    lab_title_file_upload:    'File Upload sin restricciones',
    lab_title_api_attacks:    'API Attacks – Laboratorio de APIs Inseguras',
    lab_title_business_logic: 'Business Logic Flaws',
    lab_title_container_escape: 'Container Escape',
    lab_title_oauth:          'OAuth 2.0 Attacks',
    lab_title_race_condition: 'Race Condition / TOCTOU',
    // OAuth
    oauth_flow:          'Flujo de Autorización',
    oauth_flow_desc:     'Haz clic en el botón para iniciar el flujo OAuth 2.0. El servidor te redirigirá al callback con un código de autorización.',
    oauth_start_btn:     'Iniciar flujo OAuth',
    oauth_token:         'Token de Acceso',
    oauth_userinfo_hint: 'Usa este token para acceder a recursos protegidos:',
    oauth_how:           'Cómo funciona el ataque redirect_uri',
    oauth_how_desc:      'En OAuth 2.0, tras autorizar la app el servidor redirige a redirect_uri con el código. Si no se valida, un atacante puede redirigir el código a cualquier URL que controle.',
    oauth_step1:         'El usuario hace clic en "Autorizar" en la app legítima',
    oauth_step2:         'El atacante intercepta la petición y cambia redirect_uri',
    oauth_step3:         'El código de autorización se envía al servidor del atacante',
    oauth_step4:         'El atacante intercambia el código por un token de acceso',
    oauth_step5:         'El atacante accede a los recursos de la víctima',
    // Business Logic
    shop_catalog:        'Catálogo de Productos',
    shop_balance:        'Saldo:',
    shop_prod1_name:     'HackLabs Pro License',
    shop_prod1_desc:     'Acceso completo a todos los labs',
    shop_qty:            'Cant:',
    shop_add_btn:        'Añadir al carrito',
    shop_prod2_name:     'Zero-Day Exploit Kit',
    shop_prod2_desc:     'Framework de exploits simulado',
    shop_prod3_name:     'Servicio VPN',
    shop_prod3_desc:     'VPN anónima por 1 año',
    shop_cart:           'Carrito',
    shop_total:          'Total',
    shop_cart_empty:     'El carrito está vacío.',
    shop_apply_coupon:   'Aplicar',
    shop_checkout:       'Comprar',
    shop_clear_cart:     'Limpiar',
    // Race Condition
    race_balances:       'Balances',
    race_alice:          'Alice',
    race_bob:            'Bob',
    race_transfer_btn:   'Transferir Alice → Bob',
    race_reset_btn:      'Reiniciar',
    race_attack_panel:   'Panel de Ataque Race',
    race_attack_desc:    'Lanza 10 peticiones concurrentes de $5 cada una. Si Alice tiene $10.00 y el servidor tiene race condition, Bob puede acabar con más de $10.00.',
    race_run_btn:        'Ejecutar Race Attack',
    race_log:            'Log de Resultados',
    // Container Escape
    container_recon:         'Reconocimiento del Contenedor',
    container_check_in:      'Ejecutando en contenedor',
    container_check_socket:  '/var/run/docker.sock',
    container_check_root:    'Ejecutando como root',
    container_check_priv:    'Modo privilegiado',
    container_check_hostpath:'Ruta del host montada con escritura',
    container_check_id:      'salida de id',
    container_check_cap:     'CapEff (capacidades efectivas)',
    upload_dropzone: 'Haz clic o arrastra un archivo aquí',
    upload_no_restrict: 'Sin restricciones de tipo de archivo',
    upload_btn:      'Subir archivo',
    upload_open:     'Abrir archivo',
    upload_list:     'Archivos subidos (/uploads/)',
    upload_access:   'Acceder →',
    upload_del_title: 'Eliminar archivo',
    upload_del_irrev: 'Esta acción no se puede deshacer',
    upload_del_confirm: '¿Eliminar',
    upload_del_cancel: 'Cancelar',
    upload_del_ok:   'Eliminar',
    // XXE
    xxe_btn_normal:  'XML Normal',
    xxe_btn_xxe:     'Payload XXE',
    xxe_parsed:      'Resultado parseado',
    xxe_name:        'nombre:',
    xxe_email:       'email:',
    // Path Traversal
    pt_btn_read:     'Leer',
    // Bruteforce
    bf_tab_http:     'Login HTTP',
    bf_login_title:  'Login sin rate-limiting',
    bf_ssh_desc:     'Ataque de fuerza bruta contra el servicio SSH de la máquina objetivo. No hay rate-limiting activo; la autenticación se gestiona por el servidor SSH del host.',
    bf_smb_desc:     'Ataque de fuerza bruta contra el servicio SMB/CIFS de la máquina objetivo (puerto 445).',
    bf_ftp_desc:     'Ataque de fuerza bruta contra el servicio FTP de la máquina objetivo (puerto 21). No hay rate-limiting activo.',
    // SQLi
    sqli_label:      'Buscar productos',
    sqli_query:      'Consulta:',
    sqli_no_results: 'Sin resultados para',
    // CMDi
    cmdi_output:     'Salida',
    // IDOR
    idor_label_id:   'ID de usuario',
    idor_btn_view:   'Ver perfil',
    idor_profile:    'Perfil — ID:',
    idor_no_user:    'Usuario no encontrado con ID=',
    // Insecure Design
    insec_btn_continue: 'Continuar',
    insec_user_label:   'Usuario:',
    insec_lbl_answer:   'Respuesta',
    insec_btn_verify:   'Verificar',
    insec_compromised:  '¡Cuenta comprometida!',
    insec_user_inline:  'Usuario:',
    insec_pw_label:     'Contraseña en texto plano:',
    // Outdated
    out_label:       'Buscar',
    out_ph:          'Buscar productos...',
    out_searching:   'Buscando:',
    out_enter:       'Introduce un término de búsqueda...',
    // Integrity
    int_target_id:   'ID de usuario objetivo',
    int_new_role:    'Nuevo rol',
    int_new_email:   'Nuevo email (opcional)',
    int_btn_send:    'Enviar PUT',
    // Logging
    log_empty:       '(vacío — ningún evento de seguridad es registrado)',
    // SSRF
    ssrf_label:      'URL destino',
    ssrf_response:   'Respuesta de:',
    // Auth Failures
    auth_lbl_user:   'Usuario',
    auth_lbl_pass:   'Contraseña',
    auth_btn_login:  'Iniciar sesión',
    difficulty_label: 'Dificultad',
    sidebar_search:  'Buscar lab...',
    // User menu
    nav_profile:     'Mi perfil',
    nav_progress:    'Mi progreso',
    nav_logout:      'Cerrar sesión',
    // Progress / complete button
    complete_lab:    'Completar',
    completed_lab:   'Completado',
    progress_hint_title: 'Progreso de labs',
    progress_hint_body:  'Para guardar el progreso usa una cuenta propia. Los usuarios de laboratorio (admin, alice…) son para prácticas.',
    progress_hint_cta:   'Crear cuenta',
  },
  en: {
    home:            'Home',
    logout:          'Log out',
    footer_warning:  'For educational use in isolated environments only',
    modal_title:     'Lab Resolution',
    btn_resolution:  'View Resolution',
    close:           'Close',
    cat_owasp_top_10:       'OWASP Top 10',
    cat_extras:            'Extras',
    cat_vulnerabilidades:  'Vulnerabilidades',
    cat_ia_attacks:        'IA Attacks',
    labs:            'Labs',
    resolution_steps:'Exploitation Steps',
    tools_label:     'Tools',
    // Home
    badge_text:      'Intentionally Vulnerable · Educational Use Only',
    filter_label:    'Filter:',
    filter_all:      'All',
    open_lab:        'Open lab',
    test_credentials:'Users & Passwords',
    col_username:    'Username',
    col_password:    'Password',
    col_hash:        'MD5 Hash',
    col_role:        'Role',
    stat_total:      'Total Labs',
    stat_critical:   'Critical',
    stat_high:       'High',
    stat_medium:     'Medium',
    hero_by:         'Ethical hacking training platform by',
    hero_rest:       'Practice OWASP Top 10 (2021) and more with Burp Suite, sqlmap, hydra and other Kali Linux tools.',
    lab_cat_count:   'labs',
    // A05 Misconfig
    misconfig_title: 'Misconfigurations',
    misconfig_item1: 'Admin panel accessible without authentication',
    misconfig_item2: 'Git repository configuration exposed',
    misconfig_item3: 'Full server stack trace disclosed on error',
    misconfig_item4: 'Internal user API accessible without auth',
    misconfig_hint:  'Use directory fuzzing tools to discover exposed endpoints.',
    misconfig_admin_panel: 'Admin Panel — No Authentication Required',
    // Shared form labels
    lbl_username:    'Username',
    lbl_password:    'Password',
    lbl_search:      'Search',
    lbl_search_products: 'Search products',
    lbl_host_ip:     'Host / IP',
    lbl_output:      'Output',
    lbl_result:      'Result',
    lbl_target_url:  'Target URL',
    lbl_file_path:   'File path',
    lbl_xml_payload: 'XML Payload',
    lbl_jwt_token:   'JWT Token',
    // Shared buttons
    btn_login:       'Login',
    btn_search:      'Search',
    btn_render:      'Render',
    btn_fetch:       'Fetch',
    gh_star_tooltip: 'Star on GitHub',
    btn_read:        'Read',
    btn_ping:        'Ping',
    btn_upload:      'Upload',
    btn_parse_xml:   'Parse XML',
    btn_go:          'Go to destination',
    btn_change_pw:   'Change Password',
    btn_post_comment:'Post Comment',
    btn_continue:    'Continue',
    btn_verify:      'Verify',
    btn_send_put:    'Send PUT',
    btn_launch_csrf: 'Launch CSRF',
    // Shared placeholders
    ph_search:       'Search...',
    ph_search_products: 'Search products...',
    ph_redirect_url: 'https://example.com/dashboard',
    ph_comment_name: 'Name',
    ph_new_email:    'new@email.com',
    // SSTI
    ssti_label:      'Template Input',
    ssti_rendered:   'Rendered output',
    // Open Redirect
    or_desc:         'This portal redirects users after completing actions. The destination parameter is not validated.',
    or_examples:     'Examples',
    or_comment1:     '# Redirect to external site (phishing)',
    or_comment2:     '# Bypass basic filters',
    // JWT
    jwt_generate:    'Generate Token',
    jwt_btn_gen:     'Generate JWT',
    jwt_secret_used: 'Secret used:',
    jwt_verify:      'Verify / Manipulate Token',
    jwt_btn_verify:  'Verify',
    jwt_decoded:     'Decoded payload',
    // Deserialization
    deser_title:     'Deserialize Python object (pickle)',
    deser_label:     'Payload (base64 pickle)',
    deser_ph:        'Enter a base64-serialized pickle object...',
    deser_btn:       'Deserialize',
    deser_example:   'Safe example (dict):',
    deser_result:    'Result',
    // CORS
    cors_api_title:  'Internal data API',
    cors_api_desc:   'The API returns sensitive data and reflects any Origin header with Access-Control-Allow-Credentials: true.',
    cors_comment1:   '# Vulnerable endpoint',
    cors_comment2:   '# Test with curl (observe CORS headers)',
    cors_btn:        'Make cross-origin request',
    cors_response:   'Response:',
    cors_poc_title:  'PoC – Malicious page',
    // XSS
    xss_tab_reflected: 'Reflected',
    xss_tab_stored:  'Stored',
    xss_tab_dom:     'DOM-based',
    xss_results_for: 'Results for:',
    xss_name_ph:     'Name',
    xss_btn_post:    'Post Comment',
    xss_dom_label:   'Dynamic output (from URL fragment):',
    xss_dom_hint:    'Add a fragment to the URL: #<img src=x onerror=alert(1)>',
    // CSRF
    csrf_user_label: 'User:',
    csrf_id_label:   'ID:',
    csrf_role_label: 'Role:',
    csrf_new_pw:     'New Password',
    csrf_ph_new_pw:  'Enter a password',
    csrf_btn_change: 'Change Password',
    csrf_attack_title: 'CSRF Attack — Auto-submit',
    csrf_victim_id:  'Victim User ID',
    csrf_btn_launch: 'Launch CSRF',
    // File Upload
    // Lab titles
    lab_title_file_upload:    'File Upload – No Restrictions',
    lab_title_api_attacks:    'API Attacks – Insecure APIs Lab',
    lab_title_business_logic: 'Business Logic Flaws',
    lab_title_container_escape: 'Container Escape',
    lab_title_oauth:          'OAuth 2.0 Attacks',
    lab_title_race_condition: 'Race Condition / TOCTOU',
    // OAuth
    oauth_flow:          'Authorization Flow',
    oauth_flow_desc:     'Click the button below to start the OAuth 2.0 authorization flow. The server will redirect you to the callback with an authorization code.',
    oauth_start_btn:     'Start OAuth Flow',
    oauth_token:         'Access Token',
    oauth_userinfo_hint: 'Use this token to access protected resources:',
    oauth_how:           'How OAuth redirect_uri Attack Works',
    oauth_how_desc:      'In OAuth 2.0, after the user authorizes the application the server redirects to redirect_uri with the authorization code. If the server does not validate this URI, an attacker can set it to any URL they control and steal the code.',
    oauth_step1:         'User clicks "Authorize" in the legitimate app',
    oauth_step2:         'Attacker intercepts the request and changes redirect_uri',
    oauth_step3:         'Authorization code is sent to the attacker\'s server',
    oauth_step4:         'Attacker exchanges the code for an access token',
    oauth_step5:         'Attacker accesses the victim\'s resources',
    // Business Logic
    shop_catalog:        'Product Catalog',
    shop_balance:        'Balance:',
    shop_prod1_name:     'HackLabs Pro License',
    shop_prod1_desc:     'Full access to all labs',
    shop_qty:            'Qty:',
    shop_add_btn:        'Add to Cart',
    shop_prod2_name:     'Zero-Day Exploit Kit',
    shop_prod2_desc:     'Simulated exploit framework',
    shop_prod3_name:     'VPN Service',
    shop_prod3_desc:     '1-year anonymous VPN',
    shop_cart:           'Cart',
    shop_total:          'Total',
    shop_cart_empty:     'Cart is empty.',
    shop_apply_coupon:   'Apply',
    shop_checkout:       'Checkout',
    shop_clear_cart:     'Clear',
    // Race Condition
    race_balances:       'Balances',
    race_alice:          'Alice',
    race_bob:            'Bob',
    race_transfer_btn:   'Transfer Alice → Bob',
    race_reset_btn:      'Reset',
    race_attack_panel:   'Race Attack',
    race_attack_desc:    'Fires 10 concurrent requests of $5 each. If Alice has $10.00 and the server has a race condition, Bob may end up with more than $10.00.',
    race_run_btn:        'Run Race Attack',
    race_log:            'Result Log',
    // Container Escape
    container_recon:         'Container Recon',
    container_check_in:      'Running in container',
    container_check_socket:  '/var/run/docker.sock',
    container_check_root:    'Running as root',
    container_check_priv:    'Privileged mode',
    container_check_hostpath:'Writable host path mounted',
    container_check_id:      'id output',
    container_check_cap:     'CapEff (effective capabilities)',
    upload_dropzone: 'Click or drag file here',
    upload_no_restrict: 'No file type restrictions',
    upload_btn:      'Upload',
    upload_open:     'Open file',
    upload_list:     'Uploaded files (/uploads/)',
    upload_access:   'Access →',
    upload_del_title: 'Delete file',
    upload_del_irrev: 'This action cannot be undone',
    upload_del_confirm: 'Delete',
    upload_del_cancel: 'Cancel',
    upload_del_ok:   'Delete',
    // XXE
    xxe_btn_normal:  'Normal XML',
    xxe_btn_xxe:     'XXE Payload',
    xxe_parsed:      'Parsed result',
    xxe_name:        'name:',
    xxe_email:       'email:',
    // Path Traversal
    pt_btn_read:     'Read',
    // Bruteforce
    bf_tab_http:     'HTTP Login',
    bf_login_title:  'Login without rate-limiting',
    bf_ssh_desc:     'Brute force attack against the SSH service of the target machine. No rate-limiting is active; authentication is handled by the host SSH server.',
    bf_smb_desc:     'Brute force attack against the SMB/CIFS service of the target machine (port 445).',
    // SQLi
    sqli_label:      'Search products',
    sqli_query:      'Query:',
    sqli_no_results: 'No results for',
    // CMDi
    cmdi_output:     'Output',
    // IDOR
    idor_label_id:   'User ID',
    idor_btn_view:   'View Profile',
    idor_profile:    'Profile — ID:',
    idor_no_user:    'No user found with ID=',
    // Insecure Design
    insec_btn_continue: 'Continue',
    insec_user_label:   'User:',
    insec_lbl_answer:   'Answer',
    insec_btn_verify:   'Verify',
    insec_compromised:  'Account compromised!',
    insec_user_inline:  'User:',
    insec_pw_label:     'Plaintext password:',
    // Outdated
    out_label:       'Search',
    out_ph:          'Search products...',
    out_searching:   'Searching for:',
    out_enter:       'Enter a search term...',
    // Integrity
    int_target_id:   'Target User ID',
    int_new_role:    'New Role',
    int_new_email:   'New Email (optional)',
    int_btn_send:    'Send PUT',
    // Logging
    log_empty:       '(empty — no security events are ever logged)',
    // SSRF
    ssrf_label:      'Target URL',
    ssrf_response:   'Response from:',
    // Auth Failures
    auth_lbl_user:   'Username',
    auth_lbl_pass:   'Password',
    auth_btn_login:  'Login',
    difficulty_label: 'Difficulty',
    sidebar_search:  'Search lab...',
    // User menu
    nav_profile:     'My profile',
    nav_progress:    'My progress',
    nav_logout:      'Log out',
    // Progress / complete button
    complete_lab:    'Complete',
    completed_lab:   'Completed',
    progress_hint_title: 'Lab Progress',
    progress_hint_body:  'To save your progress you need a custom account. Lab users (admin, alice…) are for practice only.',
    progress_hint_cta:   'Create account',
  }
};

// ── State ─────────────────────────────────────────────────────────
const HL = {
  lang:    localStorage.getItem('hl_lang')    || 'es',
  theme:   localStorage.getItem('hl_theme')   || 'dark',
  sidebar: localStorage.getItem('hl_sidebar') !== 'closed',
};

// ── i18n ──────────────────────────────────────────────────────────
function t(key) {
  return (T[HL.lang] || T.es)[key] || key;
}

function applyTranslations() {
  const dict = T[HL.lang] || T.es;

  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.dataset.i18n;
    const val = dict[key];
    if (val === undefined) return;

    if (el.tagName === 'INPUT' && el.type !== 'submit') {
      el.placeholder = val;
    } else if (el.children.length === 0) {
      el.textContent = val;
    } else {
      [...el.childNodes].forEach(node => {
        if (node.nodeType === Node.TEXT_NODE && node.textContent.trim()) {
          node.textContent = ' ' + val;
        }
      });
    }
  });

  // Placeholder-only elements (inputs/textareas with data-i18n-placeholder)
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.dataset.i18nPlaceholder;
    const val = dict[key];
    if (val !== undefined) el.placeholder = val;
  });

  // Sync lang button active states
  ['es', 'en'].forEach(l => {
    const btn = document.getElementById('lang-' + l);
    if (btn) btn.classList.toggle('active-lang', l === HL.lang);
  });

  // Apply lang-content visibility across the whole page (not just modal)
  applyResolutionLang('body');
}

// ── GitHub stars helper ──────────────────────────────────────────
async function fetchGitHubStars() {
  const repo = 'afsh4ck/HackLabs';
  const elWrap = document.getElementById('gh-stars');
  const elCount = document.getElementById('gh-star-count');
  const elBtn = document.getElementById('gh-star-btn');
  if (!elWrap || !elCount || !elBtn) return;
  try {
    const res = await fetch(`https://api.github.com/repos/${repo}`);
    if (!res.ok) throw new Error('GitHub API error');
    const data = await res.json();
    elCount.textContent = (data.stargazers_count || 0).toLocaleString();
    elWrap.classList.remove('hidden');
  } catch (err) {
    elCount.textContent = 'N/A';
    elWrap.classList.remove('hidden');
  }
  // Set localized custom tooltip
  try {
    const title = t('gh_star_tooltip');
    const tooltip = document.getElementById('gh-star-tooltip');
    if (tooltip) tooltip.textContent = title;
    elBtn.setAttribute('aria-label', title);
  } catch (e) {}

  // Click behavior: open repo page so user can star easily (requires GitHub login)
  elBtn.addEventListener('click', (e) => {
    e.preventDefault();
    window.open('https://github.com/afsh4ck/HackLabs', '_blank');
  });
}

// Init on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  try { fetchGitHubStars(); } catch (e) {}
});

function setLang(lang) {
  HL.lang = lang;
  localStorage.setItem('hl_lang', lang);
  // Cambia el texto del botón principal
  const langSelected = document.getElementById('lang-selected');
  if (langSelected) langSelected.textContent = lang === 'en' ? 'English' : 'Español';
  // Actualiza el check visual
  ['es', 'en'].forEach(l => {
    const check = document.getElementById('lang-check-' + l);
    if (check) {
      check.innerHTML = (l === lang)
        ? '<i class="ph-fill ph-check-circle" style="color:#CEFF00;font-size:1.1em"></i>'
        : '';
    }
  });
  // Actualiza el estado activo en el botón
  ['es', 'en'].forEach(l => {
    const btn = document.getElementById('lang-' + l);
    if (btn) {
      btn.classList.toggle('active', l === lang);
      // Aplica color amarillo al texto de la opción activa
      if (l === lang) {
        btn.querySelector('span.font-semibold').style.color = '#CEFF00';
      } else {
        btn.querySelector('span.font-semibold').style.color = '';
      }
    }
  });
  applyTranslations();
  // sync custom dropdown / select UI
  const langSelect = document.getElementById('lang-select');
  if (langSelect) langSelect.value = HL.lang || 'es';
  if (window._initLangDropdown) window._initLangDropdown();
  // Re-apply resolution lang if modal is open
  if (!document.getElementById('resolution-modal').classList.contains('hidden')) {
    applyResolutionLang('#modal-body');
  }
}

// Inicializa el check visual y el texto al cargar
document.addEventListener('DOMContentLoaded', function() {
  setLang(HL.lang);
});
// Custom language dropdown behaviour
function initLangDropdown() {
  const wrap = document.getElementById('lang-wrap');
  if (!wrap) return;
  const btn = document.getElementById('lang-btn');
  const list = document.getElementById('lang-list');
  const selected = document.getElementById('lang-selected');

  // set initial state from HL.lang
  selected.textContent = HL.lang === 'en' ? 'English' : 'Español';
  // mark active option
  list.querySelectorAll('.lang-option').forEach(li => li.classList.toggle('active', li.dataset.lang === HL.lang));

  function open() {
    list.classList.remove('hidden');
    btn.setAttribute('aria-expanded', 'true');
  }
  function close() {
    list.classList.add('hidden');
    btn.setAttribute('aria-expanded', 'false');
  }

  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    if (list.classList.contains('hidden')) open(); else close();
  });

  list.addEventListener('click', (e) => {
    const li = e.target.closest('.lang-option');
    if (!li) return;
    const lang = li.dataset.lang;
    setLang(lang);
    selected.textContent = li.textContent;
    list.querySelectorAll('.lang-option').forEach(x => x.classList.remove('active'));
    li.classList.add('active');
    close();
  });

  // close when clicking outside
  document.addEventListener('click', (e) => { if (!wrap.contains(e.target)) close(); });

  // helper to sync UI after translations applied
  window._initLangDropdown = () => {
    const sel = document.getElementById('lang-selected');
    const hl = HL.lang || 'es';
    sel && (sel.textContent = hl === 'en' ? 'English' : 'Español');
    list.querySelectorAll('.lang-option').forEach(li => li.classList.toggle('active', li.dataset.lang === hl));
  };
}

function applyResolutionLang(scope) {
  document.querySelectorAll(scope + ' .lang-content').forEach(el => {
    el.style.display = (el.dataset.lang === HL.lang) ? '' : 'none';
  });
}

// ── Theme ─────────────────────────────────────────────────────────
function applyTheme() {
  const isDark = HL.theme === 'dark';
  document.documentElement.classList.toggle('dark', isDark);
  document.documentElement.style.colorScheme = isDark ? 'dark' : 'light';
}

function toggleTheme() {
  HL.theme = HL.theme === 'dark' ? 'light' : 'dark';
  localStorage.setItem('hl_theme', HL.theme);
  applyTheme();
}

// ── Sidebar category collapse ─────────────────────────────────────
function toggleCategory(catId) {
  const items  = document.getElementById('cat-' + catId);
  const caret  = document.querySelector(`[data-cat="${catId}"] .sidebar-caret`);
  if (!items) return;
  const isCollapsed = items.classList.contains('collapsed');
  items.classList.toggle('collapsed', !isCollapsed);
  caret && caret.classList.toggle('rotated', !isCollapsed);
  const state = JSON.parse(localStorage.getItem('hl_cats') || '{}');
  state[catId] = !isCollapsed; // true = collapsed
  localStorage.setItem('hl_cats', JSON.stringify(state));
}

function initCategories() {
  const state = JSON.parse(localStorage.getItem('hl_cats') || '{}');
  Object.entries(state).forEach(([catId, collapsed]) => {
    if (!collapsed) return;
    const items = document.getElementById('cat-' + catId);
    const caret = document.querySelector(`[data-cat="${catId}"] .sidebar-caret`);
    if (items) items.classList.add('collapsed');
    if (caret) caret.classList.add('rotated');
  });
}

// ── Sidebar ───────────────────────────────────────────────────────
function applySidebar() {
  const sb  = document.getElementById('sidebar');
  const iOp = document.getElementById('sidebar-icon-open');
  const iCl = document.getElementById('sidebar-icon-close');
  const ft  = document.getElementById('app-footer');
  if (!sb) return;
  if (!sb.classList.contains('transition-all')) sb.classList.add('transition-all', 'duration-300');
  sb.classList.toggle('sidebar-open',   HL.sidebar);
  sb.classList.toggle('sidebar-closed', !HL.sidebar);
  iOp && iOp.classList.toggle('hidden',  HL.sidebar);
  iCl && iCl.classList.toggle('hidden', !HL.sidebar);
  if (ft) ft.style.marginLeft = HL.sidebar ? 'var(--sidebar-width)' : '0';
}

function toggleSidebar() {
  HL.sidebar = !HL.sidebar;
  localStorage.setItem('hl_sidebar', HL.sidebar ? 'open' : 'closed');
  applySidebar();
}

// ── Resolution modal ──────────────────────────────────────────────
function openResolution() {
  const data = document.getElementById('resolution-data');
  if (!data) return;
  const body = document.getElementById('modal-body');
  body.innerHTML = data.innerHTML;
  applyResolutionLang('#modal-body');
  document.querySelectorAll('#modal-body [data-i18n]').forEach(el => {
    el.textContent = t(el.dataset.i18n);
  });
  // Highlight code inside modal and add copy buttons
  body.querySelectorAll('pre').forEach(pre => {
    pre.style.position = 'relative';
    const code = pre.querySelector('code');
    if (code && typeof hljs !== 'undefined') hljs.highlightElement(code);
    const btn = document.createElement('button');
    btn.title = HL.lang === 'en' ? 'Copy' : 'Copiar';
    btn.innerHTML = '<i class="ph ph-copy"></i>';
    btn.style.cssText = [
      'position:absolute', 'top:8px', 'right:8px',
      'background:rgba(255,255,255,0.08)', 'border:1px solid rgba(255,255,255,0.15)',
      'color:#9ca3af', 'border-radius:6px', 'padding:3px 7px',
      'cursor:pointer', 'font-size:13px', 'line-height:1', 'transition:all .15s'
    ].join(';');
    btn.addEventListener('mouseenter', () => { btn.style.color='#fff'; btn.style.background='rgba(255,255,255,0.16)'; });
    btn.addEventListener('mouseleave', () => { btn.style.color='#9ca3af'; btn.style.background='rgba(255,255,255,0.08)'; });
    btn.addEventListener('click', () => {
      const text = (code || pre).innerText.trim();
      copyToClipboard(text, () => {
        btn.innerHTML = '<i class="ph ph-check"></i>';
        btn.style.color = '#4ade80';
        setTimeout(() => { btn.innerHTML = '<i class="ph ph-copy"></i>'; btn.style.color = '#9ca3af'; }, 1500);
        showToast(HL.lang === 'en' ? 'Copied!' : '¡Copiado!');
      });
    });
    pre.appendChild(btn);
  });
  document.getElementById('resolution-modal').classList.remove('hidden');
  document.body.style.overflow = 'hidden';
}

function closeResolution() {
  document.getElementById('resolution-modal').classList.add('hidden');
  document.body.style.overflow = '';
}

document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeResolution();
});

// Double-click code blocks to copy
document.addEventListener('dblclick', e => {
  const target = e.target.closest('pre, code');
  if (!target) return;
  copyToClipboard(target.textContent.trim(), () => {
    showToast(HL.lang === 'en' ? 'Copied!' : '¡Copiado!');
  });
});

// ── Clipboard helper (works on HTTP + HTTPS) ─────────────────────
function copyToClipboard(text, onSuccess) {
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(text).then(onSuccess).catch(() => _fallbackCopy(text, onSuccess));
  } else {
    _fallbackCopy(text, onSuccess);
  }
}
function _fallbackCopy(text, onSuccess) {
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.style.cssText = 'position:fixed;left:-9999px;top:-9999px;opacity:0';
  document.body.appendChild(ta);
  ta.focus(); ta.select();
  try { if (document.execCommand('copy') && onSuccess) onSuccess(); } catch(e) {}
  document.body.removeChild(ta);
}

// ── Syntax highlighting ───────────────────────────────────────────
function detectLang(text) {
  if (/SELECT\s+|INSERT\s+|UPDATE\s+|DROP\s+/i.test(text)) return 'sql';
  if (/<\?xml|<!DOCTYPE|<\/\w+>/i.test(text))              return 'xml';
  if (/<html|<script|<div/i.test(text))                    return 'html';
  if (/^\s*\{[\s\S]*\}/m.test(text) && /":/.test(text))   return 'json';
  return 'bash';
}

function initCodeHighlight() {
  if (typeof hljs === 'undefined') return;

  // Configure hljs
  hljs.configure({ ignoreUnescapedHTML: true });

  // Transform .hl-code divs that contain <div> child lines
  document.querySelectorAll('.hl-code').forEach(el => {
    const divChildren = el.querySelectorAll(':scope > div');
    if (divChildren.length === 0) return; // Skip dynamic content

    const lines = [...divChildren].map(d => d.textContent);
    const rawText = lines.join('\n').trim();
    if (!rawText) return;

    const lang = el.dataset.lang || detectLang(rawText);

    const pre  = document.createElement('pre');
    const code = document.createElement('code');
    code.className = 'language-' + lang;
    code.textContent = rawText;
    pre.appendChild(code);
    pre.className = 'hljs-block';
    el.replaceWith(pre);
    hljs.highlightElement(code);
  });

  // Also highlight any <pre><code> blocks already in the DOM
  document.querySelectorAll('pre code:not(.hljs)').forEach(b => {
    if (!b.className) b.className = 'language-bash';
    hljs.highlightElement(b);
  });
}

// ── Custom Select Dropdown ────────────────────────────────────────
function initCustomSelects() {
  document.querySelectorAll('select.hl-input').forEach(native => {
    // Build wrapper
    const wrapper = document.createElement('div');
    wrapper.className = 'hl-select';

    // Trigger button
    const trigger = document.createElement('div');
    trigger.className = 'hl-select-trigger';
    trigger.setAttribute('tabindex', '0');

    const label = document.createElement('span');
    label.className = 'hl-select-label';
    const selectedOpt = native.options[native.selectedIndex];
    label.textContent = selectedOpt ? selectedOpt.text : '';

    // Caret SVG
    const caret = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    caret.setAttribute('viewBox', '0 0 24 24');
    caret.setAttribute('fill', 'none');
    caret.setAttribute('stroke', 'currentColor');
    caret.setAttribute('stroke-width', '2');
    caret.setAttribute('stroke-linecap', 'round');
    caret.setAttribute('stroke-linejoin', 'round');
    caret.classList.add('hl-select-caret');
    const poly = document.createElementNS('http://www.w3.org/2000/svg', 'polyline');
    poly.setAttribute('points', '6 9 12 15 18 9');
    caret.appendChild(poly);

    trigger.appendChild(label);
    trigger.appendChild(caret);

    // Menu
    const menu = document.createElement('div');
    menu.className = 'hl-select-menu';
    menu.style.display = 'none';

    Array.from(native.options).forEach((opt, i) => {
      const item = document.createElement('div');
      item.className = 'hl-select-option' + (i === native.selectedIndex ? ' selected' : '');
      item.textContent = opt.text;
      item.dataset.value = opt.value;
      item.addEventListener('click', () => {
        native.value = opt.value;
        label.textContent = opt.text;
        menu.querySelectorAll('.hl-select-option').forEach(o => o.classList.remove('selected'));
        item.classList.add('selected');
        closeMenu();
        // Dispatch change event so any listeners on native select fire
        native.dispatchEvent(new Event('change', { bubbles: true }));
      });
      menu.appendChild(item);
    });

    function openMenu() {
      menu.style.display = '';
      trigger.classList.add('open');
    }
    function closeMenu() {
      menu.style.display = 'none';
      trigger.classList.remove('open');
    }
    function toggleMenu(e) {
      e.stopPropagation();
      menu.style.display === 'none' ? openMenu() : closeMenu();
    }

    trigger.addEventListener('click', toggleMenu);
    trigger.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggleMenu(e); }
      if (e.key === 'Escape') closeMenu();
    });

    wrapper.appendChild(trigger);
    wrapper.appendChild(menu);

    // Insert wrapper before native select, native stays hidden via CSS
    native.parentNode.insertBefore(wrapper, native);
  });

  // Close all menus when clicking outside
  document.addEventListener('click', () => {
    document.querySelectorAll('.hl-select-menu').forEach(m => {
      m.style.display = 'none';
      const trigger = m.previousElementSibling;
      if (trigger) trigger.classList.remove('open');
    });
  });
}

// ── Sidebar search/filter ─────────────────────────────────────────
function initSidebarSearch() {
  const input = document.getElementById('sidebar-search');
  if (!input) return;

  input.addEventListener('input', (e) => {
    const q = (e.target.value || '').trim().toLowerCase();

    const items = document.querySelectorAll('.sidebar-item');
    // If query empty, restore default visibility and category collapsed state
    if (!q) {
      items.forEach(i => i.style.display = '');
      document.querySelectorAll('.sidebar-category').forEach(cat => cat.style.display = '');
      initCategories();
      return;
    }

    // Filter items and show/hide categories accordingly
    document.querySelectorAll('.sidebar-category').forEach(cat => {
      const catItems = cat.querySelectorAll('.sidebar-item');
      let anyVisible = false;
      catItems.forEach(it => {
        const txt = (it.textContent || it.innerText || '').toLowerCase();
        if (txt.indexOf(q) !== -1) {
          it.style.display = '';
          anyVisible = true;
        } else {
          it.style.display = 'none';
        }
      });
      // show category header only if it has matches
      cat.style.display = anyVisible ? '' : 'none';
      // expand category if it has matches
      const itemsEl = cat.querySelector('.sidebar-cat-items');
      if (itemsEl && anyVisible) itemsEl.classList.remove('collapsed');
    });
  });

}

// ── Toast ─────────────────────────────────────────────────────────
function showToast(msg) {
  const el = document.createElement('div');
  el.innerHTML = '<i class="ph ph-check-circle" style="font-size:1rem"></i><span>' + msg + '</span>';
  el.style.cssText = 'position:fixed;bottom:5rem;right:1.75rem;background:var(--hl-primary);color:var(--hl-on-primary);font-size:.75rem;font-weight:700;padding:.5rem 1rem;border-radius:.75rem;z-index:9999;font-family:Inter,sans-serif;box-shadow:0 4px 20px rgba(0,0,0,.3);transition:opacity .3s;display:flex;align-items:center;gap:.5rem';
  document.body.appendChild(el);
  setTimeout(() => el.style.opacity = '0', 1800);
  setTimeout(() => el.remove(), 2200);
}

// ── Reward overlays ─────────────────────────────────────────────
function showLevelUpOverlay(level, levelName, levelIcon, opts = {}) {
  if (document.getElementById('levelup-overlay')) return;
  const isEn = (typeof HL !== 'undefined' && HL.lang === 'en');
  let done = false;

  const overlay = document.createElement('div');
  overlay.id = 'levelup-overlay';

  let particlesHTML = '';
  const angles = [0,18,36,54,72,90,108,126,144,162,180,198,216,234,252,270,288,306,324,342];
  angles.forEach((deg, i) => {
    const rad  = deg * Math.PI / 180;
    const dist = 120 + Math.random() * 140;
    const dx   = Math.round(Math.cos(rad) * dist);
    const dy   = Math.round(Math.sin(rad) * dist);
    const size = 3 + Math.random() * 5;
    const delay = (i * 0.018).toFixed(3);
    const dur   = (0.55 + Math.random() * 0.45).toFixed(2);
    particlesHTML += `<div class="lu-particle" style="
      width:${size.toFixed(1)}px;height:${size.toFixed(1)}px;
      top:50%;left:50%;
      --dx:${dx}px;--dy:${dy}px;
      animation:lu-particle-burst ${dur}s ease ${delay}s both;
      opacity:${(0.5 + Math.random() * 0.5).toFixed(2)};
    "></div>`;
  });

  const lvlLabel  = `LVL ${level + 1}`;
  const titleText = 'LEVEL UP';
  const accessTxt = isEn ? '// ACCESS GRANTED //' : '// ACCESO CONCEDIDO //';
  const btnLabel  = isEn ? 'Continue' : 'Continuar';
  const hintTxt   = isEn ? 'Click to continue' : 'Haz clic para continuar';
  const iconClass = levelIcon || 'ph-graduation-cap';

  function finish() {
    if (done) return;
    done = true;
    overlay.remove();
    if (typeof opts.onDone === 'function') opts.onDone();
  }

  overlay.innerHTML = `
    <div class="levelup-card">
      ${particlesHTML}
      <div class="levelup-access">${accessTxt}</div>
      <div class="levelup-title">${titleText}</div>
      <div class="levelup-icon-circle"><i class="ph ${iconClass}"></i></div>
      <div class="levelup-lvl-badge">${lvlLabel}</div>
      <div class="levelup-name">${levelName}</div>
      <div>
        <button class="levelup-btn" onclick="event.stopPropagation();">
          <i class="ph ph-arrow-square-right" style="font-size:1rem"></i>${btnLabel}
        </button>
      </div>
      <div class="levelup-hint">${hintTxt}</div>
    </div>`;

  overlay.addEventListener('click', finish);
  const btn = overlay.querySelector('.levelup-btn');
  if (btn) btn.addEventListener('click', finish);
  document.body.appendChild(overlay);
  setTimeout(finish, opts.timeout || 4200);
}

function showBadgeOverlay(badge, opts = {}) {
  if (document.getElementById('badgeup-overlay')) return;
  const isEn = (typeof HL !== 'undefined' && HL.lang === 'en');
  let done = false;
  const overlay = document.createElement('div');
  overlay.id = 'badgeup-overlay';

  const title = isEn ? 'NEW BADGE' : 'NUEVO BADGE';
  const subtitle = isEn ? 'Achievement unlocked' : 'Logro desbloqueado';
  const btnLabel = isEn ? 'Continue' : 'Continuar';
  const hintTxt = isEn ? 'Click to continue' : 'Haz clic para continuar';

  function finish() {
    if (done) return;
    done = true;
    overlay.remove();
    if (typeof opts.onDone === 'function') opts.onDone();
  }

  overlay.innerHTML = `
    <div class="badgeup-card">
      <div class="badgeup-access">// ${subtitle.toUpperCase()} //</div>
      <div class="badgeup-title">${title}</div>
      <div class="badgeup-icon-circle">${badge.icon || '🏆'}</div>
      <div class="badgeup-name">${badge.name || 'Badge'}</div>
      <div>
        <button class="levelup-btn" onclick="event.stopPropagation();">
          <i class="ph ph-arrow-square-right" style="font-size:1rem"></i>${btnLabel}
        </button>
      </div>
      <div class="levelup-hint">${hintTxt}</div>
    </div>`;

  overlay.addEventListener('click', finish);
  const btn = overlay.querySelector('.levelup-btn');
  if (btn) btn.addEventListener('click', finish);
  document.body.appendChild(overlay);
  setTimeout(finish, opts.timeout || 3200);
}

function playProgressUnlockSequence(data, fallbackToast) {
  const queue = [];

  if (data.level_up) {
    queue.push((next) => showLevelUpOverlay(
      data.new_level,
      data.new_level_name,
      data.new_level_icon,
      { onDone: next, timeout: 4200 }
    ));
  }

  if (Array.isArray(data.new_badges) && data.new_badges.length > 0) {
    data.new_badges.forEach((badge) => {
      queue.push((next) => showBadgeOverlay(badge, { onDone: next, timeout: 3200 }));
    });
  }

  if (!queue.length) {
    if (fallbackToast) showToast(fallbackToast);
    return;
  }

  let idx = 0;
  const runNext = () => {
    if (idx >= queue.length) {
      window.location.href = '/progress';
      return;
    }
    const step = queue[idx++];
    step(runNext);
  };
  runNext();
}

// ── Init ─────────────────────────────────────────────────────────
(function init() {
  applyTheme();
  applySidebar();
  initCategories();
  applyTranslations();
  initCodeHighlight();
  initCustomSelects();
  // initialize custom language dropdown (styles+handlers)
  try { initLangDropdown(); } catch(e) {}
  initSidebarSearch();

  // Dynamic footer year
  const fy = document.getElementById('footer-year');
  if (fy) fy.textContent = new Date().getFullYear();

  // Show global FAB only on pages that have resolution data
  const fab = document.getElementById('global-fab');
  if (fab && document.getElementById('resolution-data')) {
    fab.style.display = '';
  }

  // Mark active sidebar item and scroll it into view
  const path = window.location.pathname;
  document.querySelectorAll('.sidebar-item').forEach(el => {
    if (el.getAttribute('href') === path) {
      el.classList.add('active');
      el.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
  });
})();

// Re-apply after full page load (ensures Phosphor Icons and other libs are done)
window.addEventListener('load', applyTranslations);

// ── Progress system ───────────────────────────────────────────

function _updateProgressUI(data) {
  // Update progress ring values
  const label = document.querySelector('.progress-ring-label');
  const fill  = document.querySelector('.progress-ring-fill');
  const ring  = document.getElementById('nav-progress-ring');
  if (label && fill && data.total > 0) {
    const circ   = 87.96;
    const offset = circ * (1 - data.count / data.total);
    fill.setAttribute('stroke-dashoffset', offset.toFixed(2));
    // Update label text (keep /total span)
    label.innerHTML = data.count + '<span class="progress-ring-total">/' + data.total + '</span>';
    if (ring) ring.title = 'Mi progreso: ' + data.count + '/' + data.total + ' labs completados';
  }
}

function submitLabFlag(labId) {
  const btn = document.getElementById('lab-complete-btn');
  const input = document.getElementById('lab-flag-input');
  if (!btn || !input) return;

  // If already completed, allow user to unmark and re-exploit the lab.
  if (btn.classList.contains('lab-complete-btn--done')) {
    btn.classList.add('animating');
    setTimeout(() => btn.classList.remove('animating'), 200);

    fetch('/progress/uncomplete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ lab_id: labId })
    })
    .then(r => r.json())
    .then(data => {
      if (data.error) {
        showToast('No se pudo desmarcar el lab');
        return;
      }
      btn.classList.remove('lab-complete-btn--done');
      const icon = btn.querySelector('i');
      const span = btn.querySelector('span');
      if (icon) icon.className = 'ph ph-flag-checkered text-sm';
      if (span) span.textContent = 'Validar flag';
      btn.title = 'Validar flag del laboratorio';
      input.disabled = false;
      input.value = '';
      _updateProgressUI(data);
      showToast('Lab desmarcado. Puedes volver a explotarlo');
    })
    .catch(() => {});
    return;
  }

  if (input.disabled) return;
  const flag = (input.value || '').trim();
  if (!flag) {
    showToast('Introduce una flag valida (ej: HL{...})');
    return;
  }

  btn.classList.add('animating');
  setTimeout(() => btn.classList.remove('animating'), 200);

  fetch('/progress/submit-flag', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ lab_id: labId, flag: flag })
  })
  .then(r => r.json())
  .then(data => {
    if (data.error) {
      if (data.error === 'invalid_flag') showToast('Flag incorrecta');
      else if (data.error === 'empty_flag') showToast('Introduce una flag');
      else if (data.error === 'flag_required') showToast('Este lab solo se completa con flag valida');
      else showToast('No se pudo validar la flag');
      return;
    }

    const done = !!data.completed;
    btn.classList.add('lab-complete-btn--done');
    const icon = btn.querySelector('i');
    const span = btn.querySelector('span');
    if (icon) icon.className = 'ph ph-arrow-counter-clockwise text-sm';
    if (span) span.textContent = 'Desmarcar';
    btn.title = 'Desmarcar lab como completado';
    input.disabled = true;
    input.value = flag;
    _updateProgressUI(data);
    if (done) {
      playProgressUnlockSequence(data, 'Flag correcta. Lab completado');
    } else {
      showToast('Flag validada');
    }
  })
  .catch(() => {});
}
