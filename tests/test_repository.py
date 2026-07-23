"""Regression tests that keep the source checkout lightweight and complete."""

import re
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
ICON_REFERENCE_PATTERN = re.compile(r'["\']([^/"\']+\.(?:png|jpe?g))["\']', re.IGNORECASE)
SIZE_BUDGET_BYTES = 2 * 1024 * 1024
EXCLUDED_DIRECTORIES = {".git", ".ruff_cache", "__pycache__"}


class RepositoryTestCase(unittest.TestCase):
    def test_every_icon_is_referenced_and_every_reference_exists(self):
        reference_files = (
            REPOSITORY_ROOT / "jam_asset_manager.py",
            REPOSITORY_ROOT / "config.json",
            REPOSITORY_ROOT / "ui" / "jam.ui",
            REPOSITORY_ROOT / "ui" / "report.ui",
        )
        referenced_icons = set()
        for path in reference_files:
            referenced_icons.update(
                ICON_REFERENCE_PATTERN.findall(path.read_text(encoding="utf-8"))
            )

        available_icons = {path.name for path in (REPOSITORY_ROOT / "icons").iterdir()}
        self.assertEqual(available_icons, referenced_icons)

    def test_working_source_stays_within_size_budget(self):
        source_files = (
            path
            for path in REPOSITORY_ROOT.rglob("*")
            if path.is_file() and not EXCLUDED_DIRECTORIES.intersection(path.parts)
        )
        total_size = sum(path.stat().st_size for path in source_files)
        self.assertLess(
            total_size,
            SIZE_BUDGET_BYTES,
            "Source checkout exceeded the 2 MiB budget; keep production assets external.",
        )


if __name__ == "__main__":
    unittest.main()
