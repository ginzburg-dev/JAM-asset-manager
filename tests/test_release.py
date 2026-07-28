"""Tests for release metadata and UI generation tooling."""

import tempfile
import unittest
from pathlib import Path

from scripts.generate_ui import normalize_generated_source
from scripts.versioning import (
    module_version,
    project_version,
    sync_module_version,
    validate_version,
)

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent


class ReleaseToolingTestCase(unittest.TestCase):
    def test_project_version_comes_from_pyproject(self):
        pyproject = (REPOSITORY_ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('version = "{}"'.format(project_version()), pyproject)

    def test_repository_versions_match(self):
        self.assertEqual(project_version(), module_version())
        self.assertEqual(validate_version(), project_version())

    def test_release_rejects_a_mismatched_tag(self):
        with self.assertRaisesRegex(RuntimeError, "does not match"):
            validate_version("v9.9.9")

    def test_release_rejects_mismatched_project_and_module_versions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pyproject_path = root / "pyproject.toml"
            module_path = root / "JAM.mod"
            pyproject_path.write_text(
                '[project]\nname = "example"\nversion = "1.2.3"\n',
                encoding="utf-8",
            )
            module_path.write_text("+ JAM 1.2.4 .\n", encoding="utf-8")

            with self.assertRaisesRegex(RuntimeError, "JAM.mod version does not match"):
                validate_version(
                    pyproject_path=pyproject_path,
                    module_path=module_path,
                )

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

    def test_release_runs_after_successful_main_ci(self):
        workflow = (REPOSITORY_ROOT / ".github" / "workflows" / "release.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("workflow_run:", workflow)
        self.assertIn("github.event.workflow_run.conclusion == 'success'", workflow)
        self.assertIn("github.event.workflow_run.head_sha", workflow)

    def test_release_uses_matching_metadata_and_version_tag(self):
        workflow = (REPOSITORY_ROOT / ".github" / "workflows" / "release.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("python -m scripts.versioning", workflow)
        self.assertIn('git push origin "${TAG}"', workflow)
        self.assertIn('gh release create "${TAG}"', workflow)
        self.assertIn('--title "${TAG}"', workflow)

    def test_ci_does_not_build_a_custom_release_archive(self):
        workflow = (REPOSITORY_ROOT / ".github" / "workflows" / "ci.yml").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("make release", workflow)

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
