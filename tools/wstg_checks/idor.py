"""WSTG-INPV-04: Insecure Direct Object Reference (IDOR) check module."""

import re
import requests
from . import CheckStatus, Severity
from .base import BaseCheck

IDEN_PATTERN = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}", re.I)


class IdorCheck(BaseCheck):
    name = "idor"
    wstg_category = "WSTG-INPV-04"
    default_severity = Severity.MEDIUM

    def run(self):
        endpoints = self.profile.get("endpoints", self.profile.get("paths", []))
        if not endpoints:
            return self._error("No endpoints in profile")

        for ep in endpoints:
            path = ep.get("path", "/")
            params = ep.get("params", [])
            for param in params:
                result = self._test_param(path, param, ep.get("method", "GET"))
                if result.status == CheckStatus.VULNERABLE:
                    return result
        total = sum(len(ep.get("params", [])) for ep in endpoints)
        return self._safe(f"Tested {total} param(s), no IDOR detected")

    def _test_param(self, path: str, param: str, method: str):
        # Step 1: Fetch baseline with original value
        baseline = self._fetch(path, param, method, "1")
        if baseline is None:
            return self._safe(f"Param '{param}' — baseline request failed")

        # Step 2: Try sequential enumeration
        for alt in ("2", "3", "0", "999"):
            resp = self._fetch(path, param, method, alt)
            if resp is None:
                continue
            if self._objects_differ(baseline, resp, alt):
                return self._vuln(
                    f"Param '{param}' — object enumerable (ID {alt} accessible)")

        # Step 3: Try UUID-style manipulation if value looks like a UUID
        orig_val = self._get_original(path, param, method)
        if orig_val and IDEN_PATTERN.match(orig_val):
            mutated = self._mutate_uuid(orig_val)
            if mutated:
                resp = self._fetch(path, param, method, mutated)
                if resp and self._objects_differ(baseline, resp, mutated):
                    return self._vuln(
                        f"Param '{param}' — UUID manipulation succeeded ({mutated})")

        return self._safe(f"Param '{param}' — no IDOR detected")

    def _fetch(self, path: str, param: str, method: str, value: str):
        try:
            if method.upper() == "POST":
                return self._post(path, data={param: value})
            return self._get(path, params={param: value})
        except requests.RequestException:
            return None

    def _get_original(self, path: str, param: str, method: str):
        """Try to read the original param value from the profile path config."""
        for ep in self.profile.get("endpoints", self.profile.get("paths", [])):
            if ep.get("path") == path:
                return str(ep.get("original_values", {}).get(param, "1"))
        return "1"

    def _objects_differ(self, baseline, response, tested_id: str) -> bool:
        """Two objects are different if status codes differ or body content differs."""
        if response.status_code == 403 or response.status_code == 404:
            return False
        if response.status_code != baseline.status_code:
            return True
        if response.text != baseline.text and len(response.text) > 0:
            return True
        return False

    @staticmethod
    def _mutate_uuid(uuid_str: str) -> str | None:
        """Increment last hex char of UUID to produce a nearby ID."""
        if len(uuid_str) < 8:
            return None
        last = uuid_str[-1]
        try:
            nxt = hex((int(last, 16) + 1) % 16)[2:]
        except ValueError:
            return None
        return uuid_str[:-1] + nxt
