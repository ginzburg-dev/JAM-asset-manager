"""Tests for reproducible release and UI generation tooling."""

import hashlib
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.build_release import build_archive, project_version, validate_version
from scripts.generate_ui import normalize_generated_source

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent


class ReleaseToolingTestCase(unittest.TestCase):
    def test_release_archive_contains_only_versioned_runtime_content(self):
        with tempfile.TemporaryDirectory() as directory:
            archive_path, checksum_path = build_archive(directory, "v" + project_version())
            with zipfile.ZipFile(archive_path) as archive:
                names = archive.namelist()

            prefix = "JAM-asset-manager-{}/".format(project_version())
            self.assertTrue(all(name.startswith(prefix) for name in names))
            self.assertIn(prefix + "CHANGELOG.md", names)
            self.assertIn(prefix + "JAM.mod", names)
            self.assertIn(prefix + "Makefile", names)
            self.assertIn(prefix + "config.example.json", names)
            self.assertIn(prefix + "pyproject.toml", names)
            self.assertIn(prefix + "src/jam_asset_manager/resources/icons/check.png", names)
            self.assertFalse(any("/tests/" in name for name in names))
            self.assertFalse(any("__pycache__" in name for name in names))

            expected_digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
            self.assertEqual(
                checksum_path.read_text(encoding="utf-8"),
                "{}  {}\n".format(expected_digest, archive_path.name),
            )

    def test_release_rejects_a_mismatched_tag(self):
        with self.assertRaisesRegex(RuntimeError, "does not match"):
            validate_version("v9.9.9")

    def test_release_title_matches_the_version_tag(self):
        workflow = (REPOSITORY_ROOT / ".github" / "workflows" / "release.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn('--title "${GITHUB_REF_NAME}"', workflow)

    def test_generated_ui_imports_are_normalized(self):
        source = """from PySide6.QtCore import (Qt, QSize)
from PySide6.QtWidgets import (QSizePolicy, QWidget)

class Ui_Form(object):
    policy = QSizePolicy.Policy.Fixed
"""
        normalized = normalize_generated_source(source)
        self.assertNotIn("from PySide6", normalized)
        self.assertIn("from ..qt import (", normalized)
        self.assertIn("QSizePolicyPolicy.Fixed", normalized)


if __name__ == "__main__":
    unittest.main()
