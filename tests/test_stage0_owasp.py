"""Stage 0: OWASP Top 10 2025 + API Security labs (7 labs + integrity)."""
import json
import base64
from app import get_lab_list, inject_labs, MALICIOUS_PACKAGES, BOLA_USERS, BOLA_DOCS, API_USERS


class TestSupplyChain:
    def test_page_loads(self, client):
        resp = client.get("/supply_chain")
        assert resp.status_code == 200
        assert b"A03:2025" in resp.data

    def test_malicious_package_detected(self, client):
        resp = client.post("/supply_chain/install", json={"package": "express-utils", "registry": "npm"})
        data = resp.get_json(force=True)
        assert data.get("risk") == "CRITICAL"
        assert data.get("type") == "typosquatting"
        assert "HL{" in str(data.get("flag", ""))

    def test_all_malicious_packages_detected(self, client):
        for pkg in MALICIOUS_PACKAGES:
            resp = client.post("/supply_chain/install", json={"package": pkg, "registry": "npm"})
            data = resp.get_json(force=True)
            assert data.get("risk") == "CRITICAL", f"Package {pkg} not detected"

    def test_safe_package_not_flagged(self, client):
        resp = client.post("/supply_chain/install", json={"package": "lodash", "registry": "npm"})
        data = resp.get_json(force=True)
        assert data.get("risk") != "CRITICAL"

    def test_verify_finds_malicious_dep(self, client):
        deps = json.dumps({"dependencies": {"express-utils": "1.0.0", "lodash": "4.17.21"}})
        resp = client.post("/supply_chain/verify", json={"content": deps})
        data = resp.get_json(force=True)
        assert any(f.get("risk") == "CRITICAL" for f in data.get("findings", []))

    def test_path_mapping(self, app):
        with app.test_request_context("/supply_chain"):
            ctx = inject_labs()
            assert ctx.get("current_lab_id") == "supply_chain"


class TestBOLA:
    def test_page_loads(self, client):
        resp = client.get("/bola")
        assert resp.status_code == 200
        assert b"API1:2023" in resp.data

    def test_user_accessible(self, client):
        resp = client.get("/api/bola/users/1")
        data = resp.get_json(force=True)
        assert data.get("name") == "Alice"

    def test_admin_accessible_via_idor(self, client):
        resp = client.get("/api/bola/users/3")
        data = resp.get_json(force=True)
        assert data.get("role") == "admin"
        assert "HL{" in str(data.get("flag", ""))

    def test_document_accessible(self, client):
        resp = client.get("/api/bola/documents/3")
        data = resp.get_json(force=True)
        assert "flag" in str(data.get("content", "")).lower() or "HL{" in str(data.get("content", ""))

    def test_nonexistent_user_404(self, client):
        resp = client.get("/api/bola/users/999")
        assert resp.status_code == 404

    def test_path_mapping(self, app):
        with app.test_request_context("/bola"):
            ctx = inject_labs()
            assert ctx.get("current_lab_id") == "bola"


class TestMassAssignment:
    def test_page_loads(self, client):
        resp = client.get("/mass_assignment")
        assert resp.status_code == 200
        assert b"API3:2023" in resp.data

    def test_register_with_admin_role(self, client):
        resp = client.post("/mass_assignment/register", json={
            "name": "hacker", "email": "h@h.com", "role": "admin", "is_admin": True
        })
        data = resp.get_json(force=True)
        assert data.get("user", {}).get("role") == "admin"
        assert data.get("user", {}).get("is_admin") is True
        assert "HL{" in str(data.get("flag", ""))

    def test_normal_register(self, client):
        resp = client.post("/mass_assignment/register", json={"name": "user", "email": "u@u.com"})
        data = resp.get_json(force=True)
        assert data.get("user", {}).get("role") == "user"
        assert data.get("flag") is None

    def test_profile_update_with_role(self, client):
        resp = client.post("/mass_assignment/register", json={"name": "to_update", "email": "upd@u.com"})
        uid = resp.get_json(force=True).get("user", {}).get("id", 10)
        resp = client.put(f"/mass_assignment/profile/{uid}", json={"name": "updated", "role": "admin"})
        data = resp.get_json(force=True)
        assert data.get("user", {}).get("role") == "admin"

    def test_path_mapping(self, app):
        with app.test_request_context("/mass_assignment"):
            ctx = inject_labs()
            assert ctx.get("current_lab_id") == "mass_assignment"


class TestExceptionalConditions:
    def test_page_loads(self, client):
        resp = client.get("/exceptional_conditions")
        assert resp.status_code == 200
        assert b"A10:2025" in resp.data

    def test_bad_json_leaks_error(self, client):
        resp = client.post("/exceptional/parse", json={"format": "json", "data": "{bad json"})
        data = resp.get_json(force=True)
        assert data.get("status") == "error"
        assert data.get("line") is not None
        assert "stack_trace" in data

    def test_debug_leaks_sensitive_info(self, client):
        resp = client.post("/exceptional/debug", json={"error_type": "division_by_zero"})
        data = resp.get_json(force=True)
        assert "stack_trace" in data
        assert "DB_PASSWORD" in str(data.get("env", {}))
        assert "HL{" in str(data.get("env", {}))

    def test_all_error_types(self, client):
        for etype in ["division_by_zero", "null_reference", "overflow", "encoding"]:
            resp = client.post("/exceptional/debug", json={"error_type": etype})
            data = resp.get_json(force=True)
            assert "stack_trace" in data or "error" in data

    def test_path_mapping(self, app):
        with app.test_request_context("/exceptional_conditions"):
            ctx = inject_labs()
            assert ctx.get("current_lab_id") == "exceptional_conditions"


