"""Stage 2: Cloud/Advanced labs (4 labs)."""
from app import get_lab_list


class TestCloudMetadataSSRF:
    def test_page_loads(self, client):
        resp = client.get("/lab/cloud_metadata_ssrf")
        assert resp.status_code == 200

    def test_fetch_returns_iam_creds(self, client):
        resp = client.post("/cloud/fetch", json={"url": "http://169.254.169.254/latest/meta-data/iam/security-credentials/"})
        data = resp.get_json()
        assert "credentials" in data or "flag" in data


class TestAdvancedSSRF:
    def test_page_loads(self, client):
        resp = client.get("/lab/ssrf_advanced")
        assert resp.status_code == 200

    def test_blocks_internal_ips(self, client):
        resp = client.post("/ssrf/advanced/fetch", json={"url": "http://127.0.0.1:5000/admin"})
        data = resp.get_json()
        assert data.get("blocked") is True

    def test_dns_rebind_simulation(self, client):
        resp = client.post("/ssrf/advanced/rebind", json={"domain": "rebind.attacker.com"})
        data = resp.get_json()
        assert "admin_data" in data


class TestHTTPSmuggling:
    def test_page_loads(self, client):
        resp = client.get("/lab/http_smuggling")
        assert resp.status_code == 200

    def test_inspector_analyses_cl_te(self, client):
        raw = "POST / HTTP/1.1\r\nHost: localhost\r\nContent-Length: 6\r\nTransfer-Encoding: chunked\r\n\r\n0\r\n\r\nX"
        resp = client.post("/smuggle/inspect", content_type="text/plain", data=raw)
        data = resp.get_json()
        assert data.get("has_content_length") is True


class TestGraphQLAdvanced:
    def test_page_loads(self, client):
        resp = client.get("/lab/graphql_advanced")
        assert resp.status_code == 200

    def test_introspection_works(self, client):
        resp = client.post("/graphql/advanced", json={"query": "{ __schema { types { name } } }"})
        data = resp.get_json()
        assert "data" in data

    def test_returns_sensitive_fields(self, client):
        resp = client.post("/graphql/advanced", json={"query": "{ users { id name email role password_hash } }"})
        data = resp.get_json()
        assert "password_hash" in str(data)
