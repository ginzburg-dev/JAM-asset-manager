"""Tests for versioned publish metadata."""

import threading
from datetime import datetime, timezone

from jam_asset_manager.core.metadata import (
    UnsupportedMetadataSchemaError,
    legacy_metadata_path,
    metadata_path,
    read_metadata,
)
from jam_asset_manager.core.publishing import (
    publish_lock,
    read_publishes,
    record_publish,
    render_publish_metadata,
)
from jam_asset_manager.core.storage import read_json, write_json
from tests.support import TemporaryProjectTestCase


class PublishingTestCase(TemporaryProjectTestCase):
    def test_publish_versions_increment_and_capture_source_and_dependencies(self):
        asset_path = self.root / "asset.ma"
        dependency_path = self.root / "texture.tx"
        asset_path.write_text("maya scene", encoding="utf-8")
        dependency_path.write_text("texture", encoding="utf-8")
        dependency = {
            "kind": "texture",
            "node": "diffuseFile",
            "path": "texture.tx",
            "resolvedPath": str(dependency_path),
            "exists": True,
            "size": dependency_path.stat().st_size,
            "fileCount": 1,
            "modifiedAt": "2026-07-28T10:00:00Z",
        }

        first = record_publish(
            asset_path,
            "asset",
            dependencies=[dependency],
            user="artist",
            now=datetime(2026, 7, 28, 10, 30, tzinfo=timezone.utc),
        )
        second = record_publish(
            asset_path,
            "asset",
            dependencies=[],
            user="artist",
            now=datetime(2026, 7, 28, 11, 0, tzinfo=timezone.utc),
        )

        self.assertEqual(first["versionLabel"], "v001")
        self.assertEqual(second["versionLabel"], "v002")
        self.assertTrue(first["source"]["exists"])
        self.assertEqual(first["dependencyStatus"], "complete")
        self.assertEqual(first["dependencies"][0]["node"], "diffuseFile")
        self.assertEqual(first["dependencies"][0]["fileCount"], 1)
        metadata = read_metadata(asset_path)
        self.assertEqual(metadata["schemaVersion"], 2)
        self.assertEqual(metadata["latestVersion"], 2)
        self.assertEqual(len(metadata["publishes"]), 2)

    def test_legacy_message_metadata_is_upgraded_without_data_loss(self):
        asset_path = self.root / "legacy.ma"
        legacy_message = {"type": "note", "message": "Keep me"}
        write_json(
            legacy_metadata_path(asset_path),
            {
                "assetName": "legacy",
                "assetType": "ma",
                "createdTime": "01/01/2020 10:00:00",
                "messages": [legacy_message],
            },
        )

        publish = record_publish(asset_path, "asset", user="artist")
        metadata = read_metadata(asset_path)

        self.assertEqual(publish["version"], 1)
        self.assertEqual(metadata["messages"], [legacy_message])
        self.assertEqual(metadata["createdTime"], "01/01/2020 10:00:00")
        self.assertEqual(metadata["latestVersion"], 1)
        self.assertTrue(metadata_path(asset_path).is_file())
        self.assertFalse(legacy_metadata_path(asset_path).exists())

    def test_source_extensions_use_independent_sidecars_and_version_sequences(self):
        ascii_path = self.root / "asset.ma"
        binary_path = self.root / "asset.mb"
        ascii_path.touch()
        binary_path.touch()
        legacy_message = {"type": "note", "message": "ASCII only"}
        write_json(
            legacy_metadata_path(ascii_path),
            {
                "assetName": "asset",
                "assetType": "ma",
                "createdTime": "01/01/2020 10:00:00",
                "messages": [legacy_message],
            },
        )

        binary_publish = record_publish(binary_path, "asset", user="artist")
        ascii_publish = record_publish(ascii_path, "asset", user="artist")

        self.assertEqual(binary_publish["versionLabel"], "v001")
        self.assertEqual(ascii_publish["versionLabel"], "v001")
        self.assertNotEqual(metadata_path(ascii_path), metadata_path(binary_path))
        self.assertEqual(read_metadata(ascii_path)["messages"], [legacy_message])
        self.assertEqual(read_metadata(binary_path)["messages"], [])

    def test_dependency_collection_errors_are_persisted_as_incomplete(self):
        asset_path = self.root / "asset.ma"
        publish = record_publish(
            asset_path,
            "asset",
            dependency_errors=["reference query failed"],
            user="artist",
        )

        self.assertEqual(publish["dependencyStatus"], "incomplete")
        self.assertEqual(publish["dependencyErrors"], ["reference query failed"])
        self.assertEqual(read_publishes(asset_path)[0], publish)

    def test_future_metadata_schema_is_rejected_without_rewriting_the_file(self):
        asset_path = self.root / "future.ma"
        future_metadata = {"schemaVersion": 999, "publishes": [], "messages": []}
        write_json(metadata_path(asset_path), future_metadata)

        with self.assertRaises(UnsupportedMetadataSchemaError):
            record_publish(asset_path, "asset", user="artist")

        self.assertEqual(
            read_json(metadata_path(asset_path)),
            future_metadata,
        )

    def test_concurrent_publishes_receive_unique_versions(self):
        asset_path = self.root / "asset.ma"
        asset_path.touch()
        threads = [
            threading.Thread(
                target=record_publish,
                args=(asset_path, "asset"),
                kwargs={"user": "artist"},
            )
            for _index in range(12)
        ]

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        versions = [publish["version"] for publish in read_publishes(asset_path)]
        self.assertEqual(sorted(versions), list(range(1, len(threads) + 1)))

    def test_publish_lock_rejects_a_second_transaction_for_the_same_source(self):
        asset_path = self.root / "asset.ma"
        with publish_lock(asset_path):
            with self.assertRaises(TimeoutError):
                with publish_lock(asset_path, timeout=0.01):
                    self.fail("The second transaction must not acquire the lock")

    def test_publish_renderer_escapes_paths_and_marks_missing_dependencies(self):
        rendered = render_publish_metadata(
            [
                {
                    "version": 1,
                    "versionLabel": "v001",
                    "kind": "asset",
                    "publishedAt": "today",
                    "publishedBy": "<artist>",
                    "dependencyStatus": "incomplete",
                    "dependencyErrors": ["<query failed>"],
                    "dependencies": [
                        {
                            "kind": "texture",
                            "resolvedPath": "<missing.tx>",
                            "exists": False,
                        }
                    ],
                }
            ]
        )

        self.assertIn("&lt;artist&gt;", rendered)
        self.assertIn("incomplete", rendered)
        self.assertIn("&lt;query failed&gt;", rendered)
        self.assertIn("&lt;missing.tx&gt; [missing]", rendered)
        self.assertNotIn("<artist>", rendered)
