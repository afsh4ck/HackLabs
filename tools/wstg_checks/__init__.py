"""WSTG Check modules — data models and base class."""

from dataclasses import dataclass
from enum import Enum


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class CheckStatus(str, Enum):
    VULNERABLE = "vulnerable"
    NOT_VULNERABLE = "not_vulnerable"
    ERROR = "error"


@dataclass
class CheckResult:
    name: str
    status: CheckStatus
    evidence: str = ""
    severity: Severity = Severity.INFO
    wstg_category: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name, "status": self.status.value,
            "evidence": self.evidence, "severity": self.severity.value,
            "wstg_category": self.wstg_category,
        }
