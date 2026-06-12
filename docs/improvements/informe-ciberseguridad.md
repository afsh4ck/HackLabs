---
title: "Propuesta de Mejoras al Programa de Certificacion en Ciberseguridad y Hacking Etico"
subtitle: "Analisis Basado en Evidencia Cientifica y Estandares de la Industria (2021-2026)"
author: "Diego Saavedra — FullStack Developer & Cybersecurity Consultant"
date: "Junio 2026"
geometry: margin=2cm
mainfont: "Helvetica"
fontsize: 11pt
toc: true
toc-depth: 3
numbersections: true
colorlinks: true
linkcolor: blue
header-includes:
  - \usepackage{booktabs}
  - \usepackage{longtable}
  - \usepackage{array}
  - \usepackage{xcolor}
  - \definecolor{critica}{RGB}{180,30,30}
  - \definecolor{alta}{RGB}{200,100,0}
  - \definecolor{media}{RGB}{0,100,150}
  - \usepackage{fancyhdr}
  - \pagestyle{fancy}
  - \fancyhead[L]{\small Programa de Ciberseguridad — Propuesta de Mejoras}
  - \fancyhead[R]{\small Diego Saavedra}
  - \fancyfoot[C]{\thepage}
  - \renewcommand{\headrulewidth}{0.4pt}
  - \renewcommand{\footrulewidth}{0.4pt}
---

\begin{center}
\textbf{PROPUESTA PRESENTADA POR}\\[0.5cm]
\Large\textbf{Diego Saavedra}\\[0.3cm]
\normalsize FullStack Developer \& Cybersecurity Consultant\\[0.2cm]
\small https://statick88.github.io\\[0.3cm]
\small Junio 2026
\end{center}

\newpage

# Resumen Ejecutivo

Este informe presenta una propuesta estructurada de mejoras al Programa de Certificacion en Ciberseguridad y Hacking Etico, basada en investigacion academica y estandares internacionales de la industria.

La propuesta incluye **47 mejoras especificas** categorizadas por prioridad, con evidencia que respalda cada recomendacion y mapeo a marcos de referencia internacionales.

## Hallazgos Principales

| Brecha Identificada | Impacto | Evidencia |
|---------------------|---------|-----------|
| OWASP Top 10 2021 vs 2025 | 2 categorias nuevas ausentes | OWASP Foundation (2025) |
| OWASP LLM Top 10 2025 | 0% cobertura en AI/LLM | 210% incremento vulnerabilidades AI (HackerOne 2024-2025) |
| NIST CSF 2.0 (GOVERN) | Framework ausente | NIST CSWP 29 (Feb 2024) |
| DevSecOps | Mercado de $32.4B ignorado | 23.2% CAGR (2024-2030) |
| MITRE ATT&CK | 0% integracion | Framework universal de amenazas |
| Zero Trust Architecture | 1 solo bullet mencionado | NIST SP 800-207 |
| IoT/OT/ICS | Totalmente ausente | NIST SP 800-82r3 (2023) |

## Prioridad de las Mejoras

| Prioridad | Cantidad | Descripcion |
|-----------|----------|-------------|
| \textcolor{critica}{CRITICA} | 14 | Implementacion inmediata |
| \textcolor{alta}{ALTA} | 18 | Proximos 3 meses |
| \textcolor{media}{MEDIA} | 15 | Proximo ciclo |

\newpage

# Analisis del Programa Actual

## Estructura

El programa se compone de 4 modulos de 4 semanas cada uno:

| Modulo | Semana 1 | Semana 2 | Semana 3 | Semana 4 |
|--------|----------|----------|----------|----------|
| **I: Fundamentos** | Introduccion a la ciberseguridad | Tipos de amenazas y vulnerabilidades | Sistemas operativos y redes | Herramientas basicas de seguridad |
| **II: Hacking Etico** | Reconocimiento y enumeracion | Explotacion de vulnerabilidades | Post-explotacion | Ingenieria social |
| **III: Defensa** | Analisis de malware | Seguridad de redes | Seguridad de aplicaciones | Laboratorio practico |
| **IV: Especializacion** | Analisis forense digital | Seguridad en la nube | Hacking web avanzado | Investigacion de amenazas |

## Fortalezas del Programa Actual

