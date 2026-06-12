"""Base class for WSTG security check modules."""

from abc import ABC, abstractmethod

import requests

from . import CheckResult, CheckStatus, Severity


class BaseCheck(ABC):
    name: str = "base"
    wstg_category: str = ""
    default_severity: Severity = Severity.MEDIUM

    def __init__(self, profile: dict, timeout: int = 10):
        self.profile = profile
        self.base_url = profile.get("base_url", "").rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers["User-Agent"] = "HackLabs-WSTG-Scanner/0.1"

    @abstractmethod
    def run(self) -> CheckResult: ...

    def _get(self, path: str, **kw):
        return self.session.get(f"{self.base_url}{path}", timeout=self.timeout, **kw)

    def _post(self, path: str, **kw):
        return self.session.post(f"{self.base_url}{path}", timeout=self.timeout, **kw)

    def _error(self, msg: str) -> CheckResult:
        return CheckResult(self.name, CheckStatus.ERROR, msg, Severity.INFO, self.wstg_category)

    def _vuln(self, evidence: str, severity: Severity | None = None) -> CheckResult:
        return CheckResult(self.name, CheckStatus.VULNERABLE, evidence,
                           severity or self.default_severity, self.wstg_category)

    def _safe(self, evidence: str = "No vulnerability detected") -> CheckResult:
        return CheckResult(self.name, CheckStatus.NOT_VULNERABLE, evidence,
                           Severity.INFO, self.wstg_category)
