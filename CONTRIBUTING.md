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
```

Use a short, imperative commit subject such as `Prevent render scene overwrite`.
Keep unrelated changes in separate commits.

## Releases

Maintainers publish releases by merging a release pull request into `main`.
Before merging, move the relevant entries from `Unreleased` into a dated section
in `CHANGELOG.md` and update the version in both `[project].version` in
`pyproject.toml` and the first line of `JAM.mod`. `make sync-version` can update
the latter after the project version changes.

CI rejects mismatched versions. After CI succeeds on `main`, the release workflow
creates the matching `vX.Y.Z` tag and GitHub Release. If that version already
exists, the workflow leaves its tag and release unchanged. Contributors should
not change either version unless the pull request is intended to publish a
release.