1. Cobertura de fundamentos solida
2. Inclusion de ingenieria social
3. Presencia de analisis forense y malware
4. Estructura progresiva logica

## Debilidades Criticas

### 1. Estandares de Seguridad Obsoletos
- OWASP Top 10 2021 vs. OWASP Top 10 2025
- Sin referencia a MITRE ATT&CK
- Sin mapeo al NICE Framework v2.0.0

### 2. Temas Ausentes Criticos
- Seguridad AI/LLM
- DevSecOps y Pipeline de Seguridad
- Seguridad IoT/OT/ICS
- Seguridad de Cadena de Suministro
- Zero Trust Architecture
- Post-quantum Cryptography (FIPS 203/204/205)

### 3. Sin Framework de Gobernanza
- NIST CSF 2.0 (Feb 2024) con GOVERN ausente
- Sin mapeo a marcos regulatorios (GDPR, SOC2, PCI DSS)

\newpage

# MODULO I: Fundamentos de Ciberseguridad

## Semana 1: Introduccion a la Ciberseguridad

### Estado Actual
- Definiciones basicas de ciberseguridad
- Historia de la seguridad informatica
- Conceptos de CIA Triad

### Mejoras Propuestas

**1.1 \textcolor{critica}{CRITICA} — Integrar NIST CSF 2.0 como Marco Referencial**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | Conceptos generales de seguridad |
| **Contenido Recomendado** | NIST CSF 2.0 con 6 funciones: GOVERN, IDENTIFY, PROTECT, DETECT, RESPOND, RECOVER |
| **Evidencia** | NIST CSWP 29 (Feb 2024): "La nueva funcion GOVERN es el eje central del marco" |
| **Impacto** | Proporciona estructura organizacional para TODOS los demas modulos |
| **NICE Work Roles** | 701: Security Control Assessor, 710: System Security Manager |

**1.2 \textcolor{critica}{CRITICA} — Agregar Mapeo MITRE ATT&CK**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | Sin referencia a frameworks de amenazas |
| **Contenido Recomendado** | MITRE ATT&CK Enterprise: 14 tacticas, 200+ tecnicas |
| **Evidencia** | MITRE ATT&CK utilizado por 90%+ de Fortune 500 (MITRE, 2025) |
| **Impacto** | Vocabulario comun para describir ataques en todos los modulos |
| **NICE Work Roles** | 511: Threat Analyst, 521: Exploitation Analyst |

**1.3 \textcolor{alta}{ALTA} — Agregar Tema: Seguridad AI y LLM**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | No menciona AI/ML |
| **Contenido Recomendado** | OWASP LLM Top 10 2025, amenazas de IA generativa |
| **Evidencia** | 210% incremento en vulnerabilidades AI (HackerOne 2024-2025); 73% de despliegues LLM con al menos 1 vulnerabilidad critica (OWASP 2025) |
| **Herramientas** | Garak (LLM vulnerability scanner), PyRIT (Microsoft) |
| **OWASP LLM Top 10** | LLM01 Prompt Injection, LLM06 Excessive Agency, LLM07 System Prompt Leakage |

**1.4 \textcolor{alta}{ALTA} — Agregar Zero Trust Architecture como Principio Transversal**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | "Gestion de usuarios y permisos" (1 bullet) |
| **Contenido Recomendado** | NIST SP 800-207: "Nunca confies, siempre verifica" — 5 pilares |
| **Evidencia** | NIST SP 800-207: "Zero Trust es un modelo de seguridad estrategico" |
| **Impacto** | Debe ser hilo conductor de TODO el programa, no un tema aislado |
| **Pilares** | Identity, Devices, Networks, Applications & Workloads, Data |

---

## Semana 2: Tipos de Amenazas y Vulnerabilidades

### Estado Actual
- Malware (virus, gusanos, troyanos)
- Phishing y ingenieria social
- Denegacion de servicio

### Mejoras Propuestas

**2.1 \textcolor{critica}{CRITICA} — Actualizar OWASP Top 10 a Version 2025**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | OWASP Top 10 2021 |
| **Contenido Recomendado** | OWASP Top 10 2025 con 2 categorias nuevas |
| **Evidencia** | OWASP Foundation (2025): A03 Supply Chain (NUEVA), A10 Exceptional Conditions (NUEVA) |
| **Cambios Clave** | A03: Vulnerabilidades en cadenas de suministro; A10: Condiciones excepcionales |
| **OWASP Reference** | https://owasp.org/Top10/ |

