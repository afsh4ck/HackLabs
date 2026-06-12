"""WSTG-SEIN-01: SQL Injection check module."""

import requests
from . import CheckStatus, Severity
from .base import BaseCheck

SQLI_PAYLOADS = [
    ("single-quote", "'", "error"),
    ("OR tautology", "' OR '1'='1", "error"),
    ("UNION probe", "' UNION SELECT NULL--", "error"),
    ("boolean TRUE", "' AND 1=1--", "boolean"),
    ("boolean FALSE", "' AND 1=2--", "boolean"),
]

SQL_ERROR_PATTERNS = [
    "sql syntax", "mysql", "sqlite", "postgresql", "ora-",
    "unclosed quotation", "quoted string not properly terminated",
]


class SqliCheck(BaseCheck):
    name = "sqli"
    wstg_category = "WSTG-SEIN-01"
    default_severity = Severity.HIGH

    def run(self):
        paths = self.profile.get("paths", [])
        if not paths:
            return self._error("No paths in profile")

        for path_cfg in paths:
            path, params = path_cfg.get("path", "/"), path_cfg.get("params", [])
            for param in params:
                result = self._test_param(path, param)
                if result.status == CheckStatus.VULNERABLE:
                    return result
        return self._safe(f"Tested {sum(len(p.get('params', [])) for p in paths)} param(s)")

    def _test_param(self, path: str, param: str):
        for label, payload, method in SQLI_PAYLOADS:
            try:
                resp = self._get(path, params={param: payload})
            except requests.RequestException:
                continue
            if method == "error" and any(p in resp.text.lower() for p in SQL_ERROR_PATTERNS):
                return self._vuln(f"Param '{param}' — {label} triggered SQL error")

        try:
            rt = self._get(path, params={param: "' AND 1=1--"})
            rf = self._get(path, params={param: "' AND 1=2--"})
            if rt.status_code == rf.status_code and len(rt.text) != len(rf.text):
                return self._vuln(f"Param '{param}' — boolean differential detected")
        except requests.RequestException:
            pass
        return self._safe(f"Param '{param}' clean")
