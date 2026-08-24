"""Command-line interface for ScopeGuard."""

from __future__ import annotations

import argparse
import json
import sys

from .scanner import scan


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="scopeguard",
        description="Run read-only security posture checks against an authorised web target.",
    )
    parser.add_argument("target", help="HTTP(S) URL you are authorised to assess")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    parser.add_argument("--timeout", type=float, default=5.0, help="network timeout in seconds (default: 5)")
    parser.add_argument(
        "--i-have-authorization",
        action="store_true",
        help="confirm that you own or have written permission to assess this target",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.i_have_authorization:
        print("Refusing to scan: pass --i-have-authorization for an approved target.", file=sys.stderr)
        return 2
    if args.timeout <= 0:
        print("Timeout must be greater than zero.", file=sys.stderr)
        return 2
    try:
        report = scan(args.target, args.timeout)
    except ValueError as error:
        print(f"Invalid target: {error}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report.as_dict(), indent=2))
        return 0
    print(f"ScopeGuard report for {report.target}")
    print(f"Checked at: {report.checked_at}")
    for finding in report.findings:
        print(f"[{finding.severity.upper()}] {finding.title}\n  {finding.detail}\n  Next step: {finding.recommendation}")
    if not report.findings:
        print("No observations from the configured checks.")
    for error in report.errors:
        print(f"[NOTE] {error}")
    return 0
