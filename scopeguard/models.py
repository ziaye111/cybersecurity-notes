"""Data structures shared by the scanner and report renderers."""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class Finding:
    """One observation, written so a human can decide what to do next."""

    check: str
    severity: str
    title: str
    detail: str
    recommendation: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ScanReport:
    """The complete result of one deliberately small assessment."""

    target: str
    checked_at: str
    findings: list[Finding]
    errors: list[str]

    def as_dict(self) -> dict[str, Any]:
        return {
            "target": self.target,
            "checked_at": self.checked_at,
            "findings": [finding.as_dict() for finding in self.findings],
            "errors": self.errors,
        }