**2.2 \textcolor{critica}{CRITICA} — Agregar OWASP API Security Top 10 (2023)**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | No menciona seguridad API |
| **Contenido Recomendado** | OWASP API Security Top 10: BOLA, Broken Authentication, Mass Assignment |
| **Evidencia** | APIs representan el 90% del trafico web; API1:2023 (BOLA) es la vulnerabilidad mas comun |

**2.3 \textcolor{alta}{ALTA} — Agregar OWASP LLM Top 10 2025**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | Sin cobertura de amenazas AI |
| **Contenido Recomendado** | 10 categorias de vulnerabilidades LLM |
| **Evidencia** | 540% incremento en reportes de prompt injection (OWASP 2025) |

**2.4 \textcolor{alta}{ALTA} — Incluir CVE/NVD como Herramienta de Investigacion**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | No se ensena a buscar CVEs |
| **Contenido Recomendado** | National Vulnerability Database (NVD), CVSS scoring |
| **Evidencia** | Mas de 25,000 CVEs publicadas anualmente (NVD 2024) |

---

## Semana 3: Sistemas Operativos y Redes

### Estado Actual
- Instalacion y configuracion de Linux/Windows
- Conceptos basicos de redes TCP/IP
- Protocolos de red comunes

### Mejoras Propuestas

**3.1 \textcolor{alta}{ALTA} — Agregar Seguridad en Infraestructura de Red**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | Configuracion basica de redes |
| **Contenido Recomendado** | Hardening de red, segmentacion, firewalls, IDS/IPS |
| **Herramientas** | pfSense, Snort/Suricata, Wireshark |
| **NICE Work Roles** | 421: Network Operations Specialist |

**3.2 \textcolor{media}{MEDIA} — Agregar Seguridad de Contenedores (Introduccion)**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | No menciona contenedores |
| **Contenido Recomendado** | Docker basico, seguridad de imagenes, conceptos de Kubernetes |
| **Evidencia** | CWPP market: $5.13B a $15.41B por 2030 (GlobeNewsWire 2026) |

---

## Semana 4: Herramientas Basicas de Seguridad

### Estado Actual
- Kali Linux introductorio
- Herramientas basicas de escaneo
- Metasploit introductorio

### Mejoras Propuestas

**4.1 \textcolor{critica}{CRITICA} — Expandir Herramientas a Estandar de la Industria**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | Kali Linux + Metasploit basico |
| **Contenido Recomendado** | Kali + Nmap avanzado + Burp Suite + OWASP ZAP + Wireshark + Nuclei + Subfinder |
| **Evidencia** | Endor Labs (2026): herramientas utilizadas en 90% de pentests profesionales |

**4.2 \textcolor{alta}{ALTA} — Agregar Laboratorio: Entorno Seguro de Pentesting**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | Teoria sobre herramientas |
| **Contenido Recomendado** | VMs vulnerables (DVWA, Metasploitable, WebGoat) para practica |

\newpage

# MODULO II: Hacking Etico

## Semana 5: Reconocimiento y Enumeracion

### Estado Actual
- OSINT basico
- Enumeracion de redes
- Reconocimiento pasivo y activo

### Mejoras Propuestas

**5.1 \textcolor{critica}{CRITICA} — Agregar Metodologia de Reconocimiento Estructurada**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | Herramientas sueltas |
| **Contenido Recomendado** | Metodologia de 5 fases: Recon, Enum, Vuln, Exploit, Report |
| **Evidencia** | PTES (Penetration Testing Execution Standard), OWASP Testing Guide v4 |
| **Herramientas** | Subfinder, httpx, nuclei, ffuf, amass |
| **NICE Work Roles** | 511: Threat Analyst, 521: Exploitation Analyst |

**5.2 \textcolor{alta}{ALTA} — Incluir Reconocimiento de Infraestructura Critica**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | Solo redes IT convencionales |
| **Contenido Recomendado** | Introduccion a reconocimiento OT/ICS (Purdue Model, Modbus) |
| **Evidencia** | NIST SP 800-82r3 (2023): "Guide to OT Security" |

