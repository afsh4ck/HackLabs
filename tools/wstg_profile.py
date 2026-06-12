"""YAML profile loader for WSTG scans."""

from pathlib import Path
import yaml

DEFAULT_PROFILE_DIR = Path(__file__).parent / "profiles"


def load_profile(name: str, profile_dir: str | Path | None = None) -> dict:
    if not name.endswith(".yaml"):
        name += ".yaml"
    search_dir = Path(profile_dir) if profile_dir else DEFAULT_PROFILE_DIR
    path = search_dir / name
    if not path.exists():
        raise FileNotFoundError(f"Profile not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        profile = yaml.safe_load(f)
    for field in ("lab_name", "base_url"):
        if field not in profile:
            raise ValueError(f"Profile '{path.name}' missing required field: {field}")
    return profile


def list_profiles(profile_dir: str | Path | None = None) -> list[str]:
    search_dir = Path(profile_dir) if profile_dir else DEFAULT_PROFILE_DIR
    return sorted(p.stem for p in search_dir.glob("*.yaml"))
