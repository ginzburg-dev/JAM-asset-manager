"""Collect file dependencies from the current Maya scene."""

import glob
import logging
import os
import re
from datetime import datetime, timezone
from typing import NamedTuple

import maya.cmds as cmds

LOGGER = logging.getLogger(__name__)

NODE_PATH_ATTRIBUTES = (
    ("file", ("computedFileTextureNamePattern", "fileTextureName"), "texture"),
    ("aiImage", ("filename",), "texture"),
    ("PxrTexture", ("filename",), "texture"),
    ("AlembicNode", ("abc_File",), "cache"),
    ("gpuCache", ("cacheFileName",), "cache"),
    ("audio", ("filename",), "audio"),
    ("imagePlane", ("imageName",), "image"),
)
FILE_PATTERN_TOKEN = re.compile(
    r"<(?:UDIM|UVTILE|u|v|f|frame)>|#+|%0?\d*d|\$F\d*",
    re.IGNORECASE,
)


class DependencyCollection(NamedTuple):
    """A dependency snapshot plus any non-fatal collection errors."""

    dependencies: tuple
    errors: tuple


def _values(value):
    if isinstance(value, (list, tuple)):
        return value
    if isinstance(value, str):
        return [value]
    return []


def _utc_timestamp(timestamp):
    return (
        datetime.fromtimestamp(timestamp, timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )


def _resolve_path(path, scene_path):
    expanded = os.path.expandvars(os.path.expanduser(path))
    error = ""
    try:
        workspace_path = cmds.workspace(expandName=expanded)
    except Exception as workspace_error:
        workspace_path = ""
        error = "Could not expand dependency path {!r}: {}".format(path, workspace_error)
    if isinstance(workspace_path, str) and workspace_path:
        expanded = workspace_path
    elif not os.path.isabs(expanded) and scene_path:
        expanded = os.path.join(os.path.dirname(scene_path), expanded)
    return os.path.normpath(os.path.abspath(expanded)), error


def _glob_pattern(path):
    if not FILE_PATTERN_TOKEN.search(path):
        return ""
    placeholder = "__JAM_FILE_TOKEN__"
    tokenized = FILE_PATTERN_TOKEN.sub(placeholder, path)
    return glob.escape(tokenized).replace(placeholder, "*")


def _matching_files(path):
    pattern = _glob_pattern(path)
    if not pattern:
        return [path] if os.path.isfile(path) else [], ""
    try:
        matches = sorted(
            candidate for candidate in glob.iglob(pattern) if os.path.isfile(candidate)
        )
    except OSError as error:
        return [], "Could not expand dependency pattern {!r}: {}".format(path, error)
    return matches, ""


def _dependency(kind, path, scene_path, node=""):
    raw_path = str(path).strip()
    resolved_path, resolution_error = _resolve_path(raw_path, scene_path)
    dependency = {
        "kind": kind,
        "path": raw_path,
        "resolvedPath": resolved_path,
        "exists": False,
    }
    if node:
        dependency["node"] = str(node)

    matching_files, pattern_error = _matching_files(resolved_path)
    file_stats = []
    for matching_file in matching_files:
        try:
            file_stats.append(os.stat(matching_file))
        except OSError as error:
            pattern_error = "Could not inspect dependency {!r}: {}".format(
                matching_file,
                error,
            )
    if not file_stats:
        return dependency, resolution_error or pattern_error

    dependency.update(
        {
            "exists": True,
            "size": sum(file_stat.st_size for file_stat in file_stats),
            "modifiedAt": _utc_timestamp(max(file_stat.st_mtime for file_stat in file_stats)),
        }
    )
    if _glob_pattern(resolved_path):
        dependency["fileCount"] = len(file_stats)
    return dependency, resolution_error or pattern_error


def _reference_node(path):
    try:
        node = cmds.referenceQuery(path, referenceNode=True)
    except Exception:
        return ""
    return node if isinstance(node, str) else ""


def collect_dependencies(scene_path=None):
    """Return a deterministic snapshot of Maya references and external files."""
    dependencies = []
    errors = []
    try:
        references = _values(cmds.file(query=True, reference=True, withoutCopyNumber=True) or [])
    except Exception as error:
        LOGGER.exception("Maya could not list scene references")
        errors.append("Could not list scene references: {}".format(error))
        references = []

    for reference in references:
        if reference:
            dependency, error = _dependency(
                "reference",
                reference,
                scene_path,
                node=_reference_node(reference),
            )
            dependencies.append(dependency)
            if error:
                errors.append(error)

    for node_type, attributes, kind in NODE_PATH_ATTRIBUTES:
        try:
            nodes = _values(cmds.ls(type=node_type) or [])
        except Exception as error:
            LOGGER.exception("Maya could not list %s dependency nodes", node_type)
            errors.append("Could not list {} dependency nodes: {}".format(node_type, error))
            continue
        for node in nodes:
            path = ""
            attribute_errors = []
            for attribute in attributes:
                try:
                    candidate = cmds.getAttr("{}.{}".format(node, attribute))
                except Exception as error:
                    attribute_errors.append(str(error))
                    continue
                if isinstance(candidate, str) and candidate.strip():
                    path = candidate
                    break
            if not path and attribute_errors:
                LOGGER.error("Maya could not read dependency path from %s", node)
                errors.append(
                    "Could not read dependency path from {}: {}".format(
                        node,
                        "; ".join(attribute_errors),
                    )
                )
                continue
            if isinstance(path, str) and path.strip():
                dependency, error = _dependency(kind, path, scene_path, node=node)
                dependencies.append(dependency)
                if error:
                    errors.append(error)

    unique_dependencies = {
        (
            dependency["kind"],
            dependency.get("node", ""),
            dependency["resolvedPath"],
        ): dependency
        for dependency in dependencies
    }
    sorted_dependencies = sorted(
        unique_dependencies.values(),
        key=lambda item: (
            item["kind"].casefold(),
            item["resolvedPath"].casefold(),
            item.get("node", "").casefold(),
        ),
    )
    return DependencyCollection(
        dependencies=tuple(sorted_dependencies),
        errors=tuple(dict.fromkeys(errors)),
    )
