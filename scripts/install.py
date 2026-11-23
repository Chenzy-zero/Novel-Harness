#!/usr/bin/env python3
"""Install the Novel Harness scaffold into an existing or new novel directory."""
import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCAFFOLD = ROOT / "scaffold"

def install(destination, force=False, dry_run=False):
    destination = destination.expanduser().resolve()
    if destination == ROOT or ROOT in destination.parents:
        raise ValueError("Do not install inside the harness source repository")
    if not SCAFFOLD.is_dir():
        raise RuntimeError("Missing scaffold directory")
    copied, skipped = [], []
    for source in sorted(SCAFFOLD.rglob("*")):
        if not source.is_file():
            continue
        relative = source.relative_to(SCAFFOLD)
        target = destination / relative
        if target.exists() and not force:
            skipped.append(str(relative))
            continue
        copied.append(str(relative))
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    for name in copied:
        print(("WOULD INSTALL " if dry_run else "INSTALLED ") + name)
    for name in skipped:
        print("SKIPPED existing " + name)
    print("Summary: {} installed, {} skipped".format(len(copied), len(skipped)))
    return copied, skipped

def main():
    parser = argparse.ArgumentParser(description="Initialize a novel workspace using Novel Harness")
    parser.add_argument("destination", help="Target novel repository or folder")
    parser.add_argument("--force", action="store_true", help="Overwrite existing scaffold files (may destroy work)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    install(Path(args.destination), args.force, args.dry_run)

if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, ValueError) as exc:
        print("ERROR:", exc, file=sys.stderr)
        sys.exit(1)
