"""WSTG-INPV-07: OS Command Injection check module."""

import time
import requests
from . import CheckStatus, Severity
from .base import BaseCheck

CMDI_MARKER = "HL-CMDI"
CMDI_PAYLOADS = [
    ("pipe", f"| echo {CMDI_MARKER}"),
    ("semicolon", f"; echo {CMDI_MARKER}"),
    ("backtick", f"`echo {CMDI_MARKER}`"),
    ("$() subshell", f"$(echo {CMDI_MARKER})"),
]
TIME_DELAY = "; sleep 3"
TIME_THRESHOLD = 2.5


class CmdiCheck(BaseCheck):
    name = "cmdi"
    wstg_category = "WSTG-INPV-07"
    default_severity = Severity.CRITICAL

    def run(self):
        paths = self.profile.get("paths", [])
        if not paths:
            return self._error("No paths in profile")

        for path_cfg in paths:
            path, params = path_cfg.get("path", "/"), path_cfg.get("params", [])
            for param in params:
                for detection in (self._test_output, self._test_timing):
                    result = detection(path, param)
                    if result.status == CheckStatus.VULNERABLE:
                        return result
        return self._safe("No command injection detected")

    def _test_output(self, path: str, param: str):
        for label, payload in CMDI_PAYLOADS:
            try:
                if CMDI_MARKER in self._get(path, params={param: payload}).text:
                    return self._vuln(f"Param '{param}' — {label} produced command output")
            except requests.RequestException:
                continue
        return self._safe()

    def _test_timing(self, path: str, param: str):
        try:
            t0 = time.time()
            self._get(path, params={param: "normaltest"})
            baseline = time.time() - t0
            t0 = time.time()
            self._get(path, params={param: TIME_DELAY})
            elapsed = time.time() - t0
            if elapsed - baseline > TIME_THRESHOLD:
                return self._vuln(
                    f"Param '{param}' — time-based injection ({elapsed:.1f}s vs {baseline:.1f}s)")
        except requests.RequestException:
            pass
        return self._safe()
