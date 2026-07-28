"""Maya operations for importing, validating, and publishing assets."""

import logging
import os

import maya.cmds as cmds

from ..core.publishing import publish_lock, record_publish
from .dependencies import collect_dependencies

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


def check_asset():
    """Run all asset checks and display their aggregate result."""
    result, message = asset_check_message()
    if result:
        cmds.confirmDialog(
            title="Asset check complete",
            message="No asset problems were found.",
            button=["OK"],
        )
    else:
        cmds.confirmDialog(title="Asset check failed", message=message, button=["OK"])
    return bool(result)


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
        with publish_lock(scene_path):
            try:
                cmds.file(save=True)
            except RuntimeError:
                LOGGER.exception("Maya could not publish asset %s", scene_path)
                cmds.warning("The asset could not be published. See the Script Editor for details.")
                return False

            dependency_collection = collect_dependencies(scene_path)
            try:
                publish = record_publish(
                    scene_path,
                    "asset",
                    dependencies=dependency_collection.dependencies,
                    dependency_errors=dependency_collection.errors,
                )
            except (OSError, TimeoutError, TypeError, ValueError):
                LOGGER.exception(
                    "Maya saved %s but JAM could not record publish metadata",
                    scene_path,
                )
                cmds.warning(
                    "The asset was saved, but its publish metadata could not be recorded. "
                    "See the Script Editor for details."
                )
                return False
    except (OSError, TimeoutError):
        LOGGER.exception("JAM could not acquire the publish lock for %s", scene_path)
        cmds.warning("Another publish is active or the asset publish lock is unavailable.")
        return False

    message = "The asset was published successfully as {}.".format(publish["versionLabel"])
    if publish["dependencyStatus"] == "incomplete":
        message += " The dependency scan was incomplete; see the metadata pane."
        cmds.warning("The asset was published with an incomplete dependency snapshot.")
    cmds.confirmDialog(
        title="Publish complete",
        message=message,
        button=["OK"],
    )
    return True
