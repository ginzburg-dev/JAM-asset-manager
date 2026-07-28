"""Tests for report metadata and safe HTML rendering."""

import threading
from datetime import datetime

from jam_asset_manager.core.reports import (
    append_message,
    metadata_path,
    new_metadata,
    read_messages,
    render_history,
)
from tests.support import TemporaryProjectTestCase


class ReportsTestCase(TemporaryProjectTestCase):
    def test_hours_are_preserved_and_html_is_escaped(self):
        asset_path = self.root / "asset.ma"
        append_message(
            asset_path,
            "asset",
            "report",
            "<b>created</b>",
            hours=2,
            user="artist",
            now=datetime(2026, 7, 23, 12, 30),
        )
        messages = read_messages(asset_path)
        self.assertEqual(messages[0]["hours"], 2)
        self.assertEqual(messages[0]["createdTime"], "23/07/2026 12:30:00")
        rendered = render_history(messages)
        self.assertIn("&lt;b&gt;created&lt;/b&gt;", rendered)
        self.assertNotIn("<b>created</b>", rendered)

    def test_initial_created_time_is_preserved_across_messages(self):
        asset_path = self.root / "asset.ma"
        first_time = datetime(2026, 7, 23, 10, 0)
        second_time = datetime(2026, 7, 24, 11, 30)
        append_message(asset_path, "asset", "note", "First", now=first_time)
        data = append_message(asset_path, "asset", "report", "Second", now=second_time)
        self.assertEqual(data["createdTime"], "23/07/2026 10:00:00")
        self.assertEqual(data["assetType"], "ma")
        self.assertEqual(data["schemaVersion"], 2)
        self.assertEqual(data["publishes"], [])
        self.assertEqual(len(data["messages"]), 2)
        self.assertEqual(metadata_path(asset_path), self.root / "asset.ma.json")

    def test_renderer_ignores_unknown_types_and_escapes_byline(self):
        messages = [
            {"type": "unknown", "message": "hidden"},
            {
                "type": "note",
                "createdTime": "today",
                "user": "<artist>",
                "message": "line one\nline two",
                "hours": 99,
            },
        ]
        rendered = render_history(messages)
        self.assertNotIn("hidden", rendered)
        self.assertIn("&lt;artist&gt;", rendered)
        self.assertIn("line one<br>line two", rendered)
        self.assertNotIn("99h", rendered)
        self.assertEqual(new_metadata()["messages"], [])

    def test_concurrent_messages_are_not_lost(self):
        asset_path = self.root / "asset.ma"
        threads = [
            threading.Thread(
                target=append_message,
                args=(asset_path, "asset", "note", "message {}".format(index)),
                kwargs={"user": "artist"},
            )
            for index in range(12)
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        messages = read_messages(asset_path)
        self.assertEqual(len(messages), len(threads))
        self.assertEqual(
            {message["message"] for message in messages},
            {"message {}".format(index) for index in range(len(threads))},
        )
