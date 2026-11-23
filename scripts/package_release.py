#!/usr/bin/env python3
"""Build a direct-to-project Novel Harness Starter release."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import re
import tarfile
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
SCAFFOLD = ROOT / "scaffold"
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?$")
REQUIRED_FILES = (
    "AGENTS.md",
    "workflow.md",
    ".agents/skills/novel-init/SKILL.md",
    ".agents/skills/novel-outline/SKILL.md",
    ".agents/skills/novel-continue/SKILL.md",
    "project/brief.md",
    "bible/world.md",
    "outline/master.md",
    "chapters/README.md",
    "state/current.md",
    "handoffs/_TEMPLATE.md",
    "reviews/_TEMPLATE.md",
    "templates/chapter-contract.md",
    "scripts/validate_novel.py",
    "docs/grilling.md",
    ".github/ISSUE_TEMPLATE/arc.yml",
)


def read_version(override: str | None = None) -> str:
    version = override if override is not None else (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not SEMVER.fullmatch(version):
        raise ValueError(f"Invalid semantic version: {version!r}")
    return version


def collect_files() -> dict[str, bytes]:
    if not SCAFFOLD.is_dir():
        raise FileNotFoundError(f"Missing project template directory: {SCAFFOLD}")
    files = {
        path.relative_to(SCAFFOLD).as_posix(): path.read_bytes()
        for path in sorted(SCAFFOLD.rglob("*"))
        if path.is_file()
        and "tests" not in path.relative_to(SCAFFOLD).parts
    }
    for metadata in ("VERSION", "CHANGELOG.md"):
        source = ROOT / metadata
        if not source.is_file():
            raise FileNotFoundError(f"Missing release metadata: {metadata}")
        files[metadata] = source.read_bytes()
    missing = sorted(set(REQUIRED_FILES) - files.keys())
    if missing:
        raise ValueError("Starter template is missing required files: " + ", ".join(missing))
    if "README.md" not in files:
        raise ValueError("The project Starter needs scaffold/README.md at its root")
    return files


def write_zip(path: Path, files: dict[str, bytes]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, content in sorted(files.items()):
            item = zipfile.ZipInfo(name, date_time=(2024, 1, 1, 0, 0, 0))
            item.compress_type = zipfile.ZIP_DEFLATED
            item.create_system = 3
            item.external_attr = 0o100644 << 16
            archive.writestr(item, content)


def write_tar_gz(path: Path, files: dict[str, bytes]) -> None:
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as archive:
                for name, content in sorted(files.items()):
                    item = tarfile.TarInfo(name=PurePosixPath(name).as_posix())
                    item.size = len(content)
                    item.mtime = 0
                    item.mode = 0o644
                    item.uid = 0
                    item.gid = 0
                    item.uname = ""
                    item.gname = ""
                    archive.addfile(item, io.BytesIO(content))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build(output_dir: Path, version: str | None = None) -> list[Path]:
    version = read_version(version)
    output_dir.mkdir(parents=True, exist_ok=True)
    files = collect_files()
    zip_path = output_dir / f"Novel-Harness-Project-Starter-v{version}.zip"
    tar_path = output_dir / f"Novel-Harness-Project-Starter-v{version}.tar.gz"
    write_zip(zip_path, files)
    write_tar_gz(tar_path, files)
    sums_path = output_dir / f"Novel-Harness-Project-Starter-v{version}-SHA256SUMS.txt"
    sums_path.write_text(
        "".join(f"{sha256(path)}  {path.name}\n" for path in (zip_path, tar_path)),
        encoding="ascii",
        newline="\n",
    )
    return [zip_path, tar_path, sums_path]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    parser.add_argument("--version", help="Override VERSION after validating SemVer")
    args = parser.parse_args()
    for path in build(args.output_dir, args.version):
        print(f"BUILT {path} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
