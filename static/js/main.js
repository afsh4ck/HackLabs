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
    cat_owasp_top_10:'OWASP Top 10',
    cat_extras:      'Extras',
    labs:            'Labs',
    resolution_steps:'Pasos de explotación',
    tools_label:     'Herramientas',
    // Home
    badge_text:      'Intencionalmente Vulnerable · Solo uso educativo',
    filter_label:    'Filtrar:',
    filter_all:      'Todos',
    open_lab:        'Abrir lab',
    test_credentials:'Credenciales de prueba',
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
  },
  en: {
    home:            'Home',
    logout:          'Log out',
    footer_warning:  'For educational use in isolated environments only',
    modal_title:     'Lab Resolution',
    btn_resolution:  'View Resolution',
    close:           'Close',
    cat_owasp_top_10:'OWASP Top 10',
    cat_extras:      'Extras',
    labs:            'Labs',
    resolution_steps:'Exploitation Steps',
    tools_label:     'Tools',
    // Home
    badge_text:      'Intentionally Vulnerable · Educational Use Only',
    filter_label:    'Filter:',
    filter_all:      'All',
    open_lab:        'Open lab',
    test_credentials:'Test Credentials',
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
    if (val === undefined) return; // Never show raw key strings

    if (el.tagName === 'INPUT' && el.type !== 'submit') {
      el.placeholder = val;
    } else if (el.children.length === 0) {
      // Leaf node — safe to set textContent directly
      el.textContent = val;
    } else {
      // Has child elements (e.g. icons): update only direct text nodes
      [...el.childNodes].forEach(node => {
        if (node.nodeType === Node.TEXT_NODE && node.textContent.trim()) {
          node.textContent = ' ' + val;
        }
      });
    }
  });

  // Sync lang button active states
  ['es', 'en'].forEach(l => {
    const btn = document.getElementById('lang-' + l);
    if (btn) btn.classList.toggle('active-lang', l === HL.lang);
  });

  applyResolutionLang('#modal-body');
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
  if (!sb) return;
  sb.classList.toggle('sidebar-open',   HL.sidebar);
  sb.classList.toggle('sidebar-closed', !HL.sidebar);
  iOp && iOp.classList.toggle('hidden',  HL.sidebar);
  iCl && iCl.classList.toggle('hidden', !HL.sidebar);
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
  // Highlight code inside modal
  body.querySelectorAll('pre code').forEach(b => {
    if (typeof hljs !== 'undefined') hljs.highlightElement(b);
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
  navigator.clipboard.writeText(target.textContent.trim()).then(() => {
    showToast(HL.lang === 'en' ? 'Copied!' : '¡Copiado!');
  }).catch(() => {});
});

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
