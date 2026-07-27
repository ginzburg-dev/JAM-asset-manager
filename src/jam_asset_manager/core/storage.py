"""Small, reliable JSON persistence helpers."""

import json
import os
import time
from contextlib import contextmanager
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


@contextmanager
def exclusive_file_lock(path, timeout=5.0, poll_interval=0.05, stale_after=60.0):
    """Coordinate short cross-process updates using a portable lock file."""
    target_path = Path(path)
    lock_path = target_path.with_name(target_path.name + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + timeout

    while True:
        try:
            descriptor = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            try:
                lock_age = time.time() - lock_path.stat().st_mtime
            except FileNotFoundError:
                continue
            if lock_age > stale_after:
                try:
                    lock_path.unlink()
                except FileNotFoundError:
                    pass
                continue
            if time.monotonic() >= deadline:
                raise TimeoutError(
                    "Timed out waiting for JSON lock: {}".format(lock_path)
                ) from None
            time.sleep(poll_interval)
        else:
            with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
                stream.write(str(os.getpid()))
                stream.write("\n")
            break

    try:
        yield
    finally:
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass


def update_json(path, update, default=None):
    """Atomically apply a read-modify-write callback across local processes."""
    with exclusive_file_lock(path):
        data = read_json(path, default)
        updated_data = update(data)
        write_json(path, updated_data)
    return updated_data
