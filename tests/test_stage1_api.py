"""Stage 1: API Security labs — bug bounty findings (6 labs)."""
from app import get_lab_list, inject_labs


class TestPrototypePollution:
    def test_page_loads(self, client):
        resp = client.get("/lab/prototype_pollution")
        assert resp.status_code == 200
        assert b"CWE-1321" in resp.data

    def test_normal_merge(self, client):
        resp = client.post("/pollute/merge", json={"theme": "light"})
        assert resp.status_code == 200

    def test_admin_check(self, client):
        resp = client.get("/pollute/admin")
        data = resp.get_json()
        assert "isAdmin" in data

    def test_proto_pollution_injection(self, client):
        resp = client.post("/pollute/merge", json={"__proto__": {"isAdmin": True}})
        assert resp.status_code == 200

    def test_lab_in_list(self):
        lab_ids = {l["id"] for l in get_lab_list()}
        assert "prototype_pollution" in lab_ids


class TestAPIDataExposure:
    def test_page_loads(self, client):
        resp = client.get("/lab/api_data_exposure")
        assert resp.status_code == 200

    def test_user_data_exposed(self, client):
        resp = client.get("/api/v2/users/1")
        data = resp.get_json()
        assert data is not None
        assert "password_hash" in data
        assert "ssn" in data
        assert "reset_token" in data
        assert "HL{" in (data.get("flag") or "")

    def test_missing_user_404(self, client):
        resp = client.get("/api/v2/users/999")
        assert resp.status_code == 404

    def test_lab_in_list(self):
        lab_ids = {l["id"] for l in get_lab_list()}
        assert "api_data_exposure" in lab_ids


class TestRateLimitBypass:
    def test_page_loads(self, client):
        resp = client.get("/lab/rate_limit_bypass")
        assert resp.status_code == 200

    def test_login_returns_401(self, client):
        resp = client.post("/api/auth/login", json={"email": "x@x.com", "password": "wrong"})
        assert resp.status_code == 401

    def test_rate_limit_check(self, client):
        resp = client.post("/api/auth/login", json={"email": "admin@hacklabs.com", "password": "wrong"})
        assert resp.status_code in [401, 429]

    def test_lab_in_list(self):
        lab_ids = {l["id"] for l in get_lab_list()}
        assert "rate_limit_bypass" in lab_ids


class TestBusinessFlowAbuse:
    def test_page_loads(self, client):
        resp = client.get("/lab/business_flow_abuse")
        assert resp.status_code == 200

    def test_coupon_applies(self, client):
        resp = client.post("/api/coupon/apply", json={"coupon": "WELCOME10", "cart_total": 100})
        data = resp.get_json()
        assert data.get("status") == "applied"
        assert data.get("discount") == 10

    def test_referral_bonus(self, client):
        resp = client.post("/api/referral", json={"referral_email": "test@x.com"})
        data = resp.get_json()
        assert data.get("bonus") == 5.0

    def test_lab_in_list(self):
        lab_ids = {l["id"] for l in get_lab_list()}
        assert "business_flow_abuse" in lab_ids


class TestBFLA:
    def test_page_loads(self, client):
        resp = client.get("/lab/bfla")
        assert resp.status_code == 200

    def test_user_profile_accessible(self, client):
        resp = client.get("/api/user/profile")
        assert resp.status_code == 200

    def test_admin_users_without_auth(self, client):
        resp = client.get("/api/admin/users")
        data = resp.get_json()
        assert "users" in data
        assert "HL{" in (data.get("flag") or "")

    def test_admin_config_accessible(self, client):
        resp = client.get("/api/admin/config")
        data = resp.get_json()
        assert "debug_mode" in data

    def test_debug_leaks_secrets(self, client):
        resp = client.get("/api/internal/debug")
        data = resp.get_json()
        assert "SECRET_KEY" in str(data)

    def test_lab_in_list(self):
        lab_ids = {l["id"] for l in get_lab_list()}
        assert "bfla" in lab_ids


class TestUnsafeAPIConsumption:
    def test_page_loads(self, client):
        resp = client.get("/lab/unsafe_api_consumption")
        assert resp.status_code == 200

    def test_webhook_accepted(self, client):
        resp = client.post("/api/webhook", json={"status": "ok", "note": "test"})
        assert resp.status_code == 200

    def test_payment_status_shows_webhooks(self, client):
        resp = client.get("/api/payment-status")
        data = resp.get_json()
        assert "webhooks" in data

    def test_lab_in_list(self):
        lab_ids = {l["id"] for l in get_lab_list()}
        assert "unsafe_api_consumption" in lab_ids


class TestStage1LabCount:
    def test_total_labs_ge_56(self):
        assert len(get_lab_list()) >= 56
