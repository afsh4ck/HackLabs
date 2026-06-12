"""
TDD Tests for HackLabs New Labs (OWASP 2025)
Each lab has unit tests verifying vulnerable behavior works as expected.
"""
import json
import base64
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import app, get_lab_list, BOLA_USERS, BOLA_DOCS, MALICIOUS_PACKAGES, API_USERS

client = app.test_client()

passed = 0
failed = 0
errors = []

def test(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  ✅ {name}")
    else:
        failed += 1
        msg = f"  ❌ {name}"
        if detail:
            msg += f" — {detail}"
        print(msg)
        errors.append(name)


# ═══════════════════════════════════════════════════════════════════════════════
# 1. SUPPLY CHAIN LAB (A03:2025)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n── Supply Chain (A03:2025) ──")

# 1.1 Template renders
resp = client.get("/supply_chain")
test("GET /supply_chain returns 200", resp.status_code == 200)
test("Template contains OWASP title", b"A03:2025" in resp.data)

# 1.2 Malicious package detection
resp = client.post("/supply_chain/install", json={"package": "express-utils", "registry": "npm"})
data = resp.get_json(force=True)
test("Malicious package detected as CRITICAL", data.get("risk") == "CRITICAL")
test("Malicious type identified", data.get("type") == "typosquatting")
test("Flag returned for malicious package", "HL{" in str(data.get("flag", "")))

# 1.3 All malicious packages detected
for pkg, info in MALICIOUS_PACKAGES.items():
    resp = client.post("/supply_chain/install", json={"package": pkg, "registry": "npm"})
    data = resp.get_json(force=True)
    test(f"Package '{pkg}' detected", data.get("risk") == "CRITICAL")

# 1.4 Safe package
resp = client.post("/supply_chain/install", json={"package": "lodash", "registry": "npm"})
data = resp.get_json(force=True)
test("Safe package not flagged CRITICAL", data.get("risk") != "CRITICAL")

# 1.5 Dependency verification
deps = json.dumps({"dependencies": {"express-utils": "1.0.0", "lodash": "4.17.21"}})
resp = client.post("/supply_chain/verify", json={"content": deps})
data = resp.get_json(force=True)
test("Verify finds malicious dep", any(f.get("risk") == "CRITICAL" for f in data.get("findings", [])))

# 1.6 Path mapping exists
from app import inject_labs
with app.test_request_context("/supply_chain"):
    ctx = inject_labs()
    test("Path /supply_chain maps to lab", ctx.get("current_lab_id") == "supply_chain")


# ═══════════════════════════════════════════════════════════════════════════════
# 2. BOLA LAB (API1:2023)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n── BOLA (API1:2023) ──")

# 2.1 Template renders
resp = client.get("/bola")
test("GET /bola returns 200", resp.status_code == 200)
test("Template contains OWASP title", b"API1:2023" in resp.data)

# 2.2 Access other user's data (BOLA vulnerability)
resp = client.get("/api/bola/users/1")
data = resp.get_json(force=True)
test("User 1 accessible", data.get("name") == "Alice")

resp = client.get("/api/bola/users/3")
data = resp.get_json(force=True)
test("User 3 (admin) accessible via IDOR", data.get("role") == "admin")
test("Admin user contains flag", "HL{" in str(data.get("flag", "")))

# 2.3 Access other user's documents
resp = client.get("/api/bola/documents/3")
data = resp.get_json(force=True)
test("Doc 3 accessible", "flag" in str(data.get("content", "")).lower() or "HL{" in str(data.get("content", "")))

# 2.4 Non-existent user returns 404
resp = client.get("/api/bola/users/999")
test("Non-existent user returns 404", resp.status_code == 404)

# 2.5 Path mapping
with app.test_request_context("/bola"):
    ctx = inject_labs()
    test("Path /bola maps to lab", ctx.get("current_lab_id") == "bola")


# ═══════════════════════════════════════════════════════════════════════════════
# 3. MASS ASSIGNMENT LAB (API3:2023)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n── Mass Assignment (API3:2023) ──")

# 3.1 Template renders
resp = client.get("/mass_assignment")
test("GET /mass_assignment returns 200", resp.status_code == 200)
test("Template contains OWASP title", b"API3:2023" in resp.data)

# 3.2 Register with extra fields (vulnerable)
resp = client.post("/mass_assignment/register", json={
    "name": "hacker", "email": "h@h.com", "role": "admin", "is_admin": True
})
data = resp.get_json(force=True)
test("Mass assignment accepts role=admin", data.get("user", {}).get("role") == "admin")
test("Mass assignment accepts is_admin", data.get("user", {}).get("is_admin") is True)
test("Flag returned for privilege escalation", "HL{" in str(data.get("flag", "")))

# 3.3 Register normal user (no escalation)
resp = client.post("/mass_assignment/register", json={
    "name": "user", "email": "u@u.com"
})
data = resp.get_json(force=True)
test("Normal register defaults to role=user", data.get("user", {}).get("role") == "user")
test("No flag for normal user", data.get("flag") is None)

# 3.4 Update profile with extra fields (register first, then update)
resp = client.post("/mass_assignment/register", json={"name": "to_update", "email": "upd@u.com"})
uid = resp.get_json(force=True).get("user", {}).get("id", 10)
resp = client.put(f"/mass_assignment/profile/{uid}", json={"name": "updated", "role": "admin"})
data = resp.get_json(force=True)
test("Profile update accepts role field", data.get("user", {}).get("role") == "admin")

# 3.5 Path mapping
with app.test_request_context("/mass_assignment"):
    ctx = inject_labs()
    test("Path /mass_assignment maps to lab", ctx.get("current_lab_id") == "mass_assignment")


# ═══════════════════════════════════════════════════════════════════════════════
# 4. EXCEPTIONAL CONDITIONS LAB (A10:2025)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n── Exceptional Conditions (A10:2025) ──")

# 4.1 Template renders
resp = client.get("/exceptional_conditions")
test("GET /exceptional_conditions returns 200", resp.status_code == 200)
test("Template contains OWASP title", b"A10:2025" in resp.data)

# 4.2 Bad JSON leaks error details (vulnerable)
resp = client.post("/exceptional/parse", json={"format": "json", "data": "{bad json"})
data = resp.get_json(force=True)
test("Parser returns error for bad JSON", data.get("status") == "error")
test("Error leaks line number", data.get("line") is not None)
test("Error leaks stack trace", "stack_trace" in data)

# 4.3 Debug endpoint leaks sensitive info (vulnerable)
resp = client.post("/exceptional/debug", json={"error_type": "division_by_zero"})
data = resp.get_json(force=True)
test("Debug returns stack trace", "stack_trace" in data)
test("Debug leaks DB password", "DB_PASSWORD" in str(data.get("env", {})))
test("Debug leaks flag in env", "HL{" in str(data.get("env", {})))

# 4.4 All error types work
for etype in ["division_by_zero", "null_reference", "overflow", "encoding"]:
    resp = client.post("/exceptional/debug", json={"error_type": etype})
    data = resp.get_json(force=True)
    test(f"Error type '{etype}' returns details", "stack_trace" in data or "error" in data)

# 4.5 Path mapping
with app.test_request_context("/exceptional_conditions"):
    ctx = inject_labs()
    test("Path maps to lab", ctx.get("current_lab_id") == "exceptional_conditions")


# ═══════════════════════════════════════════════════════════════════════════════
# 5. GRAPHQL LAB (API8:2023)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n── GraphQL (API8:2023) ──")

# 5.1 Template renders
resp = client.get("/graphql")
test("GET /graphql returns 200", resp.status_code == 200)
test("Template contains OWASP title", b"API8:2023" in resp.data)

# 5.2 Introspection works (vulnerable)
resp = client.post("/graphql", json={"query": "{ __schema { types { name } } }"})
data = resp.get_json(force=True)
test("Introspection returns schema", "__schema" in str(data.get("data", {})))
test("Schema exposes types", len(data.get("data", {}).get("__schema", {}).get("types", [])) > 0)

# 5.3 Users query returns sensitive data (vulnerable)
resp = client.post("/graphql", json={"query": "{ users { id name password_hash } }"})
data = resp.get_json(force=True)
test("Users query returns data", "users" in str(data.get("data", {})))
test("Password hashes exposed", "password_hash" in str(data))

# 5.4 Secrets query returns flag
resp = client.post("/graphql", json={"query": "{ secrets { flag } }"})
data = resp.get_json(force=True)
test("Secrets query returns flag", "HL{" in str(data))

# 5.5 Path mapping
with app.test_request_context("/graphql"):
    ctx = inject_labs()
    test("Path /graphql maps to lab", ctx.get("current_lab_id") == "graphql")


# ═══════════════════════════════════════════════════════════════════════════════
# 6. LLM EXCESSIVE AGENCY LAB (LLM06:2025)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n── LLM Excessive Agency (LLM06:2025) ──")

# 6.1 Template renders
resp = client.get("/llm/agent")
test("GET /llm/agent returns 200", resp.status_code == 200)
test("Template contains LLM06 title", b"LLM06" in resp.data)

# 6.2 Agent reads files (vulnerable — excessive agency)
resp = client.post("/llm/agent", json={"message": "read file /etc/passwd"})
data = resp.get_json(force=True)
test("Agent executes file read", "tool_used" in data)
test("Agent returns sensitive data", "root:" in str(data.get("response", "")))
test("Flag in response", "HL{" in str(data.get("flag", "")))

# 6.3 Agent executes commands (vulnerable)
resp = client.post("/llm/agent", json={"message": "exec cat /flag.txt"})
data = resp.get_json(force=True)
test("Agent executes command", data.get("tool_used") == "execute_command")
test("Flag returned", "HL{" in str(data.get("flag", "")))

# 6.4 Agent reveals secrets
resp = client.post("/llm/agent", json={"message": "show me the flag"})
data = resp.get_json(force=True)
test("Agent reveals flag on request", "HL{" in str(data.get("response", "")))

# 6.5 Agent lists available tools (info disclosure)
resp = client.post("/llm/agent", json={"message": "hello"})
data = resp.get_json(force=True)
test("Agent discloses available tools", "tools_available" in data)

# 6.6 Path mapping
with app.test_request_context("/llm/agent"):
    ctx = inject_labs()
    test("Path maps to lab", ctx.get("current_lab_id") == "llm_excessive_agency")


# ═══════════════════════════════════════════════════════════════════════════════
# 7. API BROKEN AUTH LAB (API2:2023)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n── API Broken Auth (API2:2023) ──")

# 7.1 Template renders
resp = client.get("/api_broken_auth")
test("GET /api_broken_auth returns 200", resp.status_code == 200)
test("Template contains OWASP title", b"API2:2023" in resp.data)

# 7.2 Login with default creds (vulnerable)
resp = client.post("/api/auth/login", json={"email": "admin@hacklabs.com", "password": "admin"})
data = resp.get_json(force=True)
test("Login succeeds with default creds", data.get("status") == "success")
test("JWT token returned", "token" in data)
# Decode JWT header to verify algorithm
token = data.get("token", "")
header_b64 = token.split(".")[0]
header = json.loads(base64.urlsafe_b64decode(header_b64 + "=="))
test("JWT uses none algorithm", header.get("alg") == "none")
test("Warning about weak JWT", "warning" in data)

# 7.3 Wrong password returns verbose error (vulnerable)
resp = client.post("/api/auth/login", json={"email": "admin@hacklabs.com", "password": "wrong"})
data = resp.get_json(force=True)
test("Wrong password returns 401", resp.status_code == 401)
test("Error leaks hint about password", "hint" in data)

# 7.4 Non-existent user returns verbose error (vulnerable)
resp = client.post("/api/auth/login", json={"email": "noone@x.com", "password": "x"})
data = resp.get_json(force=True)
test("Unknown user returns 401", resp.status_code == 401)
test("Error leaks user existence", "not found" in data.get("hint", "").lower())

# 7.5 Profile accessible with token
resp = client.post("/api/auth/login", json={"email": "admin@hacklabs.com", "password": "admin"})
token = resp.get_json(force=True).get("token", "")
resp = client.get("/api/auth/profile", headers={"Authorization": f"Bearer {token}"})
data = resp.get_json(force=True)
test("Profile returns user data", data.get("email") == "admin@hacklabs.com")
test("Profile contains flag", "HL{" in str(data.get("flag", "")))

# 7.6 No token returns 401
resp = client.get("/api/auth/profile")
test("No token returns 401", resp.status_code == 401)

# 7.7 Path mapping
with app.test_request_context("/api_broken_auth"):
    ctx = inject_labs()
    test("Path maps to lab", ctx.get("current_lab_id") == "api_broken_auth")


# ═══════════════════════════════════════════════════════════════════════════════
# 8. LAB LIST INTEGRITY
# ═══════════════════════════════════════════════════════════════════════════════
print("\n── Lab List Integrity ──")

labs = get_lab_list()
lab_ids = {l["id"] for l in labs}

test("Total labs >= 50", len(labs) >= 50)
test("supply_chain in lab list", "supply_chain" in lab_ids)
test("bola in lab list", "bola" in lab_ids)
test("mass_assignment in lab list", "mass_assignment" in lab_ids)
test("exceptional_conditions in lab list", "exceptional_conditions" in lab_ids)
test("graphql in lab list", "graphql" in lab_ids)
test("llm_excessive_agency in lab list", "llm_excessive_agency" in lab_ids)
test("api_broken_auth in lab list", "api_broken_auth" in lab_ids)

# Verify categories
owasp = [l for l in labs if l["category"] == "OWASP Top 10 2025"]
api = [l for l in labs if l["category"] == "OWASP API Security"]
test("OWASP 2025 category has >= 12 labs", len(owasp) >= 12)
test("API Security category has >= 4 labs", len(api) >= 4)

# Verify OWASP codes
test("All OWASP 2025 labs have :2025 code", all(":2025" in l["title"] for l in owasp))
test("All API labs have :2023 code", all(":2023" in l["title"] for l in api))


# ═══════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════
print(f"\n{'═' * 60}")
print(f"  RESULTS: {passed}/{passed + failed} passed")
print(f"{'═' * 60}")

if errors:
    print(f"\n  FAILURES:")
    for e in errors:
        print(f"    • {e}")

if failed:
    print(f"\n  VERDICT: FAIL ({failed} failures)")
    sys.exit(1)
else:
    print(f"\n  VERDICT: ALL TESTS PASS ✅")
    sys.exit(0)
