"""YAML profile loader for WSTG scans."""

import hashlib
import json
from pathlib import Path

import yaml

DEFAULT_PROFILE_DIR = Path(__file__).parent / "profiles"

# Required fields for a valid profile
REQUIRED_FIELDS = ("lab_name", "base_url")
# Optional but recommended
RECOMMENDED_FIELDS = ("description", "wstg_categories", "endpoints")


def _normalize_endpoints(profile: dict) -> dict:
    """Normalize profiles that use 'paths' instead of 'endpoints'."""
    if "endpoints" not in profile and "paths" in profile:
        profile["endpoints"] = profile.pop("paths")
    return profile


def _validate_profile(profile: dict, path: Path) -> list[str]:
    """Validate profile structure. Returns list of errors (empty = valid)."""
    errors = []
    for field in REQUIRED_FIELDS:
        if field not in profile:
            errors.append(f"Missing required field: {field}")
    if "endpoints" not in profile and "paths" not in profile:
        errors.append("Missing endpoints or paths list")
    if "wstg_categories" in profile and not isinstance(profile["wstg_categories"], list):
        errors.append("wstg_categories must be a list")
    if "endpoints" in profile and not isinstance(profile["endpoints"], list):
        errors.append("endpoints must be a list")
    return errors


def profile_hash(profile: dict) -> str:
    """Compute a deterministic SHA-256 hash of the profile content."""
    canonical = json.dumps(profile, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]


def load_profile(name: str, profile_dir: str | Path | None = None) -> dict:
    """Load a YAML profile by name, with dual-key normalization and validation."""
    if not name.endswith(".yaml"):
        name += ".yaml"
    search_dir = Path(profile_dir) if profile_dir else DEFAULT_PROFILE_DIR
    path = search_dir / name
    if not path.exists():
        raise FileNotFoundError(f"Profile not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        profile = yaml.safe_load(f)
    errors = _validate_profile(profile, path)
    if errors:
        raise ValueError(f"Profile '{path.name}' invalid: {'; '.join(errors)}")
    profile = _normalize_endpoints(profile)
    profile["_hash"] = profile_hash(profile)
    profile["_source"] = str(path)
    return profile


def list_profiles(profile_dir: str | Path | None = None) -> list[str]:
    """List available profile names (without .yaml extension)."""
    search_dir = Path(profile_dir) if profile_dir else DEFAULT_PROFILE_DIR
    return sorted(p.stem for p in search_dir.glob("*.yaml"))


def list_profiles_with_info(profile_dir: str | Path | None = None) -> list[dict]:
    """List profiles with metadata (name, lab_name, hash, endpoint count)."""
    results = []
    for name in list_profiles(profile_dir):
        try:
            profile = load_profile(name, profile_dir)
            eps = profile.get("endpoints", [])
            results.append({
                "name": name,
                "lab_name": profile.get("lab_name", ""),
                "hash": profile.get("_hash", ""),
                "endpoint_count": len(eps),
                "wstg_categories": profile.get("wstg_categories", []),
            })
        except Exception as e:
            results.append({"name": name, "error": str(e)})
    return results


def discover_profile_for_check(check_name: str, profile_dir: str | Path | None = None) -> str | None:
    """Auto-discover the best profile for a given check module name.

    Maps check module names (e.g., 'sqli', 'path_traversal') to profile names
    (e.g., 'sqli-lab', 'path-traversal-lab').
    Returns profile name or None if not found.
    """
    # Normalize check_name: underscores to hyphens
    normalized = check_name.replace("_", "-")
    candidates = [
        f"{normalized}-lab",
        normalized,
        f"{check_name}-lab",
        check_name,
    ]
    available = list_profiles(profile_dir)
    for candidate in candidates:
        if candidate in available:
            return candidate
    return None