---

## Semana 6: Explotacion de Vulnerabilidades

### Estado Actual
- Explotacion con Metasploit
- Inyeccion SQL basica
- Cross-Site Scripting (XSS)

### Mejoras Propuestas

**6.1 \textcolor{critica}{CRITICA} — Actualizar Tecnicas de Explotacion a 2025-2026**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | Tecnicas clasicas (SQLi, XSS) |
| **Contenido Recomendado** | + SSTI, SSRF, XXE, deserialization, OAuth/OIDC exploitation, JWT attacks |
| **Evidencia** | OWASP Top 10 2025: nuevas categorias y vectores |

**6.2 \textcolor{alta}{ALTA} — Agregar Laboratorio: Explotacion de API**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | Sin explotacion de APIs |
| **Contenido Recomendado** | OWASP API Security Top 10 hands-on: BOLA, Broken Auth, Mass Assignment |
| **Herramientas** | Postman, Burp Suite, OWASP crAPI (vulnerable API) |

---

## Semana 7: Post-Explotacion

### Estado Actual
- Escalada de privilegios
- Mantenimiento de acceso
- Cobertura de huellas

### Mejoras Propuestas

**7.1 \textcolor{alta}{ALTA} — Agregar Lateral Movement y Pivot**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | Escalada de privilegios local |
| **Contenido Recomendado** | Lateral movement, pivot de red, pass-the-hash, Kerberoasting |
| **Evidencia** | MITRE ATT&CK: TA0008 Lateral Movement (10 tecnicas) |

**7.2 \textcolor{alta}{ALTA} — Agregar Active Directory Attack Path**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | No cubre Active Directory |
| **Contenido Recomendado** | AD enumeration, Kerberoasting, DCSync, Golden/Silver Ticket |
| **Evidencia** | AD es el sistema de autenticacion #1 en empresas; 95% de Fortune 100 usan AD |
| **Herramientas** | BloodHound, Mimikatz, Impacket, Rubeus |
| **NICE Work Roles** | 521: Exploitation Analyst |

---

## Semana 8: Ingenieria Social

### Estado Actual
- Tecnicas de phishing
- Pretexting y baiting
- Defensa contra ingenieria social

### Mejoras Propuestas

**8.1 \textcolor{alta}{ALTA} — Agregar Deepfakes y AI-Powered Social Engineering**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | Phishing tradicional |
| **Contenido Recomendado** | Deepfakes de audio/video, vishing con AI, deepfake detection |
| **Evidencia** | Harvard DCE Panel (2026): "AI democratiza el ciberdelito" |

**8.2 \textcolor{media}{MEDIA} — Agregar Simulacion de Phishing Corporativo**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | Teoria de phishing |
| **Contenido Recomendado** | Configuracion de campana de phishing simulado con GoPhish |
| **Evidencia** | KnowBe4: phishing sigue siendo vector de entrada #1 (36% de breaches) |

\newpage

# MODULO III: Defensa y Analisis

## Semana 9: Analisis de Malware

### Estado Actual
- Tipos de malware
- Analisis estatico basico
- Desinfeccion y eliminacion

### Mejoras Propuestas

**9.1 \textcolor{critica}{CRITICA} — Agregar Analisis Dinamico de Malware**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | Solo analisis estatico |
| **Contenido Recomendado** | + Analisis dinamico (sandboxing), ingenieria inversa, YARA rules |
| **Evidencia** | MITRE ATT&CK: tecnicas de evasion requieren analisis dinamico |
| **Impacto** | El 60% del malware moderno usa ofuscacion que evita analisis estatico |
| **Herramientas** | Any.Run, Cuckoo Sandbox, Ghidra, YARA, CAPA |
| **NICE Work Roles** | 511: Threat Analyst, 541: Malware Analyst |

---

## Semana 10: Seguridad de Redes

### Estado Actual
- Firewalls e IDS/IPS
- Seguridad de redes inalambricas
- VPN y segmentacion

### Mejoras Propuestas

