"""Validated application and user configuration loading."""

import os
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Tuple

from .constants import (
    ASSET_MANAGER_PATH,
    ASSET_MANAGER_PATH_ENV,
    CONFIG_PATH,
    CONFIG_PATH_ENV,
    DEFAULT_ALLOWED_EXTENSIONS,
    DEFAULT_EXCLUDED_NAMES,
    DEFAULT_ICON_PLACEHOLDER,
    DEFAULT_ICON_SIZE,
    SOURCE_ROOT,
    USER_CONFIG_PATH,
    USER_CONFIG_PATH_ENV,
    default_user_config_path,
    environment_path,
)
from .storage import read_json, write_json


class ConfigurationError(ValueError):
    """Raised when a JAM configuration file is missing required or valid values."""


@dataclass(frozen=True)
class AssetTypeConfig:
    name: str
    relative_path: str


@dataclass(frozen=True)
class ProjectConfig:
    name: str
    root: Path
    episode_path: str
    asset_types: Tuple[AssetTypeConfig, ...]
    render_scene: Path

    def asset_directory(self, asset_type_name):
        for asset_type in self.asset_types:
            if asset_type.name == asset_type_name:
                return self.root / asset_type.relative_path
        return None


@dataclass(frozen=True)
class ApplicationConfig:
    name: str
    projects: Tuple[ProjectConfig, ...]
    current_project: str
    excluded_names: Tuple[str, ...] = DEFAULT_EXCLUDED_NAMES
    allowed_extensions: Tuple[str, ...] = DEFAULT_ALLOWED_EXTENSIONS
    icon_placeholder: str = DEFAULT_ICON_PLACEHOLDER
    icon_size: int = DEFAULT_ICON_SIZE

    def project(self, name):
        for project in self.projects:
            if project.name == name:
                return project
        return None


@dataclass
class ProjectState:
    asset_type: str = ""
    episode: str = ""


@dataclass
class UserState:
    current_project: str
    projects: Dict[str, ProjectState] = field(default_factory=dict)

    def project(self, name):
        return self.projects.setdefault(name, ProjectState())

    def to_mapping(self):
        return {
            "currentProject": self.current_project,
            "configs": [
                {
                    "projectName": project_name,
                    "currentAssetType": state.asset_type,
                    "currentEpisode": state.episode,
                }
                for project_name, state in sorted(self.projects.items())
            ],
        }


@dataclass
class JamConfig:
    """Loaded JAM settings and local state passed to application consumers.

    Use :meth:`from_environment` for normal application startup. Constructing or
    loading an explicit instance makes the core and Maya UI straightforward to
    test, embed, or reuse without changing process-wide globals.
    """

    application: ApplicationConfig
    user_state: UserState
    asset_manager_path: Path
    config_path: Path
    user_config_path: Path

    @property
    def icons_path(self):
        return self.asset_manager_path / "icons"

    def project(self, name):
        return self.application.project(name)

    def reload(self):
        """Reload local UI state from this instance's configured path."""
        self.user_state = load_user_state(self.application, self.user_config_path)
        return self.user_state

    def save(self):
        """Persist local UI state to this instance's configured path."""
        save_user_state(self.user_state, self.user_config_path)

    @classmethod
    def from_paths(cls, asset_manager_path, config_path=None, user_config_path=None):
        """Load an isolated config instance from explicit filesystem paths."""
        root = Path(asset_manager_path).expanduser().resolve()
        shared_path = Path(config_path or root / "config.json").expanduser().resolve()
        local_path = Path(user_config_path or default_user_config_path()).expanduser().resolve()
        application = load_application_config(shared_path, root)
        return cls(
            application=application,
            user_state=load_user_state(application, local_path),
            asset_manager_path=root,
            config_path=shared_path,
            user_config_path=local_path,
        )

    @classmethod
    def from_environment(cls, environ=None):
        """Load paths and settings from JAM environment variables."""
        root = environment_path(ASSET_MANAGER_PATH_ENV, SOURCE_ROOT, environ)
        shared_path = environment_path(CONFIG_PATH_ENV, root / "config.json", environ)
        local_path = environment_path(
            USER_CONFIG_PATH_ENV,
            default_user_config_path(environ),
            environ,
        )
        return cls.from_paths(root, shared_path, local_path)


def resolve_path(value, base_path=ASSET_MANAGER_PATH):
    """Expand environment/user markers and anchor relative paths to *base_path*."""
    if not isinstance(value, str) or not value.strip():
        raise ConfigurationError("Configured paths must be non-empty strings.")
    expanded = Path(os.path.expandvars(os.path.expanduser(value)))
    if not expanded.is_absolute():
        expanded = Path(base_path) / expanded
    return expanded.resolve()


def _required_string(mapping, key, context):
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ConfigurationError("{}.{} must be a non-empty string.".format(context, key))
    return value.strip()


