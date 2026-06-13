"""Stage 3: Breach-driven labs (5 labs)."""
from app import get_lab_list


class TestSupplyChainAdvanced:
    def test_page_loads(self, client):
        resp = client.get("/lab/supply_chain_v2")
        assert resp.status_code == 200

    def test_typosquatting_detection(self, client):
        resp = client.post("/supply_chain_v2/scan", json={"dependencies": {"expresss": "^1.0.0"}})
        data = resp.get_json()
        assert len(data.get("findings", [])) > 0


class TestExceptionalV2:
    def test_page_loads(self, client):
        resp = client.get("/lab/exceptional_v2")
        assert resp.status_code == 200

    def test_db_error_leak(self, client):
        resp = client.post("/exceptional_v2/lookup", json={"id": "1'"})
        data = resp.get_json()
        assert "error" in data


class TestDOMXSSAdvanced:
    def test_page_loads(self, client):
        resp = client.get("/lab/dom_xss_advanced")
        assert resp.status_code == 200

    def test_event_handler_detection(self, client):
        resp = client.post("/dom_xss_advanced/render", json={"html": '<img src=x onerror=alert(1)>'})
        data = resp.get_json()
        assert data.get("has_event_handler") is True


class TestMassAssignmentV2:
    def test_page_loads(self, client):
        resp = client.get("/lab/mass_assignment_v2")
        assert resp.status_code == 200

    def test_role_escalation(self, client):
        resp = client.post("/mass_assignment_v2/register", json={
            "name": "A", "email": "a@b.com", "password": "x", "role": "admin"
        })
        data = resp.get_json()
        assert data.get("is_admin") is True
        assert "HL{" in (data.get("flag") or "")


class TestUUIDIDOR:
    def test_page_loads(self, client):
        resp = client.get("/lab/uuid_idor")
        assert resp.status_code == 200

    def test_sequential_uuid_accessible(self, client):
        resp = client.get("/uuid_idor/doc/doc-00000005")
        data = resp.get_json()
        assert data.get("flag") is not None

    def test_invalid_uuid_404(self, client):
        resp = client.get("/uuid_idor/doc/doc-99999999")
        assert resp.status_code == 404
