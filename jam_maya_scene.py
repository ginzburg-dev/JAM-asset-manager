"""Maya operations for validating and managing render scenes."""

import logging
import os
import shutil

import maya.cmds as cmds

LOGGER = logging.getLogger(__name__)


def get_current_scene_path():
    return cmds.file(query=True, sceneName=True)


def check_quality():
    """Require at least a 1600 x 900 output resolution."""
    width = cmds.getAttr("defaultResolution.width")
    height = cmds.getAttr("defaultResolution.height")
    if width >= 1600 and height >= 900:
        return [1, ""]
    return [0, "Change the render resolution to at least 1600 x 900."]


def check_camera_name():
    """Verify that each renderable camera contains the scene name."""
    scene_name = os.path.splitext(os.path.basename(get_current_scene_path()))[0]
    if not scene_name:
        return [0, "Save the scene before validating its camera name."]

    renderable_cameras = [
        camera for camera in (cmds.ls(type="camera") or []) if cmds.getAttr(camera + ".renderable")
    ]
    if not renderable_cameras:
        return [0, "Set a renderable camera before publishing the scene."]

    invalid_cameras = [camera for camera in renderable_cameras if scene_name not in camera]
    if not invalid_cameras:
        return [1, ""]

    message = ("The following renderable camera names do not match the scene name: {}.").format(
        ", ".join(invalid_cameras)
    )
    cmds.warning(message)
    return [0, message]


def scene_check_message():
    """Run all scene checks and combine their messages."""
    failures = [message for result, message in (check_camera_name(), check_quality()) if not result]
    return [0, "\n\n".join(failures)] if failures else [1, ""]


def check_scene():
    result, message = scene_check_message()
    if result:
        cmds.confirmDialog(
            title="Scene check complete",
            message="No scene problems were found.",
            button=["OK"],
        )
    else:
        cmds.confirmDialog(title="Scene check failed", message=message, button=["OK"])
    return bool(result)


def _save_changes_before_opening():
    """Return whether an operation that replaces the current scene may continue."""
    if not cmds.file(query=True, modified=True):
        return True

    current_scene = get_current_scene_path() or "Untitled scene"
    choice = cmds.confirmDialog(
        title="Save changes",
        message="Save changes to {}?".format(current_scene),
        button=["Save", "Don't Save", "Cancel"],
        defaultButton="Save",
        cancelButton="Cancel",
        dismissString="Cancel",
    )
    if choice == "Cancel":
        return False
    if choice == "Save":
        cmds.file(save=True)
    return True


def _checked_animation_path(name, render_filename):
    return os.path.join(os.path.dirname(render_filename), name + "_check_v01.ma")


def createRenderScene(name, anim_filename, render_filename, rs_filename):
    """Create a render scene from the configured template and animation scene."""
    if not _save_changes_before_opening():
        return False

    missing_files = [path for path in (anim_filename, rs_filename) if not os.path.isfile(path)]
    if missing_files:
        cmds.warning("Required scene file does not exist: {}".format(missing_files[0]))
        return False

    os.makedirs(os.path.dirname(render_filename), exist_ok=True)
    animation_copy = _checked_animation_path(name, render_filename)
    shutil.copy2(anim_filename, animation_copy)
    shutil.copy2(rs_filename, render_filename)

    cmds.file(new=True, force=True, bls=True)
    cmds.file(render_filename, open=True, force=True)
    cmds.file(
        animation_copy,
        reference=True,
        mergeNamespacesOnClash=True,
        namespace="anim",
    )
    return True


def openRenderScene(path):
    """Open an existing render scene after resolving unsaved changes."""
    if not os.path.isfile(path):
        cmds.warning("Render scene does not exist: {}".format(path))
        return False
    if not _save_changes_before_opening():
        return False
    cmds.file(path, open=True, force=True)
    return True


def updateRenderScene(name, anim_filename, render_filename):
    """Replace a render scene's checked animation copy and open the render scene."""
    if not os.path.isfile(render_filename):
        message = "Create the render scene before updating it."
        cmds.warning(message)
        cmds.confirmDialog(title="Render scene unavailable", message=message, button=["OK"])
        return False
    if not os.path.isfile(anim_filename):
        cmds.warning("Animation scene does not exist: {}".format(anim_filename))
        return False
    if not _save_changes_before_opening():
        return False

    shutil.copy2(anim_filename, _checked_animation_path(name, render_filename))
    cmds.file(new=True, force=True, bls=True)
    cmds.file(render_filename, open=True, force=True)
    return True


def publish_scene():
    """Validate and save the current render scene."""
    scene_path = get_current_scene_path()
    if not scene_path:
        cmds.warning("Save the scene before publishing it.")
        return False

    check_result, check_message = scene_check_message()
    if not check_result:
        cmds.confirmDialog(
            title="Scene was not published",
            message=check_message,
            button=["OK"],
        )
        return False

    try:
        cmds.file(save=True)
    except RuntimeError:
        LOGGER.exception("Maya could not publish scene %s", scene_path)
        cmds.warning("The scene could not be published. See the Script Editor for details.")
        return False

    cmds.confirmDialog(
        title="Publish complete",
        message="The scene was published successfully.",
        button=["OK"],
    )
    return True
