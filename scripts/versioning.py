"""Project and Maya module version helpers."""

import ast
import re
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
PYPROJECT_PATH = REPOSITORY_ROOT / "pyproject.toml"
MAYA_MODULE_PATH = REPOSITORY_ROOT / "JAM.mod"
SEMANTIC_VERSION = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")


def project_version(path=PYPROJECT_PATH):
    """Read the static project version without requiring a TOML dependency."""
    pyproject_path = Path(path)
    section = None
    for source_line in pyproject_path.read_text(encoding="utf-8").splitlines():
        line = source_line.strip()
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip()
            continue
        if section != "project" or not line.startswith("version"):
            continue
        key, separator, raw_value = line.partition("=")
        if separator and key.strip() == "version":
            version = ast.literal_eval(raw_value.strip())
            if isinstance(version, str):
                return version
    raise RuntimeError("Could not find [project].version in {}".format(pyproject_path))


def _module_definition(path):
    module_path = Path(path)
    source = module_path.read_text(encoding="utf-8")
    lines = source.splitlines()
    if not lines:
        raise RuntimeError("{} is empty".format(module_path))

    fields = lines[0].split()
    module_index = next(
        (index for index, field in enumerate(fields[1:], start=1) if ":" not in field),
        None,
    )
    if not fields or fields[0] != "+" or module_index is None or len(fields) <= module_index + 2:
        raise RuntimeError(
            "{} must begin with '+ [conditions] JAM <version> <path>'".format(module_path)
        )
    if fields[module_index] != "JAM":
        raise RuntimeError("Unexpected Maya module name: {}".format(fields[module_index]))
    return source, lines, fields, module_index


def module_version(path=MAYA_MODULE_PATH):
    """Read the version declared in the Maya module definition."""
    _, _, fields, module_index = _module_definition(path)
    return fields[module_index + 1]


def sync_module_version(pyproject_path=PYPROJECT_PATH, module_path=MAYA_MODULE_PATH):
    """Synchronize the required Maya module version from ``pyproject.toml``."""
    version = project_version(pyproject_path)
    source, lines, fields, module_index = _module_definition(module_path)
    fields[module_index + 1] = version
    lines[0] = " ".join(fields)
    updated_source = "\n".join(lines) + ("\n" if source.endswith("\n") else "")
    changed = updated_source != source
    if changed:
        Path(module_path).write_text(updated_source, encoding="utf-8")
    return version, changed


def validate_version(
    expected_version=None,
    pyproject_path=PYPROJECT_PATH,
    module_path=MAYA_MODULE_PATH,
):
    """Validate project, Maya-module, and optional tag versions."""
    version = project_version(pyproject_path)
    if not SEMANTIC_VERSION.fullmatch(version):
        raise RuntimeError("Invalid project version: {!r}".format(version))
    if module_version(module_path) != version:
        raise RuntimeError("JAM.mod version does not match project version {}".format(version))

    normalized_expected = (
        expected_version[1:]
        if expected_version and expected_version.startswith("v")
        else expected_version
    )
    if normalized_expected and normalized_expected != version:
        raise RuntimeError(
            "Release tag version {} does not match project version {}".format(
                normalized_expected,
                version,
            )
        )
    return version
