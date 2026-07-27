# Changelog

All notable changes to JAM Asset Manager are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-07-28

### Added

- Maya-integrated browsing for production assets, animation shots, and render
  scenes.
- Render-scene creation, opening, updating, validation, and publishing workflows.
- Asset importing and publishing with explicit validation and error reporting.
- Notes and time reports stored as sidecar JSON metadata.
- Environment-driven, injectable configuration with per-user selection state.
- PySide2 and PySide6 compatibility for supported Maya generations.
- Optional RenderMan denoising helpers for compatible legacy pipelines.
- Automated tests for configuration, storage, catalog, Maya adapters, UI
  integration, reporting, and release tooling.
- Deterministic Maya-module release archives with SHA-256 checksums.
- Continuous integration and tag-based GitHub Releases.

### Security

- Atomic JSON writes and locking protect shared metadata from partial or
  concurrent updates.
- Report content is HTML-escaped before rendering.
- Asset traversal avoids following directory symlinks.
- Maya file operations validate paths and avoid unintended overwrites.

[Unreleased]: https://github.com/ginzburg-dev/JAM-asset-manager/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/ginzburg-dev/JAM-asset-manager/releases/tag/v0.1.0
