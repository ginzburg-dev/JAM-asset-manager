"""Shared sidecar metadata schema and persistence helpers."""

from contextlib import ExitStack
from copy import deepcopy
from pathlib import Path

from .constants import ASSET_METADATA_TEMPLATE, METADATA_SCHEMA_VERSION
from .storage import exclusive_file_lock, read_json, write_json


class MetadataError(ValueError):
    """Base class for sidecar schema and migration errors."""


class UnsupportedMetadataSchemaError(MetadataError):
    """Raised when a sidecar was written by a newer incompatible JAM version."""


class AmbiguousLegacyMetadataError(MetadataError):
    """Raised when an extension-less legacy sidecar cannot be assigned safely."""


def metadata_path(path):
    """Return an extension-preserving JSON sidecar path."""
    source_path = Path(path)
    return source_path.with_name(source_path.name + ".json")


def legacy_metadata_path(path):
    """Return the pre-schema-v2 sidecar path that replaced the source suffix."""
    return Path(path).with_suffix(".json")


def new_metadata():
    """Return an independent metadata document using the current schema."""
    return deepcopy(ASSET_METADATA_TEMPLATE)


def normalize_metadata(data):
    """Upgrade a metadata document in memory without discarding unknown fields."""
    if not isinstance(data, dict):
        raise MetadataError("Metadata root must be a JSON object.")
    normalized = dict(data)
    schema_version = normalized.get("schemaVersion", 1)
    if (
        not isinstance(schema_version, int)
        or isinstance(schema_version, bool)
        or schema_version < 1
    ):
        raise MetadataError("Invalid metadata schema version: {!r}".format(schema_version))
    if schema_version > METADATA_SCHEMA_VERSION:
        raise UnsupportedMetadataSchemaError(
            "Metadata schema version {} is newer than supported version {}.".format(
                schema_version,
                METADATA_SCHEMA_VERSION,
            )
        )

    defaults = new_metadata()

    for key in ("assetName", "assetType", "createdTime"):
        normalized.setdefault(key, defaults[key])
    if not isinstance(normalized.get("messages"), list):
        normalized["messages"] = []
    if not isinstance(normalized.get("publishes"), list):
        normalized["publishes"] = []

    versions = [
        publish.get("version")
        for publish in normalized["publishes"]
        if isinstance(publish, dict)
        and isinstance(publish.get("version"), int)
        and not isinstance(publish.get("version"), bool)
        and publish["version"] > 0
    ]
    latest_version = normalized.get("latestVersion", 0)
    if (
        not isinstance(latest_version, int)
        or isinstance(latest_version, bool)
        or latest_version < 0
    ):
        latest_version = 0
    normalized["latestVersion"] = max([latest_version] + versions)
    normalized["schemaVersion"] = METADATA_SCHEMA_VERSION
    return normalized


def _legacy_matches_source(data, path):
    source_type = Path(path).suffix.lower().lstrip(".")
    metadata_type = str(data.get("assetType", "")).lower().lstrip(".")
    return bool(source_type and metadata_type and source_type == metadata_type)


def _load_metadata_file(path):
    try:
        return read_json(path, default={})
    except (OSError, ValueError) as error:
        raise MetadataError("Could not read metadata {}: {}".format(path, error)) from error


def _read_path(path):
    current_path = metadata_path(path)
    if current_path.is_file():
        return current_path

    old_path = legacy_metadata_path(path)
    if old_path == current_path or not old_path.is_file():
        return current_path
    legacy_data = _load_metadata_file(old_path)
    if _legacy_matches_source(legacy_data, path):
        return old_path
    if legacy_data.get("assetType"):
        return current_path
    raise AmbiguousLegacyMetadataError(
        "Legacy metadata cannot be assigned safely to {}: {}".format(path, old_path)
    )


def read_metadata(path):
    """Read and normalize a sidecar without modifying it on disk."""
    return normalize_metadata(_load_metadata_file(_read_path(path)))


def update_metadata(path, update):
    """Update metadata atomically and migrate an unambiguous legacy sidecar."""
    current_path = metadata_path(path)
    old_path = legacy_metadata_path(path)
    lock_targets = sorted({current_path, old_path}, key=str)

    with ExitStack() as locks:
        for lock_target in lock_targets:
            locks.enter_context(exclusive_file_lock(lock_target))

        migrated_path = None
        if current_path.is_file():
            data = _load_metadata_file(current_path)
        elif old_path != current_path and old_path.is_file():
            legacy_data = _load_metadata_file(old_path)
            if _legacy_matches_source(legacy_data, path):
                data = legacy_data
                migrated_path = old_path
            elif legacy_data.get("assetType"):
                data = {}
            else:
                raise AmbiguousLegacyMetadataError(
                    "Legacy metadata cannot be assigned safely to {}: {}".format(path, old_path)
                )
        else:
            data = {}

        updated_data = normalize_metadata(update(normalize_metadata(data)))
        write_json(current_path, updated_data)
        if migrated_path is not None:
            try:
                migrated_path.unlink()
            except OSError:
                pass
        return updated_data
