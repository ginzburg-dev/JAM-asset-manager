"""Application-wide constants and environment-controlled paths."""

import os
from collections.abc import Mapping
from pathlib import Path

ASSET_MANAGER_PATH_ENV = "JAM_ASSET_MANAGER_PATH"
CONFIG_PATH_ENV = "JAM_CONFIG_PATH"
USER_CONFIG_PATH_ENV = "JAM_USER_CONFIG_PATH"
DENOISER_EXECUTABLE_ENV = "JAM_DENOISER_EXECUTABLE"

SOURCE_ROOT = Path(__file__).resolve().parent.parent


def environment_path(variable, default, environ=None):
    """Resolve a path setting from *environ* with a portable default."""
    source = os.environ if environ is None else environ
    if not isinstance(source, Mapping):
        raise TypeError("environ must be a mapping")
    value = source.get(variable)
    path = Path(value).expanduser() if value else Path(default)
    return path.resolve()


def default_user_config_path(environ=None):
    """Return the platform-appropriate location for local JAM state."""
    source = os.environ if environ is None else environ
    if source.get("APPDATA"):
        config_home = Path(source["APPDATA"])
    elif source.get("XDG_CONFIG_HOME"):
        config_home = Path(source["XDG_CONFIG_HOME"])
    else:
        config_home = Path.home() / ".config"
    return config_home / "jam-asset-manager" / "config.user.json"


ASSET_MANAGER_PATH = environment_path(ASSET_MANAGER_PATH_ENV, SOURCE_ROOT)
CONFIG_PATH = environment_path(CONFIG_PATH_ENV, ASSET_MANAGER_PATH / "config.json")
USER_CONFIG_PATH = environment_path(USER_CONFIG_PATH_ENV, default_user_config_path())
ICONS_PATH = ASSET_MANAGER_PATH / "icons"

DEFAULT_ALLOWED_EXTENSIONS = ("hdr", "ma", "mb")
DEFAULT_EXCLUDED_NAMES = (".DS_Store",)
DEFAULT_ICON_PLACEHOLDER = "icon_placeholder.jpg"
DEFAULT_ICON_SIZE = 200
DEFAULT_DENOISER_EXECUTABLE = "//server/pixar/denoise/ginzburg_denoiser_linux"
DENOISER_EXECUTABLE = os.environ.get(DENOISER_EXECUTABLE_ENV, DEFAULT_DENOISER_EXECUTABLE)

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
