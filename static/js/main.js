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
    csrf_btn_change: 'Cambiar contraseña',
    csrf_attack_title: 'Ataque CSRF — Auto-envío',
    csrf_victim_id:  'ID de usuario víctima',
    csrf_btn_launch: 'Lanzar CSRF',
    // File Upload
    upload_dropzone: 'Haz clic o arrastra un archivo aquí',
    upload_no_restrict: 'Sin restricciones de tipo de archivo',
    upload_btn:      'Subir archivo',
    upload_open:     'Abrir archivo',
    upload_list:     'Archivos subidos (/uploads/)',
    upload_access:   'Acceder →',
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
    csrf_btn_change: 'Change Password',
    csrf_attack_title: 'CSRF Attack — Auto-submit',
    csrf_victim_id:  'Victim User ID',
    csrf_btn_launch: 'Launch CSRF',
    // File Upload
    upload_dropzone: 'Click or drag file here',
    upload_no_restrict: 'No file type restrictions',
    upload_btn:      'Upload',
    upload_open:     'Open file',
    upload_list:     'Uploaded files (/uploads/)',
    upload_access:   'Access →',
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

function setLang(lang) {
  HL.lang = lang;
  localStorage.setItem('hl_lang', lang);
  applyTranslations();
  // Re-apply resolution lang if modal is open
  if (!document.getElementById('resolution-modal').classList.contains('hidden')) {
    applyResolutionLang('#modal-body');
  }
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

// ── Init ─────────────────────────────────────────────────────────
(function init() {
  applyTheme();
  applySidebar();
  initCategories();
  applyTranslations();
  initCodeHighlight();
  initCustomSelects();
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