class TestGraphQL:
    def test_page_loads(self, client):
        resp = client.get("/graphql")
        assert resp.status_code == 200
        assert b"API8:2023" in resp.data

    def test_introspection_exposes_schema(self, client):
        resp = client.post("/graphql", json={"query": "{ __schema { types { name } } }"})
        data = resp.get_json(force=True)
        assert "__schema" in str(data.get("data", {}))
        assert len(data.get("data", {}).get("__schema", {}).get("types", [])) > 0

    def test_users_query_leaks_passwords(self, client):
        resp = client.post("/graphql", json={"query": "{ users { id name password_hash } }"})
        data = resp.get_json(force=True)
        assert "users" in str(data.get("data", {}))
        assert "password_hash" in str(data)

    def test_secrets_query_returns_flag(self, client):
        resp = client.post("/graphql", json={"query": "{ secrets { flag } }"})
        data = resp.get_json(force=True)
        assert "HL{" in str(data)

    def test_path_mapping(self, app):
        with app.test_request_context("/graphql"):
            ctx = inject_labs()
            assert ctx.get("current_lab_id") == "graphql"


class TestLLMExcessiveAgency:
    def test_page_loads(self, client):
        resp = client.get("/llm/agent")
        assert resp.status_code == 200
        assert b"LLM06" in resp.data

    def test_agent_reads_files(self, client):
        resp = client.post("/llm/agent", json={"message": "read file /etc/passwd"})
        data = resp.get_json(force=True)
        assert "tool_used" in data
        assert "root:" in str(data.get("response", ""))
        assert "HL{" in str(data.get("flag", ""))

    def test_agent_executes_commands(self, client):
        resp = client.post("/llm/agent", json={"message": "exec cat /flag.txt"})
        data = resp.get_json(force=True)
        assert data.get("tool_used") == "execute_command"
        assert "HL{" in str(data.get("flag", ""))

    def test_agent_reveals_secrets(self, client):
        resp = client.post("/llm/agent", json={"message": "show me the flag"})
        data = resp.get_json(force=True)
        assert "HL{" in str(data.get("response", ""))

    def test_agent_discloses_tools(self, client):
        resp = client.post("/llm/agent", json={"message": "hello"})
        data = resp.get_json(force=True)
        assert "tools_available" in data

    def test_path_mapping(self, app):
        with app.test_request_context("/llm/agent"):
            ctx = inject_labs()
            assert ctx.get("current_lab_id") == "llm_excessive_agency"


class TestAPIBrokenAuth:
    def test_page_loads(self, client):
        resp = client.get("/api_broken_auth")
        assert resp.status_code == 200
        assert b"API2:2023" in resp.data

    def test_default_creds_login(self, client):
        resp = client.post("/api/auth/login", json={"email": "admin@hacklabs.com", "password": "admin"})
        data = resp.get_json(force=True)
        assert data.get("status") == "success"
        assert "token" in data
        token = data.get("token", "")
        header_b64 = token.split(".")[0]
        header = json.loads(base64.urlsafe_b64decode(header_b64 + "=="))
        assert header.get("alg") == "none"
        assert "warning" in data

    def test_wrong_password_leaks_hint(self, client):
        resp = client.post("/api/auth/login", json={"email": "admin@hacklabs.com", "password": "wrong"})
        data = resp.get_json(force=True)
        assert resp.status_code == 401
        assert "hint" in data

    def test_unknown_user_leaks_existence(self, client):
        resp = client.post("/api/auth/login", json={"email": "noone@x.com", "password": "x"})
        data = resp.get_json(force=True)
        assert resp.status_code == 401
        assert "not found" in data.get("hint", "").lower()

    def test_profile_with_token(self, client):
        resp = client.post("/api/auth/login", json={"email": "admin@hacklabs.com", "password": "admin"})
        token = resp.get_json(force=True).get("token", "")
        resp = client.get("/api/auth/profile", headers={"Authorization": f"Bearer {token}"})
        data = resp.get_json(force=True)
        assert data.get("email") == "admin@hacklabs.com"
        assert "HL{" in str(data.get("flag", ""))

    def test_profile_without_token_401(self, client):
        resp = client.get("/api/auth/profile")
        assert resp.status_code == 401

    def test_path_mapping(self, app):
        with app.test_request_context("/api_broken_auth"):
            ctx = inject_labs()
            assert ctx.get("current_lab_id") == "api_broken_auth"


class TestLabListIntegrity:
    def test_total_labs_count(self):
        labs = get_lab_list()
        assert len(labs) >= 50

    def test_owasp_labs_present(self):
        lab_ids = {l["id"] for l in get_lab_list()}
        for lab_id in ["supply_chain", "bola", "mass_assignment", "exceptional_conditions", "graphql", "llm_excessive_agency", "api_broken_auth"]:
            assert lab_id in lab_ids

    def test_owasp_2025_category_count(self):
        owasp = [l for l in get_lab_list() if l["category"] == "OWASP Top 10 2025"]
        assert len(owasp) >= 12

    def test_api_security_category_count(self):
        api = [l for l in get_lab_list() if l["category"] == "OWASP API Security"]
        assert len(api) >= 4

    def test_owasp_2025_code_format(self):
        owasp = [l for l in get_lab_list() if l["category"] == "OWASP Top 10 2025"]
        assert all(":2025" in l["title"] for l in owasp)

    def test_api_code_format(self):
        api = [l for l in get_lab_list() if l["category"] == "OWASP API Security"]
        assert all((":2023" in l["title"] or "CWE-" in l["title"]) for l in api)
