-- HackLabs Database Schema
-- Datos de prueba para practicar vulnerabilidades web

CREATE TABLE IF NOT EXISTS users (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    username        TEXT NOT NULL UNIQUE,
    email           TEXT NOT NULL,
    password_plain  TEXT NOT NULL,
    password_md5    TEXT NOT NULL,
    role            TEXT NOT NULL DEFAULT 'user',
    security_question TEXT,
    security_answer TEXT,
    phone           TEXT,
    address         TEXT,
    credit_card     TEXT,
    ssn             TEXT,
    is_system_user  INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS products (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    description TEXT,
    price       REAL,
    category    TEXT
);

CREATE TABLE IF NOT EXISTS comments (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    author  TEXT NOT NULL,
    body    TEXT NOT NULL,
    created TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS orders (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER,
    product_id INTEGER,
    quantity   INTEGER,
    total      REAL,
    created    TEXT DEFAULT (datetime('now'))
);

-- ─────────────────────────────────────────────
-- Usuarios de prueba
-- Contraseñas en texto plano y MD5 (intencionalmente inseguro)
-- admin:admin123  →  MD5: 0192023a7bbd73250516f069df18b500
-- alice:password  →  MD5: 5f4dcc3b5aa765d61d8327deb882cf99
-- bob:123456      →  MD5: e10adc3949ba59abbe56e057f20f883e
-- charlie:qwerty  →  MD5: d8578edf8458ce06fbc5bb76a58c5ca4
-- ─────────────────────────────────────────────

INSERT OR IGNORE INTO users (id, username, email, password_plain, password_md5, role, security_question, security_answer, phone, address, credit_card, ssn, is_system_user)
VALUES
(1, 'admin',   'admin@hacklabs.local',   'admin123', '0192023a7bbd73250516f069df18b500', 'admin',   '¿Cuál es el nombre de tu mascota?', 'rex',     '+34 600 000 001', 'Calle Mayor 1, Madrid',  '4111111111111111', '111-22-3333', 1),
(2, 'alice',   'alice@hacklabs.local',   'password', '5f4dcc3b5aa765d61d8327deb882cf99', 'user',    '¿Cuál es el nombre de tu mascota?', 'fluffy',  '+34 600 000 002', 'Av. Libertad 22, BCN',   '4222222222222222', '222-33-4444', 1),
(3, 'bob',     'bob@hacklabs.local',     '123456',   'e10adc3949ba59abbe56e057f20f883e', 'user',    '¿Ciudad donde naciste?',            'sevilla', '+34 600 000 003', 'C/ Rosas 7, Sevilla',    '4333333333333333', '333-44-5555', 1),
(4, 'charlie', 'charlie@hacklabs.local', 'qwerty',   'd8578edf8458ce06fbc5bb76a58c5ca4', 'user',    '¿Nombre de tu primera escuela?',    'ceip',    '+34 600 000 004', 'Pl. España 3, Valencia', '4444444444444444', '444-55-6666', 1),
(5, 'dave',    'dave@hacklabs.local',    'letmein',  '0d107d09f5bbe40cade3de5c71e9e9b7', 'manager', '¿Cuál es el nombre de tu mascota?', 'max',     '+34 600 000 005', 'Gran Vía 100, Madrid',   '4555555555555555', '555-66-7777', 1);

-- Productos de prueba para SQL Injection
INSERT OR IGNORE INTO products (id, name, description, price, category) VALUES
(1, 'Kali Linux USB',      'Pendrive booteable con Kali Linux 2024',         29.99, 'hardware'),
(2, 'Rubber Ducky',        'USB HID attack tool – Hak5',                     49.99, 'hardware'),
(3, 'Flipper Zero',        'Dispositivo de pruebas de radiofrecuencia',      169.99, 'hardware'),
(4, 'Metasploit Pro',      'Framework de explotación profesional',           499.00, 'software'),
(5, 'Burp Suite Pro',      'Proxy de interceptación y escaneo web',          449.00, 'software'),
(6, 'WiFi Pineapple',      'Auditoría de redes WiFi',                         99.99, 'hardware'),
(7, 'HackRF One',          'SDR de propósito general',                       299.99, 'hardware'),
(8, 'Maltego Pro',         'OSINT y análisis de grafos',                     999.00, 'software'),
(9, 'Nessus Essentials',   'Escáner de vulnerabilidades',                      0.00, 'software'),
(10,'OSCP Certification',  'Certificación Offensive Security',               1499.00, 'training'),
(11,'Pentesting Toolkit',  'Kit completo de herramientas para testing',        59.99, 'accessories');

-- Comentarios iniciales para XSS stored
INSERT OR IGNORE INTO comments (id, author, body) VALUES
(1, 'admin', 'Bienvenidos al foro de HackLabs. ¡Practica con responsabilidad!'),
(2, 'alice', 'Excelente plataforma para aprender ethical hacking.'),
(3, 'bob',   'Probando el laboratorio de XSS almacenado.');

-- Órdenes de prueba
INSERT OR IGNORE INTO orders (user_id, product_id, quantity, total) VALUES
(2, 1, 1, 29.99),
(2, 5, 1, 449.00),
(3, 2, 2, 99.98),
(1, 4, 1, 499.00);
