# JAM Asset Manager

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
- PySide2 and shiboken2 (included with supported Maya installations)
- RenderMan for Maya only when using the legacy helpers in `jam_denoise.py`

The application is intended to run inside Maya; it is not a standalone Qt
program.

## Installation

1. Clone or copy this repository to a stable location. For the smallest download,
   use a shallow clone:

   ```bash
   git clone --depth 1 https://github.com/ginzburg-dev/JAM-asset-manager.git
   ```

2. Update `config.json` with your project roots, asset folders, episode folder,
   and render-scene template paths.
3. Run the following from Maya's Python Script Editor, replacing the path with
   the repository location:

```python
import sys

jam_path = r"/absolute/path/to/JAM-asset-manager"
if jam_path not in sys.path:
    sys.path.insert(0, jam_path)

from jam_asset_manager import jam_asset_manager_run

jam_window = jam_asset_manager_run()
```

Keep the returned `jam_window` reference alive for the duration of the session.

Runtime locations are controlled through environment variables:

| Variable | Purpose | Default |
| --- | --- | --- |
| `JAM_ASSET_MANAGER_PATH` | Root containing shared configuration and icons | Repository root |
| `JAM_CONFIG_PATH` | Shared project configuration | `<root>/config.json` |
| `JAM_USER_CONFIG_PATH` | Local UI selection state | User configuration directory |
| `JAM_DENOISER_EXECUTABLE` | Site-specific legacy denoiser executable | Built-in pipeline path |

The explicit configuration variables take precedence over
`JAM_ASSET_MANAGER_PATH`. Set them before importing JAM in Maya.

Configuration is represented by an explicit object and can be passed to the UI.
This is useful for studio launchers, tests, and future service adapters:

```python
from jam_asset_manager import jam_asset_manager_run
from jam_core import JamConfig

config = JamConfig.from_environment()
jam_window = jam_asset_manager_run(config=config)
```

For an isolated configuration that does not depend on process-wide environment
state, use `JamConfig.from_paths(asset_manager_path, config_path,
user_config_path)`. Each instance owns its loaded application settings and local
selection state, and provides `reload()` and `save()` methods.

## Configuration

`config.json` defines the shared production structure:

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

The repository separates Maya/Qt integration from reusable application logic:

```text
jam_asset_manager.py     Maya window, widgets, and event handlers
jam_maya_scene.py        Maya render-scene operations
jam_maya_asset.py        Maya asset operations
jam_denoise.py           Legacy RenderMan integration
jam_core/
├── constants.py         Environment variables, paths, and shared defaults
├── config.py            Injectable config object, typed models, and validation
├── storage.py           Atomic JSON persistence
├── catalog.py           Asset, episode, and scene discovery
└── reports.py           Sidecar metadata and safe history rendering
```

`jam_core` has no Maya or Qt dependency, so its behavior can be tested in a
standard Python interpreter. A FastAPI service is intentionally not included:
the current application is local to Maya and has no defined remote client or
authentication boundary. The core package is suitable for reuse by an API later
if a concrete network workflow is required.

## Development

The Qt classes in `ui/ui_jam.py` and `ui/ui_report.py` are generated from the
corresponding `.ui` files. Edit the `.ui` sources and regenerate the Python files
instead of hand-editing generated code.

Run the local quality checks from the repository root:

```bash
ruff check .
ruff format --check .
python3 -m unittest discover -s tests -v
PYTHONPYCACHEPREFIX=/tmp/jam-pycache python3 -m compileall -q .
```

The test suite uses Python's standard `unittest` framework. Maya, PySide2, and
RenderMan are replaced by controlled test doubles, so configuration, filesystem,
publishing, scene-management, denoising, and UI dependency-injection behavior can
be verified outside Maya and in CI.

The community edition exposes placeholders for commercial statistics features.
The denoising module is retained for compatible legacy RenderMan pipelines and
may require site-specific commands and executable paths.

## License

Licensed under the [Apache License 2.0](LICENSE).
