"""WSTG-INPV-02: Cross-Site Scripting (XSS) check module."""

import html as _html
import requests
from . import CheckStatus, Severity
from .base import BaseCheck

MARKER = "HLXSS9f3a"
XSS_PAYLOADS = [
    ("basic tag", f"<{MARKER}></{MARKER}>"),
    ("event handler", f'" onmouseover="alert(1)"'),
    ("script break-out", f"</{MARKER}><script>var m='{MARKER}'</script>"),
]


class XssCheck(BaseCheck):
    name = "xss"
    wstg_category = "WSTG-INPV-02"
    default_severity = Severity.MEDIUM

    def run(self):
        paths = self.profile.get("endpoints", [])
        if not paths:
            return self._error("No endpoints in profile")

        for path_cfg in paths:
            path, params = path_cfg.get("path", "/"), path_cfg.get("params", [])
            for param in params:
                result = self._test_param(path, param)
                if result.status == CheckStatus.VULNERABLE:
                    return result
        return self._safe("No reflected XSS detected")

    def _test_param(self, path: str, param: str):
        for label, payload in XSS_PAYLOADS:
            try:
                resp = self._get(path, params={param: payload})
            except requests.RequestException:
                continue
            body = resp.text
            if MARKER in body:
                escaped = _html.escape(MARKER)
                if escaped not in body or body.count(MARKER) > body.count(escaped):
                    return self._vuln(f"Param '{param}' — {label} reflected without encoding")
        return self._safe(f"Param '{param}' — reflection absent or encoded")