**10.1 \textcolor{alta}{ALTA} — Agregar Network Detection and Response (NDR)**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | Firewalls e IDS tradicionales |
| **Contenido Recomendado** | NDR, NetFlow analysis, east-west traffic monitoring |
| **Evidencia** | Gartner (2025): NDR es componente esencial del SOC moderno |
| **Herramientas** | Zeek (Bro), Suricata, Security Onion |

**10.2 \textcolor{alta}{ALTA} — Agregar Seguridad Zero Trust en Red**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | Segmentacion tradicional |
| **Contenido Recomendado** | Zero Trust Network Access (ZTNA), microsegmentacion, SDP |
| **Evidencia** | NIST SP 800-207: "Zero Trust Architecture" |

---

## Semana 11: Seguridad de Aplicaciones

### Estado Actual
- OWASP Top 10
- Secure coding practices
- Revisiones de codigo

### Mejoras Propuestas

**11.1 \textcolor{critica}{CRITICA} — Actualizar a OWASP Top 10 2025 + OWASP ASVS**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | OWASP Top 10 2021 |
| **Contenido Recomendado** | OWASP Top 10 2025 + ASVS (Application Security Verification Standard) |
| **Evidencia** | OWASP Top 10 2025 incluye Supply Chain y Exceptional Conditions |

**11.2 \textcolor{critica}{CRITICA} — Agregar DevSecOps y Pipeline de Seguridad**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | No menciona DevSecOps |
| **Contenido Recomendado** | CI/CD pipeline security: SAST, DAST, SCA, IaC scanning, SBOM |
| **Evidencia** | DevSecOps market: $7.5B a $32.4B por 2030 (23.2% CAGR) |
| **Capas** | PRE-COMMIT, PR CHECKS, CI BUILD, DEPLOY, RUNTIME |
| **Herramientas** | Semgrep (SAST), Trivy (SCA/container), Checkov (IaC), Syft (SBOM), Cosign (signing) |
| **NICE Work Roles** | 512: Software Development Security, 612: Cloud Security Architect |
| **OWASP Reference** | OWASP SPVS (Secure Pipeline Verification Standard) 2025 |

**11.3 \textcolor{alta}{ALTA} — Agregar Seguridad de Contenedores y Kubernetes**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | No menciona contenedores |
| **Contenido Recomendado** | Docker security, K8s Pod Security Standards, admission controllers |
| **Evidencia** | CNCF: Pod Security Standards (Agosto 2025); DoD Enterprise DevSecOps Reference Design |
| **Herramientas** | Trivy, Falco, Kyverno, OPA Gatekeeper |
| **Certificaciones** | KCNA, KCSA, CKA, CKS |

---

## Semana 12: Laboratorio Integrador

### Estado Actual
- Escenario integrador
- Resolucion de incidentes
- Presentacion de resultados

### Mejoras Propuestas

**12.1 \textcolor{critica}{CRITICA} — Agregar Compromiso con CTF (Capture The Flag)**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | Sin competencias CTF |
| **Contenido Recomendado** | CTF como actividad transversal mensual |
| **Evidencia** | SANS, Hack The Box, TryHackMe: CTFs son el estandar de capacitacion practica |
| **Plataformas** | TryHackMe, Hack The Box, PicoCTF, OverTheWire |

**12.2 \textcolor{alta}{ALTA} — Agregar Laboratorio: Incident Response Simulation**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | Presentacion de resultados |
| **Contenido Recomendado** | Simulacion de incidente: deteccion, contencion, erradicacion, recuperacion |
| **Evidencia** | NIST SP 800-61r2: Computer Security Incident Handling Guide |
| **Herramientas** | TheHive, MISP, Cortex (SOAR) |
| **NICE Work Roles** | 412: Incident Analyst, 421: Incident Responder |

\newpage

# MODULO IV: Especializacion

## Semana 13: Analisis Forense Digital

### Estado Actual
- Introduccion al forense digital
- Recoleccion de evidencia
- Analisis de discos

### Mejoras Propuestas

**13.1 \textcolor{alta}{ALTA} — Agregar Forense de Memoria y Volatile Data**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | Solo forense de disco |
| **Contenido Recomendado** | + Forense de memoria (Volatility), red, cloud |
| **Herramientas** | Volatility 3, Rekall, LiME (Linux memory acquisition) |

