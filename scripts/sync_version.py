#!/usr/bin/env python3
"""Synchronize the Maya module version with ``pyproject.toml``."""

from .versioning import sync_module_version


def main():
    version, changed = sync_module_version()
    action = "Updated" if changed else "Verified"
    print("{} JAM.mod version {}".format(action, version))


if __name__ == "__main__":
    main()
