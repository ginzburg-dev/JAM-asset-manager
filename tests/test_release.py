"""Tests for reproducible release and UI generation tooling."""

import hashlib
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.build_release import build_archive
from scripts.generate_ui import normalize_generated_source
from scripts.versioning import project_version, sync_module_version, validate_version

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent


class ReleaseToolingTestCase(unittest.TestCase):
    def test_project_version_comes_from_pyproject(self):
        pyproject = (REPOSITORY_ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('version = "{}"'.format(project_version()), pyproject)

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

    def test_maya_module_version_is_synchronized_from_pyproject(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pyproject_path = root / "pyproject.toml"
            module_path = root / "JAM.mod"
            pyproject_path.write_text(
                '[project]\nname = "example"\nversion = "1.2.3"\n',
                encoding="utf-8",
            )
            module_path.write_text(
                "+ JAM 0.0.0 .\nPYTHONPATH +:= src\n",
                encoding="utf-8",
            )

            version, changed = sync_module_version(pyproject_path, module_path)

            self.assertEqual(version, "1.2.3")
            self.assertTrue(changed)
            self.assertEqual(
                module_path.read_text(encoding="utf-8"),
                "+ JAM 1.2.3 .\nPYTHONPATH +:= src\n",
            )

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
