# Contributing

Thank you for improving JAM Asset Manager.

## Development setup

JAM's core and test suite run in a standard Python environment. Maya, Qt, and
RenderMan integrations are replaced with test doubles during automated tests.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --editable ".[dev]"
make check
```

On Windows, activate the environment with `.venv\Scripts\activate`.

## Changes

- Keep Maya-specific calls in `src/jam_asset_manager/maya/`.
- Keep reusable filesystem and configuration logic in
  `src/jam_asset_manager/core/`.
- Add regression tests for behavior changes.
- Edit Qt Designer files under `src/jam_asset_manager/ui/forms/`, then run
  `make ui` with a PySide UI compiler available.
- Do not commit production scenes, textures, local configuration, generated
  caches, or credentials.

Before opening a pull request, run:

```bash
make check
make build
make release
```

Use a short, imperative commit subject such as `Prevent render scene overwrite`.
Keep unrelated changes in separate commits.

## Releases

Maintainers create releases from semantic-version tags. Before tagging, move the
relevant entries from `Unreleased` into a dated section in `CHANGELOG.md`. The
version in `src/jam_asset_manager/__init__.py` and `JAM.mod` must match the tag
without its leading `v`. Pushing the tag starts the release workflow;
contributors should not change the version unless the change is intended for a
release.
