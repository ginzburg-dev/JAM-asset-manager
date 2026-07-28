# JAM Asset Manager

[![CI](https://github.com/ginzburg-dev/JAM-asset-manager/actions/workflows/ci.yml/badge.svg)](https://github.com/ginzburg-dev/JAM-asset-manager/actions/workflows/ci.yml)
[![Latest release](https://img.shields.io/github/v/release/ginzburg-dev/JAM-asset-manager)](https://github.com/ginzburg-dev/JAM-asset-manager/releases/latest)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)

JAM Asset Manager is a lightweight, extensible publishing pipeline for small
post-production studios working in Autodesk Maya. It keeps publishing consistent
for assets and scenes across multiple projects.

[Publishing](#publishing) · [Architecture](#architecture) ·
[Installation](#installation) ·
[Watch the showreel](https://www.youtube.com/watch?v=ntvdcg_zj6I&t=14s)

![JAM Asset Manager interface](https://github.com/ginzburg-dev/JAM-asset-manager/assets/143356357/d4c7b994-8b63-48b2-a076-0ef36a24aa3c)

## Features

- Publish versioned Maya scenes with JSON metadata.
- Track scene dependencies and flag missing files.
- Create and validate render scenes from shared templates.
- Browse and import project assets and animation shots.
- Add production notes and time reports.

## Requirements

- Autodesk Maya with Python 3
- PySide2 or PySide6
- RenderMan for Maya only for optional denoising

JAM runs inside Maya.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ginzburg-dev/JAM-asset-manager.git
   ```

2. Create and edit `config.json`:

   ```bash
   cd JAM-asset-manager
   make setup
   ```

3. Add the repository to `MAYA_MODULE_PATH` in `Maya.env`, then restart Maya:

   ```text
   MAYA_MODULE_PATH=/absolute/path/to/JAM-asset-manager
   ```

4. Run in Maya's Python Script Editor:

   ```python
   from jam_asset_manager import run

   jam_window = run()
   ```

## Configuration

`config.json` defines projects, asset folders, episode paths, and render
templates. Use [config.example.json](config.example.json) as a starting point.

Expected project layout:

```text
<project>/<episodePath>/<episode>/
├── maya/animation/<shot>.ma
└── render/<shot>/<shot>.ma
```

Paths can be absolute or relative to the repository. Asset previews use a JPEG
with the same name as the asset.

## Publishing

Each publish saves the Maya scene and updates its JSON sidecar, such as
`shot.ma.json`.

The sidecar stores:

- Version, author, and time
- Scene references and external files
- Missing dependencies and scan errors

Publishing is locked per scene, and metadata writes are atomic. Versions record
publish history.

## Architecture

- `core` — configuration, catalog, metadata, and storage
- `maya` — scene operations and dependency collection
- `ui` — PySide interface for Maya

The core has no Maya or Qt dependency and can be tested with standard Python.

## Development

```bash
python3 -m pip install -e ".[dev]"
make check
make build
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for development and release steps.
[CHANGELOG.md](CHANGELOG.md) lists changes, and [SECURITY.md](SECURITY.md)
explains how to report vulnerabilities.

## License

Licensed under the [Apache License 2.0](LICENSE).
