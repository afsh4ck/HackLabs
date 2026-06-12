"""WSTG-INPV-19: Server-Side Request Forgery (SSRF) check module."""

import re
import requests
from urllib.parse import urljoin
from . import CheckStatus, Severity
from .base import BaseCheck

SSRF_MARKER = "HLSSRF7b2c"
SSRF_PAYLOADS = [
    ("localhost loopback", "http://127.0.0.1/"),
    ("localhost name", "http://localhost/"),
    ("metadata AWS", "http://169.254.169.254/latest/meta-data/"),
    ("metadata GCP", "http://metadata.google.internal/computeMetadata/v1/"),
    ("file protocol", f"file:///etc/passwd"),
    ("dict protocol", f"dict://127.0.0.1:6379/info"),
]

METADATA_MARKERS = [
    "ami-id", "instance-id", "meta-data",
    "computeMetadata", "metadata-flavor",
]

REDIRECT_BODY_MARKERS = [
    "root:", "daemon:", "nobody:",  # /etc/passwd
    "ami-id", "instance-id",        # AWS metadata
]


class SsrfCheck(BaseCheck):
    name = "ssrf"
    wstg_category = "WSTG-INPV-19"
    default_severity = Severity.HIGH

    def run(self):
        endpoints = self.profile.get("endpoints", self.profile.get("paths", []))
        if not endpoints:
            return self._error("No endpoints in profile")

        for ep in endpoints:
            path = ep.get("path", "/")
            params = ep.get("params", [])
            for param in params:
                result = self._test_param(path, param)
                if result.status == CheckStatus.VULNERABLE:
                    return result
        total = sum(len(ep.get("params", [])) for ep in endpoints)
        return self._safe(f"Tested {total} param(s), no SSRF detected")

    def _test_param(self, path: str, param: str):
        for label, payload in SSRF_PAYLOADS:
            try:
                resp = self._get(path, params={param: payload})
            except requests.RequestException:
                continue
            if self._check_response(resp, label, param):
                return self._vuln(f"Param '{param}' — {label} fetched internal resource")
        return self._safe(f"Param '{param}' — no SSRF via direct payloads")

    def _check_response(self, resp, label: str, param: str) -> bool:
        body = resp.text.lower()
        if not body:
            return False
        # file:// protocol — look for passwd content
        if "file://" in label:
            return any(m in body for m in REDIRECT_BODY_MARKERS[:3])
        # metadata endpoints
        if "metadata" in label:
            return any(m.lower() in body for m in METADATA_MARKERS)
        # localhost/127.0.0.1 — look for server-specific content or error leaking
        if "127.0.0.1" in payload_str(label) or "localhost" in payload_str(label):
            # Heuristic: if response differs from a normal 404/error,
            # or contains internal server info
            return self._has_internal_leak(body, resp.status_code)
        return False

    def _has_internal_leak(self, body: str, status: int) -> bool:
        """Detect internal information leakage in SSRF responses."""
        internal_patterns = [
            r"127\.\d+\.\d+\.\d+",
            r"192\.168\.\d+\.\d+",
            r"10\.\d+\.\d+\.\d+",
            r"172\.(1[6-9]|2\d|3[01])\.\d+\.\d+",
        ]
        for pat in internal_patterns:
            if re.search(pat, body):
                return True
        return False


def payload_str(label: str) -> str:
    """Extract the URL value from a payload label for matching."""
    for lbl, url in SSRF_PAYLOADS:
        if lbl == label:
            return url
    return label
