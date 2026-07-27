"""Filesystem catalog discovery independent of Maya and Qt."""

import os
from pathlib import Path
from typing import NamedTuple


class AssetRecord(NamedTuple):
    name: str
    directory: str
    path: str


class EpisodeRecord(NamedTuple):
    name: str
    path: str


class SceneRecord(NamedTuple):
    name: str
    animation_path: str
    render_path: str
    render_exists: bool


def get_extension(path):
    return Path(path).suffix.lower().lstrip(".")


def is_allowed_extension(path, allowed_extensions):
    return get_extension(path) in allowed_extensions


def get_assets(path, allowed_extensions):
    """Return deterministic asset records found recursively beneath *path*."""
    assets = []
    for directory, subdirectories, files in os.walk(str(path)):
        subdirectories.sort()
        for filename in sorted(files):
            if is_allowed_extension(filename, allowed_extensions):
                full_path = os.path.join(directory, filename)
                assets.append(
                    AssetRecord(Path(filename).stem, directory, os.path.normpath(full_path))
                )
    return assets


def get_episodes(project):
    episode_root = project.root / project.episode_path
    if not episode_root.is_dir():
        return []
    return [
        EpisodeRecord(path.name, str(path))
        for path in sorted(episode_root.iterdir(), key=lambda item: item.name)
        if path.is_dir()
    ]


def is_valid_animation_scene_name(episode, name):
    prefix = episode + "_"
    suffix = name[len(prefix) :] if name.startswith(prefix) else ""
    shot_number, extension = os.path.splitext(suffix)
    return len(shot_number) == 3 and shot_number.isdigit() and extension.lower() == ".ma"


def get_scenes(project, episode, excluded_names=()):
    """Return animation scenes and their corresponding render-scene state."""
    episode_root = project.root / project.episode_path / episode
    animation_path = episode_root / "maya" / "animation"
    render_path = episode_root / "render"
    if not animation_path.is_dir():
        return []

    render_scenes = {}
    if render_path.is_dir():
        for directory in sorted(render_path.iterdir(), key=lambda item: item.name):
            scene_path = directory / (directory.name + ".ma")
            if directory.name not in excluded_names and scene_path.is_file():
                render_scenes[directory.name] = scene_path

    scenes = []
    for animation_scene in sorted(animation_path.iterdir(), key=lambda item: item.name):
        if (
            animation_scene.name in excluded_names
            or not animation_scene.is_file()
            or not is_valid_animation_scene_name(episode, animation_scene.name)
        ):
            continue
        scene_name = animation_scene.stem
        default_render_path = render_path / scene_name / animation_scene.name
        scene_render_path = render_scenes.get(scene_name, default_render_path)
        scenes.append(
            SceneRecord(
                scene_name,
                str(animation_scene),
                str(scene_render_path),
                scene_name in render_scenes,
            )
        )
    return scenes


def is_path_within(path, parent):
    if not path or not parent:
        return False
    try:
        return os.path.commonpath(
            [os.path.abspath(str(path)), os.path.abspath(str(parent))]
        ) == os.path.abspath(str(parent))
    except ValueError:
        return False
