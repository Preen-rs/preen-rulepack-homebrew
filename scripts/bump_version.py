#!/usr/bin/env python3
from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "manifest.toml"
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")


def fail(msg: str) -> None:
    print(f"bump failed: {msg}", file=sys.stderr)
    raise SystemExit(1)


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, cwd=ROOT)


def ensure_semver(version: str) -> None:
    if not SEMVER_RE.fullmatch(version):
        fail(f"invalid version `{version}` (expected semver)")


def replace_manifest_version(version: str) -> tuple[str, str]:
    if not MANIFEST_PATH.exists():
        fail("manifest.toml is missing")
    lines = MANIFEST_PATH.read_text(encoding="utf-8").splitlines(keepends=True)
    old_version = ""
    for idx, line in enumerate(lines):
        if line.startswith("version = "):
            old_version = line.strip().split('"')[1]
            lines[idx] = f'version = "{version}"\n'
            MANIFEST_PATH.write_text("".join(lines), encoding="utf-8")
            return old_version, version
    fail("manifest.toml does not contain `version = ...`")
    raise AssertionError("unreachable")


def ensure_git_clean() -> None:
    out = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    if out.stdout.strip():
        fail("git working tree is not clean; commit or stash changes first")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Bump manifest version for a Preen rulepack."
    )
    parser.add_argument("version", help="target version (example: 1.0.3)")
    parser.add_argument(
        "--commit",
        action="store_true",
        help="create a git commit for manifest.toml update",
    )
    args = parser.parse_args()

    ensure_semver(args.version)
    if args.commit:
        ensure_git_clean()
    old, new = replace_manifest_version(args.version)
    print(f"manifest version updated: {old} -> {new}")

    if args.commit:
        run(["git", "add", "manifest.toml"])
        run(["git", "commit", "-m", f"chore: bump rulepack version to {new}"])
        print("created commit for manifest version bump")

    print("next: run Sign Manifest workflow, then create/push tag v{new}")


if __name__ == "__main__":
    main()
