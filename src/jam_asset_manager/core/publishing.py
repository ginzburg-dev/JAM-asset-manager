"""Versioned publish records stored in asset and scene sidecar metadata."""

import getpass
import html
import os
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from .metadata import read_metadata, update_metadata
from .storage import exclusive_file_lock


def _utc_timestamp(value=None):
    timestamp = value or datetime.now(timezone.utc)
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    timestamp = timestamp.astimezone(timezone.utc)
    return timestamp.isoformat(timespec="seconds").replace("+00:00", "Z")


def _absolute_path(path):
    expanded = os.path.expandvars(os.path.expanduser(os.fspath(path)))
    return os.path.normpath(os.path.abspath(expanded))


def _text(value, default=""):
    return default if value is None else str(value).strip()


def _file_snapshot(path):
    snapshot = {"path": _absolute_path(path), "exists": False}
    try:
        file_stat = os.stat(snapshot["path"])
    except OSError:
        return snapshot

    snapshot.update(
        {
            "exists": True,
            "size": file_stat.st_size,
            "modifiedAt": _utc_timestamp(datetime.fromtimestamp(file_stat.st_mtime, timezone.utc)),
        }
    )
    return snapshot


def _normalize_dependencies(dependencies):
    normalized = []
    for dependency in dependencies or ():
        if not isinstance(dependency, dict):
            continue
        path = _text(dependency.get("path"))
        resolved_path = _text(dependency.get("resolvedPath"), path)
        if not path and not resolved_path:
            continue

        item = {
            "kind": _text(dependency.get("kind"), "file") or "file",
            "path": path or resolved_path,
            "resolvedPath": resolved_path or path,
            "exists": bool(dependency.get("exists", False)),
        }
        node = _text(dependency.get("node"))
        if node:
            item["node"] = node
        size = dependency.get("size")
        if isinstance(size, int) and not isinstance(size, bool) and size >= 0:
            item["size"] = size
        file_count = dependency.get("fileCount")
        if isinstance(file_count, int) and not isinstance(file_count, bool) and file_count >= 0:
            item["fileCount"] = file_count
        modified_at = _text(dependency.get("modifiedAt"))
        if modified_at:
            item["modifiedAt"] = modified_at
        normalized.append(item)

    normalized.sort(
        key=lambda item: (
            item["kind"].casefold(),
            item["resolvedPath"].casefold(),
            item.get("node", "").casefold(),
        )
    )
    return normalized


def _normalize_errors(errors):
    if isinstance(errors, str):
        errors = [errors]
    return [str(error).strip() for error in errors or () if str(error).strip()]


@contextmanager
def publish_lock(path, timeout=5.0):
    """Serialize the full publish transaction for one source file."""
    source_path = Path(path)
    lock_target = source_path.with_name(source_path.name + ".publish")
    with exclusive_file_lock(lock_target, timeout=timeout, stale_after=3600.0):
        yield


def record_publish(
    path,
    publish_kind,
    dependencies=None,
    dependency_errors=None,
    user=None,
    now=None,
):
    """Append a uniquely versioned publish event and return the new record."""
    published_at = _utc_timestamp(now)
    published_by = user or getpass.getuser()
    source = _file_snapshot(path)
    dependency_snapshot = _normalize_dependencies(dependencies)
    collection_errors = _normalize_errors(dependency_errors)
    new_publish = {}

    def add_publish(data):
        versions = [
            publish.get("version")
            for publish in data["publishes"]
            if isinstance(publish, dict)
            and isinstance(publish.get("version"), int)
            and not isinstance(publish.get("version"), bool)
            and publish["version"] > 0
        ]
        next_version = max([data["latestVersion"]] + versions) + 1
        publish = {
            "version": next_version,
            "versionLabel": "v{:03d}".format(next_version),
            "kind": str(publish_kind),
            "publishedAt": published_at,
            "publishedBy": published_by,
            "source": source,
            "dependencies": dependency_snapshot,
            "dependencyStatus": "incomplete" if collection_errors else "complete",
        }
        if collection_errors:
            publish["dependencyErrors"] = collection_errors
        data["assetName"] = data.get("assetName") or Path(path).stem
        data["assetType"] = data.get("assetType") or Path(path).suffix.lower().lstrip(".")
        data["createdTime"] = data.get("createdTime") or published_at
        data["latestVersion"] = next_version
        data["publishes"].append(publish)
        new_publish.update(publish)
        return data

    update_metadata(path, add_publish)
    return new_publish


def read_publishes(path):
    """Return versioned publish records from an asset or scene sidecar."""
    return read_metadata(path)["publishes"]


def render_publish_metadata(publishes):
    """Render the latest publish and its dependencies for the Qt metadata pane."""
    valid_publishes = [
        publish
        for publish in publishes
        if isinstance(publish, dict)
        and isinstance(publish.get("version"), int)
        and not isinstance(publish.get("version"), bool)
        and publish["version"] > 0
    ]
    if not valid_publishes:
        return "<p><b>Publish metadata</b><br>No versions recorded.</p>"

    latest = max(valid_publishes, key=lambda publish: publish["version"])
    dependencies = [
        dependency for dependency in latest.get("dependencies", ()) if isinstance(dependency, dict)
    ]
    dependency_status = str(latest.get("dependencyStatus", "unknown"))
    dependency_errors = [
        str(error) for error in latest.get("dependencyErrors", ()) if str(error).strip()
    ]
    missing_count = sum(not dependency.get("exists", False) for dependency in dependencies)
    rows = [
        "<p><b>Latest publish:</b> {label}<br>"
        "<b>Type:</b> {kind}<br>"
        "<b>Published:</b> {published_at}<br>"
        "<b>By:</b> {published_by}<br>"
        "<b>Versions:</b> {version_count}<br>"
        "<b>Dependencies:</b> {dependency_count} ({missing_count} missing)<br>"
        "<b>Dependency scan:</b> {dependency_status}</p>".format(
            label=html.escape(str(latest.get("versionLabel", ""))),
            kind=html.escape(str(latest.get("kind", ""))),
            published_at=html.escape(str(latest.get("publishedAt", ""))),
            published_by=html.escape(str(latest.get("publishedBy", ""))),
            version_count=len(valid_publishes),
            dependency_count=len(dependencies),
            missing_count=missing_count,
            dependency_status=html.escape(dependency_status),
        )
    ]
    if dependency_errors:
        rows.append("<p><b>Collection errors:</b></p><ul>")
        rows.extend("<li>{}</li>".format(html.escape(error)) for error in dependency_errors)
        rows.append("</ul>")
    if dependencies:
        rows.append("<ul>")
        for dependency in dependencies:
            label = "{}: {}".format(
                dependency.get("kind", "file"),
                dependency.get("resolvedPath") or dependency.get("path", ""),
            )
            if not dependency.get("exists", False):
                label += " [missing]"
            rows.append("<li>{}</li>".format(html.escape(label)))
        rows.append("</ul>")
    return "".join(rows)
