"""Application-wide constants and environment-controlled paths."""

import os
from pathlib import Path

ASSET_MANAGER_PATH_ENV = "JAM_ASSET_MANAGER_PATH"
CONFIG_PATH_ENV = "JAM_CONFIG_PATH"
USER_CONFIG_PATH_ENV = "JAM_USER_CONFIG_PATH"
DENOISER_EXECUTABLE_ENV = "JAM_DENOISER_EXECUTABLE"

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOT = PACKAGE_ROOT.parent.parent if PACKAGE_ROOT.parent.name == "src" else PACKAGE_ROOT
ICONS_PATH = PACKAGE_ROOT / "resources" / "icons"


def default_user_config_path():
    """Return the platform-appropriate location for local JAM state."""
    if os.getenv("APPDATA"):
        config_home = Path(os.environ["APPDATA"])
    elif os.getenv("XDG_CONFIG_HOME"):
        config_home = Path(os.environ["XDG_CONFIG_HOME"])
    else:
        config_home = Path.home() / ".config"
    return config_home / "jam-asset-manager" / "config.user.json"


DEFAULT_ALLOWED_EXTENSIONS = ("hdr", "ma", "mb")
DEFAULT_EXCLUDED_NAMES = (".DS_Store",)
DEFAULT_ICON_PLACEHOLDER = "icon_placeholder.jpg"
DEFAULT_ICON_SIZE = 200
# Resolve through PATH by default; studios can provide an absolute executable.
DEFAULT_DENOISER_EXECUTABLE = "denoise"
DENOISER_EXECUTABLE = os.getenv(DENOISER_EXECUTABLE_ENV, DEFAULT_DENOISER_EXECUTABLE)

ASSET_METADATA_TEMPLATE = {
    "assetName": "",
    "assetType": "",
    "createdTime": "",
    "messages": [],
}

REPORT_STYLES = {
    "report": ("Report", "#4D5CC1", "#403B45"),
    "note": ("Note", "#79A762", "#3B453D"),
}
