#!/usr/bin/env python3
"""Generate Qt forms and normalize them to the local compatibility module."""

import argparse
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
FORM_DIRECTORY = REPOSITORY_ROOT / "src" / "jam_asset_manager" / "ui" / "forms"
OUTPUT_DIRECTORY = REPOSITORY_ROOT / "src" / "jam_asset_manager" / "ui" / "generated"
FORMS = {
    "main_window.ui": "main_window.py",
    "report_dialog.ui": "report_dialog.py",
}
PYSIDE_IMPORT = re.compile(
    r"^from PySide[26]\.Qt(?:Core|Gui|Widgets) import "
    r"(?P<body>\([^)]*\)|[^\n]+)\n",
    re.MULTILINE,
)


def normalize_generated_source(source):
    """Replace binding-specific imports with the project's Qt adapter."""
    imported_names = set()
    for match in PYSIDE_IMPORT.finditer(source):
        body = match.group("body").strip().strip("()")
        imported_names.update(name.strip() for name in body.replace("\n", " ").split(","))
    if not imported_names:
        raise RuntimeError("Generated UI did not contain recognizable PySide imports")

    source = PYSIDE_IMPORT.sub("", source)
    if "QSizePolicy.Policy." in source:
        source = source.replace("QSizePolicy.Policy.", "QSizePolicyPolicy.")
        imported_names.add("QSizePolicyPolicy")

    names = sorted(name for name in imported_names if name)
    import_lines = ["from ..qt import ("]
    current_line = "    "
    for name in names:
        item = name + ", "
        if len(current_line) + len(item) > 96:
            import_lines.append(current_line.rstrip())
            current_line = "    "
        current_line += item
    import_lines.append(current_line.rstrip())
    import_lines.append(")")
    import_block = "\n".join(import_lines)

    class_marker = "\nclass "
    if class_marker not in source:
        raise RuntimeError("Generated UI did not contain a class definition")
    return source.replace(class_marker, "\n{}\n\nclass ".format(import_block), 1)


def find_uic(explicit_path=None):
    if explicit_path:
        executable = shutil.which(explicit_path) or explicit_path
        if not Path(executable).is_file():
            raise RuntimeError("Qt UI compiler was not found: {}".format(explicit_path))
        return executable
    for candidate in ("pyside6-uic", "pyside2-uic", "uic"):
        executable = shutil.which(candidate)
        if executable:
            return executable
    raise RuntimeError("Install PySide or pass the Qt UI compiler with --uic")


def generate_forms(uic_path=None):
    """Generate every tracked form with the available Qt UI compiler."""
    executable = find_uic(uic_path)
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temporary_directory:
        temporary_root = Path(temporary_directory)
        for form_name, output_name in FORMS.items():
            generated_path = temporary_root / output_name
            command = [executable]
            if Path(executable).name.lower() in {"uic", "uic.exe"}:
                command.extend(["-g", "python"])
            command.extend([str(FORM_DIRECTORY / form_name), "-o", str(generated_path)])
            subprocess.run(command, check=True)
            normalized = normalize_generated_source(generated_path.read_text(encoding="utf-8"))
            (OUTPUT_DIRECTORY / output_name).write_text(normalized, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--uic", help="Path or executable name for pyside-uic/uic")
    arguments = parser.parse_args()
    generate_forms(arguments.uic)


if __name__ == "__main__":
    main()