def _parse_asset_types(values, context):
    if not isinstance(values, list):
        raise ConfigurationError("{}.assets must be a list.".format(context))
    asset_types = []
    for index, value in enumerate(values):
        if not isinstance(value, Mapping):
            raise ConfigurationError("{}.assets[{}] must be an object.".format(context, index))
        item_context = "{}.assets[{}]".format(context, index)
        asset_types.append(
            AssetTypeConfig(
                name=_required_string(value, "assetType", item_context),
                relative_path=_required_string(value, "assetTypePath", item_context),
            )
        )
    return tuple(asset_types)


def _parse_projects(values, base_path):
    if not isinstance(values, list) or not values:
        raise ConfigurationError("projects must be a non-empty list.")
    projects = []
    names = set()
    for index, value in enumerate(values):
        if not isinstance(value, Mapping):
            raise ConfigurationError("projects[{}] must be an object.".format(index))
        context = "projects[{}]".format(index)
        name = _required_string(value, "projectName", context)
        if name in names:
            raise ConfigurationError("Project names must be unique: {}.".format(name))
        names.add(name)
        projects.append(
            ProjectConfig(
                name=name,
                root=resolve_path(_required_string(value, "projectPath", context), base_path),
                episode_path=_required_string(value, "episodePath", context),
                asset_types=_parse_asset_types(value.get("assets", []), context),
                render_scene=resolve_path(_required_string(value, "rsScene", context), base_path),
            )
        )
    return tuple(projects)


def load_application_config(path=CONFIG_PATH, asset_manager_path=ASSET_MANAGER_PATH):
    """Load and validate the shared JAM application configuration."""
    config_path = Path(path)
    if not config_path.is_file():
        raise ConfigurationError("JAM configuration was not found: {}".format(config_path))
    try:
        data = read_json(config_path)
    except (OSError, ValueError) as error:
        raise ConfigurationError(
            "Could not read JAM configuration {}: {}".format(config_path, error)
        ) from error
    if not isinstance(data, Mapping):
        raise ConfigurationError("The JAM configuration root must be an object.")

    projects = _parse_projects(data.get("projects"), Path(asset_manager_path))
    project_names = {project.name for project in projects}
    current_project = data.get("currentProject") or projects[0].name
    if current_project not in project_names:
        raise ConfigurationError(
            "currentProject references an unknown project: {}.".format(current_project)
        )

    extensions = data.get("allowedExtensions", list(DEFAULT_ALLOWED_EXTENSIONS))
    if not isinstance(extensions, list) or not all(
        isinstance(extension, str) and extension.strip() for extension in extensions
    ):
        raise ConfigurationError("allowedExtensions must be a list of strings.")
    normalized_extensions = tuple(
        dict.fromkeys(extension.lower().lstrip(".") for extension in extensions)
    )

    excluded_names = data.get("excludedNames", list(DEFAULT_EXCLUDED_NAMES))
    if not isinstance(excluded_names, list) or not all(
        isinstance(name, str) for name in excluded_names
    ):
        raise ConfigurationError("excludedNames must be a list of strings.")

    icon_size = data.get("iconSize", DEFAULT_ICON_SIZE)
    if not isinstance(icon_size, int) or icon_size <= 0:
        raise ConfigurationError("iconSize must be a positive integer.")

    return ApplicationConfig(
        name=str(data.get("assetManagerName") or "JAM Asset Manager"),
        projects=projects,
        current_project=current_project,
        excluded_names=tuple(excluded_names),
        allowed_extensions=normalized_extensions,
        icon_placeholder=str(data.get("iconPlaceholder") or DEFAULT_ICON_PLACEHOLDER),
        icon_size=icon_size,
    )


def load_user_state(application_config, path=USER_CONFIG_PATH):
    """Load local selections and merge them with configured project defaults."""
    defaults = {
        project.name: ProjectState(
            asset_type=project.asset_types[0].name if project.asset_types else ""
        )
        for project in application_config.projects
    }
    user_path = Path(path)
    if not user_path.is_file():
        return UserState(application_config.current_project, defaults)

    try:
        data = read_json(user_path)
    except (OSError, ValueError) as error:
        raise ConfigurationError(
            "Could not read user configuration {}: {}".format(user_path, error)
        ) from error
    if not isinstance(data, Mapping):
        raise ConfigurationError("The user configuration root must be an object.")

    configured_project_names = set(defaults)
    current_project = data.get("currentProject", application_config.current_project)
    if current_project not in configured_project_names:
        current_project = application_config.current_project

    configs = data.get("configs", [])
    if not isinstance(configs, list):
        raise ConfigurationError("User configuration 'configs' must be a list.")
    for item in configs:
        if not isinstance(item, Mapping):
            continue
        project_name = item.get("projectName")
        if project_name not in defaults:
            continue
        configured_project = application_config.project(project_name)
        valid_asset_types = {asset_type.name for asset_type in configured_project.asset_types}
        saved_asset_type = str(item.get("currentAssetType") or "")
        if saved_asset_type not in valid_asset_types:
            saved_asset_type = defaults[project_name].asset_type
        defaults[project_name] = ProjectState(
            asset_type=saved_asset_type,
            episode=str(item.get("currentEpisode") or ""),
        )
    return UserState(current_project, defaults)


def save_user_state(user_state, path=USER_CONFIG_PATH):
    write_json(path, user_state.to_mapping())
