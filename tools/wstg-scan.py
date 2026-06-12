#!/usr/bin/env python3
"""HackLabs WSTG-Scan — CLI entry point.

Usage:
    python wstg-scan.py --target http://localhost:5000 --profile sqli-lab
    python wstg-scan.py --target http://localhost:5000 --profile xss-lab --checks sqli,xss
    python wstg-scan.py --list-profiles
"""
import argparse, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from wstg_profile import load_profile, list_profiles
from wstg_checks import CheckStatus

CHECK_MODULES = {"sqli": "wstg_checks.sqli", "xss": "wstg_checks.xss", "cmdi": "wstg_checks.cmdi"}


def run_checks(target, profile_name, checks=None, timeout=10, quiet=False):
    profile = load_profile(profile_name)
    if target:
        profile["base_url"] = target
    selected = checks or list(CHECK_MODULES.keys())
    results, summary = [], {"total": 0, "vulnerable": 0, "safe": 0, "errors": 0}
    out = sys.stderr if quiet else sys.stdout
    for name in selected:
        if name not in CHECK_MODULES:
            print(f"[!] Unknown check: {name}", file=sys.stderr); continue
        mod = __import__(CHECK_MODULES[name], fromlist=[name.title()])
        check = getattr(mod, f"{name.title()}Check")(profile, timeout=timeout)
        print(f"[*] Running: {name} ({check.wstg_category})", file=out)
        result = check.run()
        results.append(result.to_dict())
        summary["total"] += 1
        if result.status == CheckStatus.VULNERABLE:
            summary["vulnerable"] += 1; print(f"    [!] VULNERABLE — {result.evidence}", file=out)
        elif result.status == CheckStatus.NOT_VULNERABLE:
            summary["safe"] += 1; print(f"    [+] Safe — {result.evidence}", file=out)
        else:
            summary["errors"] += 1; print(f"    [-] Error — {result.evidence}", file=out)
    return {"target": profile.get("base_url"), "profile": profile_name, "summary": summary, "results": results}


def print_report(report):
    s = report["summary"]
    print(f"\n{'=' * 60}\n  WSTG-SCAN Report — {report['target']}\n  Profile: {report['profile']}\n{'=' * 60}")
    print(f"  Checks: {s['total']}  |  Vulnerable: {s['vulnerable']}  |  Safe: {s['safe']}  |  Errors: {s['errors']}")
    print("-" * 60)
    for r in report["results"]:
        icon = "!" if r["status"] == "vulnerable" else "+" if r["status"] == "not_vulnerable" else "-"
        sev = f" [{r['severity'].upper()}]" if r["status"] == "vulnerable" else ""
        print(f"  [{icon}] {r['name']}{sev} — {r['evidence']}")
    print("=" * 60)


def main():
    p = argparse.ArgumentParser(description="HackLabs WSTG-Scan — web security scanner")
    p.add_argument("--target", "-t", help="Target base URL (overrides profile)")
    p.add_argument("--profile", "-p", help="Profile name (without .yaml)")
    p.add_argument("--checks", "-c", help="Comma-separated checks (default: all)")
    p.add_argument("--timeout", type=int, default=10, help="HTTP timeout seconds")
    p.add_argument("--output", "-o", choices=["text", "json"], default="text")
    p.add_argument("--list-profiles", action="store_true", help="List available profiles")
    args = p.parse_args()
    if args.list_profiles:
        for name in list_profiles(): print(f"  - {name}")
        return
    if not args.profile:
        p.error("--profile is required (or use --list-profiles)")
    checks = args.checks.split(",") if args.checks else None
    report = run_checks(args.target, args.profile, checks, args.timeout, quiet=(args.output == "json"))
    if args.output == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print_report(report)
    sys.exit(1 if report["summary"]["vulnerable"] > 0 else 0)


if __name__ == "__main__":
    main()
