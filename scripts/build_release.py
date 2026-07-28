#!/usr/bin/env python3
"""Build a deterministic Maya-module release archive."""

import argparse
import hashlib
import zipfile
from pathlib import Path

from .versioning import validate_version

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = REPOSITORY_ROOT / "src" / "jam_asset_manager"
PROJECT_NAME = "JAM-asset-manager"
ROOT_FILES = (
    REPOSITORY_ROOT / "CHANGELOG.md",
    REPOSITORY_ROOT / "JAM.mod",
    REPOSITORY_ROOT / "LICENSE",
    REPOSITORY_ROOT / "Makefile",
    REPOSITORY_ROOT / "README.md",
    REPOSITORY_ROOT / "config.example.json",
    REPOSITORY_ROOT / "pyproject.toml",
)
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def release_files():
    """Return the runtime files included in a Maya-module release."""
    package_files = (
        path
        for path in PACKAGE_ROOT.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix not in {".pyc", ".pyo"}
    )
    return sorted((*ROOT_FILES, *package_files), key=lambda path: path.as_posix())


def _archive_name(path, archive_root):
    return "{}/{}".format(archive_root, path.relative_to(REPOSITORY_ROOT).as_posix())


def build_archive(output_directory, expected_version=None):
    """Build and verify the versioned release ZIP plus SHA-256 sidecar."""
    version = validate_version(expected_version)
    output_path = Path(output_directory)
    output_path.mkdir(parents=True, exist_ok=True)
    archive_root = "{}-{}".format(PROJECT_NAME, version)
    archive_path = output_path / (archive_root + ".zip")

    with zipfile.ZipFile(archive_path, "w") as archive:
        for source_path in release_files():
            info = zipfile.ZipInfo(_archive_name(source_path, archive_root), ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, source_path.read_bytes(), compresslevel=9)

    with zipfile.ZipFile(archive_path) as archive:
        names = set(archive.namelist())
    required_names = {
        "{}/JAM.mod".format(archive_root),
        "{}/config.example.json".format(archive_root),
        "{}/src/jam_asset_manager/__init__.py".format(archive_root),
    }
    missing_names = required_names - names
    if missing_names:
        raise RuntimeError("Release archive is incomplete: {}".format(sorted(missing_names)))

    digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    checksum_path = archive_path.with_suffix(archive_path.suffix + ".sha256")
    checksum_path.write_text(
        "{}  {}\n".format(digest, archive_path.name),
        encoding="utf-8",
    )
    return archive_path, checksum_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="dist/release")
    parser.add_argument("--expected-version")
    arguments = parser.parse_args()
    archive_path, checksum_path = build_archive(
        arguments.output_dir,
        arguments.expected_version,
    )
    print(archive_path)
    print(checksum_path)


if __name__ == "__main__":
    main()