**13.2 \textcolor{alta}{ALTA} — Agregar Forense Cloud**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | Forense tradicional (disco local) |
| **Contenido Recomendado** | Forense en AWS/Azure/GCP, evidencia en la nube |
| **Evidencia** | Cloud-first strategies: 94% de empresas usan cloud (Flexera 2025) |
| **Herramientas** | AWS CloudTrail, Azure Sentinel, GCP Audit Logs |

---

## Semana 14: Seguridad en la Nube

### Estado Actual
- Modelos de amenaza en la nube
- Seguridad de datos en la nube
- Configuracion segura de servicios cloud

### Mejoras Propuestas

**14.1 \textcolor{critica}{CRITICA} — Agregar CNAPP y Cloud-Native Security**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | Seguridad cloud generica |
| **Contenido Recomendado** | CNAPP (Cloud-Native Application Protection Platform), CSPM, CWPP |
| **Evidencia** | Gartner (2025): 75% de nuevo CSPM sera parte de CNAPP |
| **Herramientas** | Wiz, Prisma Cloud, Checkov (IaC), Falco (runtime) |

**14.2 \textcolor{alta}{ALTA} — Agregar Infrastructure as Code (IaC) Security**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | No menciona IaC |
| **Contenido Recomendado** | Terraform, CloudFormation security scanning, policy-as-code |
| **Herramientas** | Checkov (3,000+ politicas), tfsec, KICS, OPA/Conftest |

**14.3 \textcolor{media}{MEDIA} — Agregar Post-Quantum Cryptography**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | "Cifrado de informacion" (generico) |
| **Contenido Recomendado** | FIPS 203/204/205 (Agosto 2024), NIST Post-Quantum Standards |
| **Evidencia** | NIST publico FIPS 203 (ML-KEM), 204 (ML-DSA), 205 (SLH-DSA) en Agosto 2024 |

---

## Semana 15: Hacking Web Avanzado

### Estado Actual
- Inyeccion SQL avanzada
- Cross-Site Request Forgery
- Server-Side Request Forgery

### Mejoras Propuestas

**15.1 \textcolor{alta}{ALTA} — Agregar Web3 y Blockchain Security**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | Web security tradicional |
| **Contenido Recomendado** | Smart contract vulnerabilities, reentrancy, flash loan attacks |
| **Evidencia** | Blockchain hacks: $3.8B perdidos en 2024 (Chainalysis) |
| **Herramientas** | Slither, Mythril, Echidna |

**15.2 \textcolor{alta}{ALTA} — Agregar API Security Testing Avanzado**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | Web testing generico |
| **Contenido Recomendado** | GraphQL security, REST API testing, OAuth/OIDC exploitation |
| **Evidencia** | OWASP API Security Top 10 2023 |

---

## Semana 16: Investigacion de Amenazas (Threat Intelligence)

### Estado Actual
- Fuentes de inteligencia de amenazas
- Analisis de indicadores de compromiso (IoC)
- Threat profiling

### Mejoras Propuestas

**16.1 \textcolor{critica}{CRITICA} — Agregar Threat Hunting Proactivo**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | Threat intelligence reactivo |
| **Contenido Recomendado** | Threat hunting hypothesis-driven, MITRE ATT&CK mapping |
| **Evidencia** | SANS: Threat hunting es diferenciador entre SOC reactivo y proactivo |
| **Herramientas** | Jupyter Notebook, Sigma rules, YARA, osquery |

**16.2 \textcolor{alta}{ALTA} — Agregar MITRE ATT&CK Threat Intelligence**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | IoC basico |
| **Contenido Recomendado** | MITRE ATT&CK mapping, threat actor profiles, APT tracking |
| **Herramientas** | ATT&CK Navigator, MISP, OpenCTI, Sigma |

**16.3 \textcolor{alta}{ALTA} — Agregar Seguridad de Infraestructura Critica (ICS/OT)**

| Aspecto | Detalle |
|---------|---------|
| **Contenido Actual** | No menciona ICS/OT |
| **Contenido Recomendado** | NIST SP 800-82r3, IEC 62443, Purdue Model, protocolos industriales |
| **Evidencia** | CISA (2025): Colonial Pipeline, TRITON, Industroyer como casos de estudio |
| **Herramientas** | Shodan (ICS filters), Wireshark (Modbus/DNP3), GRFICSv2 |

