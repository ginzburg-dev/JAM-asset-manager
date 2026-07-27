"""Maya operations for importing, validating, and publishing assets."""

import logging
import os

import maya.cmds as cmds

LOGGER = logging.getLogger(__name__)


def import_asset(path):
    """Import an existing Maya asset into the current scene."""
    if not os.path.isfile(path):
        cmds.warning("Asset does not exist: {}".format(path))
        return False

    cmds.file(
        path,
        i=True,
        mergeNamespacesOnClash=True,
        namespace=":",
        ra=True,
    )
    return True


def asset_check_message():
    """Return the aggregate asset validation result.

    The community edition currently has no asset-specific validators. Keeping this
    function as the aggregation point makes additional checks easy to add without
    changing the publish workflow.
    """
    messages = []
    failures = [message[1] for message in messages if not message[0]]
    return [0, "\n\n".join(failures)] if failures else [1, ""]


def publish_asset():
    """Validate and save the current Maya asset."""
    scene_path = cmds.file(query=True, sceneName=True)
    if not scene_path:
        cmds.warning("Save the asset before publishing it.")
        return False

    check_result, check_message = asset_check_message()
    if not check_result:
        cmds.confirmDialog(
            title="Asset was not published",
            message=check_message,
            button=["OK"],
        )
        return False

    try:
        cmds.file(save=True)
    except RuntimeError:
        LOGGER.exception("Maya could not publish asset %s", scene_path)
        cmds.warning("The asset could not be published. See the Script Editor for details.")
        return False

    cmds.confirmDialog(
        title="Publish complete",
        message="The asset was published successfully.",
        button=["OK"],
    )
    return True
