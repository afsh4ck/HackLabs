#!/usr/bin/env python3
"""Script de inicialización de la base de datos de HackLabs."""

import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), 'data', 'hacklabs.db')
SCHEMA   = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')

def init():
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
        print("[-] Base de datos anterior eliminada.")

    db = sqlite3.connect(DATABASE)
    with open(SCHEMA, 'r', encoding='utf-8') as f:
        db.executescript(f.read())
    db.commit()
    db.close()
    print("[+] Base de datos inicializada correctamente.")
    print(f"    Ruta: {DATABASE}")

    # Crear carpetas necesarias
    for d in ['uploads', 'logs', os.path.join('static', 'files')]:
        os.makedirs(os.path.join(os.path.dirname(__file__), d), exist_ok=True)

    # Crear archivo de texto de ejemplo para Path Traversal
    sample = os.path.join(os.path.dirname(__file__), 'static', 'files', 'readme.txt')
    with open(sample, 'w') as f:
        f.write("Archivo de ejemplo de HackLabs.\nPrueba: /files?file=readme.txt\n")

    print("[+] Directorios y archivos de ejemplo creados.")

if __name__ == '__main__':
    init()