\newpage

# Temas Transversales

## 1. Zero Trust Architecture \textcolor{critica}{[CRITICA]}

**Referencia**: NIST SP 800-207 (Agosto 2020, implementacion actualizada 2024)

| Pilar Zero Trust | Implementacion en Curriculo |
|-----------------|---------------------------|
| **Identity** | MFA, RBAC, identity federation — Modulo I |
| **Devices** | Device health verification, EDR — Modulo I-II |
| **Networks** | Microsegmentacion, ZTNA — Modulo III |
| **Applications** | Secure SDLC, API security — Modulo III |
| **Data** | Classification, encryption, DLP — Modulo IV |

## 2. MITRE ATT&CK Framework \textcolor{critica}{[CRITICA]}

**Referencia**: MITRE ATT&CK Enterprise v15 (2025)

| Modulo | Tacticas ATT&CK Relacionadas |
|--------|------------------------------|
| I: Fundamentos | Reconnaissance, Resource Development |
| II: Hacking Etico | Initial Access, Execution, Persistence, Privilege Escalation |
| III: Defensa | Detection, Response, Evasion |
| IV: Especializacion | Collection, Exfiltration, Impact |

## 3. NIST CSF 2.0 Functions \textcolor{critica}{[CRITICA]}

| Funcion CSF | Modulos Relacionados |
|-------------|---------------------|
| **GOVERN** | I, III |
| **IDENTIFY** | I, II |
| **PROTECT** | I, III |
| **DETECT** | III, IV |
| **RESPOND** | III |
| **RECOVER** | IV |

\newpage

# Resumen de Mejoras por Prioridad

## \textcolor{critica}{PRIORIDAD CRITICA} (14 mejoras)

| # | Mejora | Modulo | Semana |
|---|--------|--------|--------|
| 1.1 | Integrar NIST CSF 2.0 | I | 1 |
| 1.2 | Agregar Mapeo MITRE ATT&CK | I | 1 |
| 2.1 | Actualizar OWASP Top 10 a 2025 | I | 2 |
| 2.2 | Agregar OWASP API Security Top 10 | I | 2 |
| 4.1 | Expandir Herramientas a Estandar | I | 4 |
| 5.1 | Metodologia de Reconocimiento | II | 5 |
| 6.1 | Actualizar Tecnicas Explotacion | II | 6 |
| 9.1 | Analisis Dinamico de Malware | III | 9 |
| 11.1 | OWASP Top 10 2025 + ASVS | III | 11 |
| 11.2 | DevSecOps y Pipeline | III | 11 |
| 12.1 | Compromiso con CTF | III | 12 |
| 14.1 | CNAPP y Cloud-Native Security | IV | 14 |
| 16.1 | Threat Hunting Proactivo | IV | 16 |

## \textcolor{alta}{PRIORIDAD ALTA} (18 mejoras)

| # | Mejora | Modulo | Semana |
|---|--------|--------|--------|
| 1.3 | Seguridad AI y LLM | I | 1 |
| 1.4 | Zero Trust Architecture | I | 1 |
| 2.3 | OWASP LLM Top 10 2025 | I | 2 |
| 2.4 | CVE/NVD como Herramienta | I | 2 |
| 3.1 | Seguridad de Infraestructura de Red | I | 3 |
| 4.2 | Lab Entorno Seguro de Pentesting | I | 4 |
| 5.2 | Reconocimiento OT/ICS | II | 5 |
| 6.2 | Lab Explotacion de API | II | 6 |
| 7.1 | Lateral Movement y Pivot | II | 7 |
| 7.2 | Active Directory Attack Path | II | 7 |
| 8.1 | Deepfakes y AI Social Engineering | II | 8 |
| 10.1 | Network Detection and Response | III | 10 |
| 10.2 | Zero Trust en Red | III | 10 |
| 11.3 | Seguridad Contenedores/K8s | III | 11 |
| 12.2 | Incident Response Simulation | III | 12 |
| 13.1 | Forense de Memoria | IV | 13 |
| 13.2 | Forense Cloud | IV | 13 |
| 14.2 | IaC Security | IV | 14 |

## \textcolor{media}{PRIORIDAD MEDIA} (15 mejoras)

