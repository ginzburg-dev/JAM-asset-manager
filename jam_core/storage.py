"""Small, reliable JSON persistence helpers."""

import json
import os
from pathlib import Path


def read_json(path, default=None):
    """Read JSON from *path*, returning *default* when the file is absent."""
    json_path = Path(path)
    if not json_path.is_file():
        return {} if default is None else default
    with json_path.open(encoding="utf-8") as stream:
        return json.load(stream)


def write_json(path, data):
    """Atomically write JSON so an interrupted save cannot corrupt existing data."""
    json_path = Path(path)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = json_path.with_name(json_path.name + ".tmp")
    try:
        with temporary_path.open("w", encoding="utf-8") as stream:
            json.dump(data, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(str(temporary_path), str(json_path))
    finally:
        if temporary_path.exists():
            temporary_path.unlink()
