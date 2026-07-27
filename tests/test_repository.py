"""Regression tests that keep the source checkout lightweight and complete."""

import re
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
ICON_REFERENCE_PATTERN = re.compile(r'["\']([^/"\']+\.(?:png|jpe?g))["\']', re.IGNORECASE)
SIZE_BUDGET_BYTES = 2 * 1024 * 1024
EXCLUDED_DIRECTORIES = {
    ".git",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
}
REQUIRED_PACKAGE_DIRECTORIES = {"core", "maya", "resources", "ui"}


def is_source_file(path):
    relative_parts = path.relative_to(REPOSITORY_ROOT).parts
    return not EXCLUDED_DIRECTORIES.intersection(relative_parts) and not any(
        part.endswith(".egg-info") for part in relative_parts
    )


class RepositoryTestCase(unittest.TestCase):
    def test_repository_uses_a_conventional_source_layout(self):
        package_root = REPOSITORY_ROOT / "src" / "jam_asset_manager"
        module_file = REPOSITORY_ROOT / "JAM.mod"
        self.assertTrue((REPOSITORY_ROOT / "pyproject.toml").is_file())
        self.assertTrue((REPOSITORY_ROOT / "Makefile").is_file())
        self.assertTrue(module_file.is_file())
        self.assertTrue((REPOSITORY_ROOT / "config.example.json").is_file())
        module_definition = module_file.read_text(encoding="utf-8")
        self.assertIn("PYTHONPATH +:= src", module_definition)
        self.assertIn("JAM_ASSET_MANAGER_PATH:=.", module_definition)
        self.assertEqual(
            REQUIRED_PACKAGE_DIRECTORIES,
            {path.name for path in package_root.iterdir() if path.is_dir()} - {"__pycache__"},
        )

    def test_every_icon_is_referenced_and_every_reference_exists(self):
        reference_files = (
            REPOSITORY_ROOT / "src" / "jam_asset_manager" / "ui" / "main_window.py",
            REPOSITORY_ROOT / "config.example.json",
            REPOSITORY_ROOT / "src" / "jam_asset_manager" / "ui" / "forms" / "main_window.ui",
            REPOSITORY_ROOT / "src" / "jam_asset_manager" / "ui" / "forms" / "report_dialog.ui",
        )
        referenced_icons = set()
        for path in reference_files:
            referenced_icons.update(
                ICON_REFERENCE_PATTERN.findall(path.read_text(encoding="utf-8"))
            )

        icons_path = REPOSITORY_ROOT / "src" / "jam_asset_manager" / "resources" / "icons"
        available_icons = {path.name for path in icons_path.iterdir()}
        self.assertEqual(available_icons, referenced_icons)

    def test_working_source_stays_within_size_budget(self):
        source_files = (
            path for path in REPOSITORY_ROOT.rglob("*") if path.is_file() and is_source_file(path)
        )
        total_size = sum(path.stat().st_size for path in source_files)
        self.assertLess(
            total_size,
            SIZE_BUDGET_BYTES,
            "Source checkout exceeded the 2 MiB budget; keep production assets external.",
        )


if __name__ == "__main__":
    unittest.main()
