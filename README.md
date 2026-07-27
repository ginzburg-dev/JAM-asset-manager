# JAM Asset Manager

[![CI](https://github.com/ginzburg-dev/JAM-asset-manager/actions/workflows/ci.yml/badge.svg)](https://github.com/ginzburg-dev/JAM-asset-manager/actions/workflows/ci.yml)
[![Latest release](https://img.shields.io/github/v/release/ginzburg-dev/JAM-asset-manager)](https://github.com/ginzburg-dev/JAM-asset-manager/releases/latest)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)

JAM Asset Manager is a Maya-integrated browser for production assets and render
scenes. It provides one place to navigate project libraries, create or update
render scenes, import assets, validate scenes, publish work, and record production
notes.

[Watch the showreel](https://www.youtube.com/watch?v=ntvdcg_zj6I&t=14s)

![JAM Asset Manager interface](https://github.com/ginzburg-dev/JAM-asset-manager/assets/143356357/d4c7b994-8b63-48b2-a076-0ef36a24aa3c)

## Features

- Browse assets by project, type, and folder with optional JPEG previews.
- Browse animation shots and see whether their render scenes exist.
- Create render scenes from a project template and reference checked animation.
- Open, update, validate, and publish Maya scenes.
- Import supported assets into the current Maya scene.
- Attach notes and time reports to assets or shots as sidecar JSON metadata.
- Restore the last selected project, asset type, and episode per user.

## Requirements

- Autodesk Maya running Python 3
- PySide2/shiboken2 or PySide6/shiboken6, depending on the Maya version
- RenderMan for Maya only when using the optional `maya.denoising` adapter

The application is intended to run inside Maya; it is not a standalone Qt
program. The Qt adapter supports both Maya's Qt 5 and Qt 6 Python bindings.

## Installation

1. Clone or copy this repository to a stable location. For the smallest download,
   use a shallow clone:

   ```bash
   git clone --depth 1 https://github.com/ginzburg-dev/JAM-asset-manager.git
   ```

2. Prepare the local application configuration:

   ```bash
   make setup
   ```

   This safely creates `config.json` without replacing an existing file and
   prints the module path required by Maya. Update `config.json` with your
   project roots, asset folders, episode folder, and render-scene template paths.
3. Add the printed repository path to `MAYA_MODULE_PATH` in the `Maya.env` file
   for your Maya version, then restart Maya:

   ```text
   MAYA_MODULE_PATH=/absolute/path/to/JAM-asset-manager
   ```

   If `MAYA_MODULE_PATH` already contains other locations, add the repository
   instead of replacing the existing value. See Autodesk's documentation for
   [Maya.env](https://help.autodesk.com/view/MAYAUL/2023/ENU/?guid=GUID-8EFB1AC1-ED7D-4099-9EEE-624097872C04)
   and [module paths](https://help.autodesk.com/cloudhelp/2022/ENU/Maya-SDK/Distributing-Maya-Plug-ins/DistributingUsingModules/Maya-module-paths-folders-and.html).

   `JAM.mod` adds `src` to Maya's Python path and sets
   `JAM_ASSET_MANAGER_PATH` relative to the repository, so no hardcoded Python
   path is needed in shelf scripts.

4. Launch JAM from Maya's Python Script Editor:

```python
from jam_asset_manager import run

jam_window = run()
```

Keep the returned `jam_window` reference alive for the duration of the session.
`run()` creates `JamConfig` from the environment automatically.

As an alternative to Maya modules, install an editable Python package with:

```bash
make install MAYAPY=/absolute/path/to/mayapy
```

Runtime locations are controlled through environment variables:

| Variable | Purpose | Default |
| --- | --- | --- |
| `JAM_ASSET_MANAGER_PATH` | Root used for shared configuration and relative project paths | Repository root |
| `JAM_CONFIG_PATH` | Shared project configuration | `<root>/config.json` |
| `JAM_USER_CONFIG_PATH` | Local UI selection state | User configuration directory |
| `JAM_DENOISER_EXECUTABLE` | Site-specific legacy denoiser executable | `denoise` resolved from `PATH` |

The module file supplies `JAM_ASSET_MANAGER_PATH` for the standard installation.
Studio launchers can override it or set the more specific configuration paths
before Maya starts.

Configuration is represented by an explicit object and can be passed to the UI.
This is useful for studio launchers, tests, and future service adapters:

```python
from jam_asset_manager import JamConfig, run

config = JamConfig()
jam_window = run(config=config)
```

Explicit constructor values override environment defaults, which keeps launchers
and tests straightforward:

```python
config = JamConfig(
    asset_manager_path="/studio/jam",
    config_path="/studio/config/jam.json",
    user_config_path="/home/artist/.config/jam/config.user.json",
)
```

Each instance owns its loaded application settings and local selection state,
and provides `reload()` and `save()` methods.

## Configuration

`config.json` defines the shared production structure. The tracked
`config.example.json` is a safe template; the local `config.json` is intentionally
ignored:

| Field | Purpose |
| --- | --- |
| `projects[].projectName` | Display name shown in the project selector |
| `projects[].projectPath` | Absolute project root, or a path relative to this repository |
| `projects[].episodePath` | Episode directory relative to the project root |
| `projects[].rsScene` | Render-scene template path |
| `projects[].assets[]` | Display names and paths for browsable asset libraries |
| `allowedExtensions` | File extensions shown by the asset browser |
| `iconPlaceholder` | Fallback preview image from the `icons` directory |
| `iconSize` | Asset thumbnail size in pixels |

Environment variables and `~` are expanded in configured project and render
scene paths. `config.user.json` is generated automatically for local UI state and
should not be shared.

Production Maya scenes, HDR/EXR images, textures, and project libraries belong in
the external paths referenced by `config.json`; they are intentionally ignored by
Git. This keeps the source checkout small and prevents large binary assets from
being duplicated in repository history.

Expected shot layout:

```text
<project>/<episodePath>/<episode>/
├── maya/animation/<shot>.ma
└── render/<shot>/<shot>.ma
```

An asset preview is an adjacent JPEG with the same stem as the asset file.

## Architecture

The repository uses a conventional `src` layout and mirrors production modules
in the test suite:

```text
src/jam_asset_manager/
├── __init__.py              Public API: JamConfig and run()
├── application.py           Maya application entry point
├── core/                    Framework-independent domain services
│   ├── catalog.py           Asset, episode, and scene discovery
│   ├── config.py            Injectable configuration and validation
│   ├── constants.py         Environment names, paths, and defaults
│   ├── reports.py           Metadata and safe history rendering
│   └── storage.py           Atomic JSON persistence
├── maya/                    Autodesk Maya and RenderMan adapters
│   ├── assets.py
│   ├── scenes.py
│   └── denoising.py
├── resources/icons/         Runtime image assets
└── ui/
    ├── main_window.py       Qt event handlers and presentation logic
    ├── qt.py                PySide2/PySide6 compatibility imports
    ├── report_dialog.py
    ├── forms/               Editable Qt Designer sources
    └── generated/           Generated Qt form modules
tests/                       Unit tests mirroring source modules
```

`jam_asset_manager.core` has no Maya or Qt dependency, so its behavior can be
tested in a standard Python interpreter. A FastAPI service is intentionally not
included: the current application is local to Maya and has no defined remote
client or authentication boundary. The core package is suitable for reuse by an
API later if a concrete network workflow is required.

## Development

The Qt classes under `src/jam_asset_manager/ui/generated/` are generated from the
corresponding files under `src/jam_asset_manager/ui/forms/`. Edit the `.ui`
sources and run `make ui`; the generation script normalizes binding-specific
imports through the Qt compatibility module.

Install the development tools into an isolated environment with
`python3 -m pip install -e ".[dev]"`.

Run the local quality checks from the repository root:

```bash
make check
make build
make release
```

The test suite uses Python's standard `unittest` framework. Maya, PySide, and
RenderMan are replaced by controlled test doubles, so configuration, filesystem,
publishing, scene-management, denoising, and UI dependency-injection behavior can
be verified outside Maya and in CI.

The community edition exposes placeholders for commercial statistics features.
The denoising module is retained for compatible legacy RenderMan pipelines and
may require site-specific commands and executable paths.

## Releases

CI runs the test suite against Python versions representing supported Maya
generations, then checks formatting and packaging. A tag such as `v0.1.0`
automatically creates a GitHub Release containing a compact, versioned Maya-module
ZIP and its SHA-256 checksum.

Before tagging, update the matching version in
`src/jam_asset_manager/__init__.py` and `JAM.mod`, then run:

```bash
make check
make build
make release
git tag -a v0.1.0 -m "JAM Asset Manager 0.1.0"
git push origin v0.1.0
```

The workflow rejects tags that do not match the package and Maya-module versions.
Release notes are generated from merged pull requests and their labels.

See [CONTRIBUTING.md](CONTRIBUTING.md) for development conventions and
[SECURITY.md](SECURITY.md) for private vulnerability reporting.

## License

Licensed under the [Apache License 2.0](LICENSE).
