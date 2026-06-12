#!/usr/bin/env python3
"""HackLabs WSTG-Scan — CLI entry point.

Usage:
    python wstg-scan.py --target http://localhost:5000 --profile sqli-lab
    python wstg-scan.py --target http://localhost:5000 --profile xss-lab --checks sqli,xss
    python wstg-scan.py --list-profiles
    python wstg-scan.py --list-profiles --verbose
    python wstg-scan.py --target http://localhost:5000 --auto-scan
"""
import argparse, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from wstg_profile import load_profile, list_profiles, list_profiles_with_info, discover_profile_for_check
from wstg_checks import CheckStatus

CHECK_MODULES = {
    "sqli": "wstg_checks.sqli",
    "xss": "wstg_checks.xss",
    "cmdi": "wstg_checks.cmdi",
    "ssrf": "wstg_checks.ssrf",
    "idor": "wstg_checks.idor",
    "csrf": "wstg_checks.csrf",
    "path_traversal": "wstg_checks.path_traversal",
    "xxe": "wstg_checks.xxe",
    "ssti": "wstg_checks.ssti",
    "open_redirect": "wstg_checks.open_redirect",
    "clickjacking": "wstg_checks.clickjacking",
    "session_hijacking": "wstg_checks.session_hijacking",
    "jwt": "wstg_checks.jwt",
    "deserialization": "wstg_checks.deserialization",
    "business_logic": "wstg_checks.business_logic",
    "ai_attacks": "wstg_checks.ai_attacks",
    "html_injection": "wstg_checks.html_injection",
    "cors": "wstg_checks.cors",
    "api_attacks": "wstg_checks.api_attacks",
    "file_upload": "wstg_checks.file_upload",
}

# Map profile names to their primary check module
PROFILE_CHECK_MAP = {
    "sqli-lab": "sqli",
    "xss-lab": "xss",
    "ssrf-lab": "ssrf",
    "idor-lab": "idor",
    "csrf-lab": "csrf",
    "path-traversal-lab": "path_traversal",
    "xxe-lab": "xxe",
    "ssti-lab": "ssti",
    "open-redirect-lab": "open_redirect",
    "clickjacking-lab": "clickjacking",
    "session-hijacking-lab": "session_hijacking",
    "jwt-lab": "jwt",
    "deserialization-lab": "deserialization",
    "business-logic-lab": "business_logic",
    "ai-attacks-lab": "ai_attacks",
    "html-injection-lab": "html_injection",
    "cors-lab": "cors",
    "api-attacks-lab": "api_attacks",
    "file-upload-lab": "file_upload",
}


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
        mod_path = CHECK_MODULES[name]
        try:
            mod = __import__(mod_path, fromlist=[name.title()])
        except ImportError as e:
            print(f"[!] Cannot import {mod_path}: {e}", file=sys.stderr)
            summary["errors"] += 1
            continue
        check_cls = getattr(mod, f"{name.title()}Check", None)
        if check_cls is None:
            print(f"[!] No {name.title()}Check class in {mod_path}", file=sys.stderr)
            summary["errors"] += 1
            continue
        check = check_cls(profile, timeout=timeout)
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


def auto_discover_checks(profile_name):
    """Determine which checks to run based on the profile name."""
    check_name = PROFILE_CHECK_MAP.get(profile_name)
    if check_name:
        return [check_name]
    return None


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


def print_profiles_verbose():
    """Print detailed profile listing."""
    profiles = list_profiles_with_info()
    print(f"\n{'=' * 70}")
    print(f"  Available WSTG Profiles ({len(profiles)} total)")
    print(f"{'=' * 70}")
    for p in profiles:
        if "error" in p:
            print(f"  {p['name']:30s}  ERROR: {p['error']}")
        else:
            cats = ", ".join(p.get("wstg_categories", []))
            print(f"  {p['name']:30s}  {p['lab_name'][:30]:30s}  eps:{p['endpoint_count']:2d}  {cats}")
    print(f"{'=' * 70}")


def main():
    p = argparse.ArgumentParser(description="HackLabs WSTG-Scan — web security scanner")
    p.add_argument("--target", "-t", help="Target base URL (overrides profile)")
    p.add_argument("--profile", "-p", help="Profile name (without .yaml)")
    p.add_argument("--checks", "-c", help="Comma-separated checks (default: all)")
    p.add_argument("--timeout", type=int, default=10, help="HTTP timeout seconds")
    p.add_argument("--output", "-o", choices=["text", "json"], default="text")
    p.add_argument("--list-profiles", action="store_true", help="List available profiles")
    p.add_argument("--verbose", "-v", action="store_true", help="Verbose profile listing")
    p.add_argument("--auto-scan", action="store_true", help="Auto-discover checks from profile")
    args = p.parse_args()
    if args.list_profiles:
        if args.verbose:
            print_profiles_verbose()
        else:
            for name in list_profiles(): print(f"  - {name}")
        return
    if not args.profile:
        p.error("--profile is required (or use --list-profiles)")
    checks = args.checks.split(",") if args.checks else None
    if args.auto_scan and not checks:
        checks = auto_discover_checks(args.profile)
    report = run_checks(args.target, args.profile, checks, args.timeout, quiet=(args.output == "json"))
    if args.output == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print_report(report)
    sys.exit(1 if report["summary"]["vulnerable"] > 0 else 0)


if __name__ == "__main__":
    main()
