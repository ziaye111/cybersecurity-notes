"""Non-invasive web posture checks.

ScopeGuard intentionally asks a target only for its normal HTTP response and
TLS certificate metadata. It does not brute-force, exploit, crawl, or mutate
anything. Keep the checks boring: boring is easier to review and safer to run.
"""

from __future__ import annotations

import socket
import ssl
from datetime import datetime, timezone
from urllib.error import URLError
from urllib.request import Request, urlopen
from urllib.parse import urlparse

from .models import Finding, ScanReport

USER_AGENT = "ScopeGuard/0.1 (authorized security assessment)"


def _normalise_target(raw_target: str) -> tuple[str, str, int]:
    target = raw_target if "://" in raw_target else f"https://{raw_target}"
    parsed = urlparse(target)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("target must be an HTTP(S) URL with a hostname")
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    return target.rstrip("/"), parsed.hostname, port


def _request(target: str, timeout: float) -> tuple[object, dict[str, str]]:
    request = Request(target, headers={"User-Agent": USER_AGENT}, method="GET")
    with urlopen(request, timeout=timeout) as response:
        return response, {key.lower(): value for key, value in response.headers.items()}


def _http_findings(target: str, timeout: float) -> tuple[list[Finding], list[str]]:
    findings: list[Finding] = []
    errors: list[str] = []
    try:
        response, headers = _request(target, timeout)
    except (OSError, URLError) as error:
        return [], [f"HTTP check failed: {error}"]

    if urlparse(target).scheme == "http":
        findings.append(Finding(
            "transport", "high", "HTTP is in use",
            "The target URL uses unencrypted HTTP, so traffic can be read or changed in transit.",
            "Serve the application over HTTPS and redirect HTTP to HTTPS.",
        ))

    checks = {
        "x-content-type-options": (
            "medium", "MIME sniffing protection is missing",
            "Browsers may guess content types when this response header is absent.",
            "Add X-Content-Type-Options: nosniff.",
        ),
        "content-security-policy": (
            "medium", "Content Security Policy is missing",
            "The response does not declare a browser policy that limits executable content.",
            "Define a restrictive Content-Security-Policy appropriate for the application.",
        ),
        "referrer-policy": (
            "low", "Referrer-Policy is missing",
            "Cross-site requests may disclose more URL information than intended.",
            "Add a deliberate Referrer-Policy, such as strict-origin-when-cross-origin.",
        ),
    }
    for header, (severity, title, detail, recommendation) in checks.items():
        if header not in headers:
            findings.append(Finding("headers", severity, title, detail, recommendation))

    if "strict-transport-security" not in headers and urlparse(target).scheme == "https":
        findings.append(Finding(
            "headers", "medium", "HSTS is missing",
            "HTTPS responses do not ask browsers to keep using HTTPS for this host.",
            "Add Strict-Transport-Security after confirming every subresource and endpoint supports HTTPS.",
        ))

    server = headers.get("server")
    if server:
        findings.append(Finding(
            "information", "low", "Server header is exposed",
            f"The response identifies its server as {server!r}.",
            "Remove or minimise version and product details where practical.",
        ))

    status = getattr(response, "status", 200)
    if status >= 400:
        errors.append(f"Target returned HTTP status {status}; findings may be incomplete.")
    return findings, errors


def _tls_findings(hostname: str, port: int, timeout: float) -> tuple[list[Finding], list[str]]:
    findings: list[Finding] = []
    errors: list[str] = []
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, port), timeout=timeout) as connection:
            with context.wrap_socket(connection, server_hostname=hostname) as tls_socket:
                certificate = tls_socket.getpeercert()
                if not certificate:
                    errors.append("TLS certificate details were unavailable.")
    except (OSError, ssl.SSLError) as error:
        return [], [f"TLS check failed: {error}"]
    return findings, errors


def scan(raw_target: str, timeout: float = 5.0) -> ScanReport:
    """Run the small set of read-only checks and return a serialisable report."""
    target, hostname, port = _normalise_target(raw_target)
    findings, errors = _http_findings(target, timeout)
    if urlparse(target).scheme == "https":
        tls_findings, tls_errors = _tls_findings(hostname, port, timeout)
        findings.extend(tls_findings)
        errors.extend(tls_errors)
    return ScanReport(
        target=target,
        checked_at=datetime.now(timezone.utc).isoformat(),
        findings=findings,
        errors=errors,
    )