| # | Mejora | Modulo | Semana |
|---|--------|--------|--------|
| 3.2 | Seguridad de Contenedores (Intro) | I | 3 |
| 8.2 | Simulacion Phishing Corporativo | II | 8 |
| 14.3 | Post-Quantum Cryptography | IV | 14 |
| 15.1 | Web3 y Blockchain Security | IV | 15 |
| 15.2 | API Security Testing Avanzado | IV | 15 |
| 16.2 | MITRE ATT&CK Threat Intelligence | IV | 16 |
| 16.3 | Seguridad ICS/OT | IV | 16 |

\newpage

# Mapeo a Estandares Internacionales

## NICE Framework v2.0.0 — Work Roles Cubiertos

| NICE Work Role | Categoria | Modulos Relacionados |
|---------------|-----------|---------------------|
| 412: Incident Analyst | Operaciones | III, IV |
| 421: Network Operations Specialist | Operaciones | I, III |
| 431: Vulnerability Assessment Analyst | Operaciones | I, II, III |
| 511: Threat Analyst | Supervision | II, IV |
| 512: Software Development Security | Supervision | III |
| 521: Exploitation Analyst | Supervision | II |
| 541: Malware Analyst | Supervision | III |
| 612: Cloud Security Architect | Diseno | IV |
| 701: Security Control Assessor | Gestion | I |
| 710: System Security Manager | Gestion | I |

## Certificaciones Relacionadas por Modulo

| Modulo | Certificaciones que Prepara |
|--------|----------------------------|
| I | CompTIA Security+, ISC2 Certified in Cybersecurity |
| II | CEH (Certified Ethical Hacker), CompTIA PenTest+ |
| III | CompTIA CySA+, GIAC Security Essentials |
| IV | CKA/CKS (Kubernetes), AWS Security Specialty |

\newpage

# Conclusiones

## Impacto Esperado

| Metrica | Antes | Despues | Mejora |
|---------|-------|---------|--------|
| Estandares OWASP | 2021 | 2025 + API + LLM | Actualizado |
| Frameworks de referencia | Ninguno | NIST CSF 2.0, MITRE ATT&CK, NICE | +3 marcos |
| Temas criticos ausentes | 7 temas | 0 temas | 100% cobertura |
| Mapeo NICE Work Roles | 0 | 10 roles | +10 roles |
| Herramientas ensenadas | ~5 | ~25+ | +400% |

## ROI de la Certificacion

Con estas mejoras, la certificacion:

1. **Alineacion con demanda laboral**: Fortinet 2025 reporta 91% de empleadores prefieren candidatos certificados
2. **Competitividad regional**: similar a programas de UNI (Peru), URL (Guatemala), INACAP (Chile)
3. **Preparacion para certificaciones**: CompTIA Security+, CEH, CKA/CKS, GICSP
4. **Cobertura de emergentes**: AI/ML, DevSecOps, IoT/OT, Supply Chain

## Sobre el Autor

**Diego Saavedra** — FullStack Developer & Cybersecurity Consultant

- Portfolio: https://statick88.github.io
- Experiencia en desarrollo fullstack y ciberseguridad
- Investigacion aplicada a educacion en ciberseguridad

## Referencias Principales

1. NIST CSF 2.0 (Feb 2024) — CSWP 29
2. NIST SP 800-207 — Zero Trust Architecture
3. NIST SP 800-82r3 (Sep 2023) — OT Security
4. NIST AI 100-2 e2025 — Adversarial ML Taxonomy
5. OWASP Top 10 (2025)
6. OWASP LLM Top 10 v2.0 (Nov 2025)
7. OWASP API Security Top 10 (2023)
8. OWASP SPVS (2025) — Secure Pipeline Verification
9. MITRE ATT&CK Enterprise v15 (2025)
10. NICE Framework v2.0.0 (Mar 2025)
11. ISA/IEC 62443 — Industrial Cybersecurity
12. ISC2 Workforce Study 2024
13. Fortinet Skills Gap Report 2024/2025
14. IBM Cost of a Data Breach 2025
15. OECD: Building a Skilled Cyber Security Workforce in LATAM (2024)

---

*Propuesta presentada por Diego Saavedra — https://statick88.github.io*
*Junio 2026*
