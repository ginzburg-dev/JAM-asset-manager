"""Tests for atomic JSON storage."""

from unittest.mock import patch

from jam_asset_manager.core.storage import read_json, update_json, write_json
from tests.support import TemporaryProjectTestCase


class StorageTestCase(TemporaryProjectTestCase):
    def test_round_trip_is_formatted(self):
        path = self.root / "nested" / "data.json"
        write_json(path, {"name": "JAM"})
        self.assertEqual(read_json(path), {"name": "JAM"})
        self.assertTrue(path.read_text(encoding="utf-8").endswith("\n"))

    def test_missing_file_returns_requested_default(self):
        sentinel = object()
        self.assertIs(read_json(self.root / "missing.json", sentinel), sentinel)
        self.assertEqual(read_json(self.root / "missing.json"), {})

    def test_temporary_file_is_removed_when_replace_fails(self):
        path = self.root / "data.json"
        with patch(
            "jam_asset_manager.core.storage.os.replace",
            side_effect=OSError("disk error"),
        ):
            with self.assertRaisesRegex(OSError, "disk error"):
                write_json(path, {"name": "JAM"})
        self.assertFalse((self.root / "data.json.tmp").exists())

    def test_update_json_cleans_up_its_lock(self):
        path = self.root / "data.json"
        result = update_json(
            path,
            lambda data: {"count": data.get("count", 0) + 1},
            default={},
        )
        self.assertEqual(result, {"count": 1})
        self.assertEqual(read_json(path), {"count": 1})
        self.assertFalse((self.root / "data.json.lock").exists())
