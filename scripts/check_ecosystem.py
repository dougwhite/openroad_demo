"""Read the demo's release pin and verify its offline validation checkout."""

import argparse
import re
import subprocess
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read_pin(root: Path = ROOT) -> dict:
    pin = tomllib.loads((root / "ecosystem.toml").read_text(encoding="utf-8"))
    if type(pin.get("source_version")) is not int or pin["source_version"] < 1:
        raise ValueError("source_version must be a positive integer")
    revision = pin.get("gorak_revision")
    if not isinstance(revision, str) or not re.fullmatch(
        r"v\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", revision
    ):
        raise ValueError("gorak_revision must be a release tag")
    return pin


def check_checkout(checkout: Path, pin: dict) -> None:
    def git(*args: str) -> str:
        return subprocess.check_output(
            ["git", "-C", str(checkout), *args], text=True
        ).strip()

    # Explicit tag lookup accepts both lightweight and annotated release tags.
    tagged = git("rev-parse", f"refs/tags/{pin['gorak_revision']}^{{commit}}")
    if git("rev-parse", "HEAD") != tagged:
        raise ValueError("gorak checkout does not match gorak_revision")
    if git("status", "--porcelain", "--untracked-files=all"):
        raise ValueError("gorak checkout has local changes")
    upstream = tomllib.loads((checkout / "ecosystem.toml").read_text(encoding="utf-8"))
    if type(upstream.get("source_version")) is not int or (
        upstream["source_version"] != pin["source_version"]
    ):
        raise ValueError("gorak source_version does not match the demo contract")
    print(
        f"Verified gorak {pin['gorak_revision']}, source_version {pin['source_version']}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--github-output", type=Path)
    parser.add_argument("--checkout", type=Path)
    args = parser.parse_args()
    pin = read_pin()
    if args.github_output:
        with args.github_output.open("a", encoding="utf-8") as output:
            output.write(f"gorak_revision={pin['gorak_revision']}\n")
    if args.checkout:
        check_checkout(args.checkout, pin)
