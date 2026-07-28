"""Unit tests for render-scene workflows using mocked Maya commands."""

import importlib
import tempfile
import unittest
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, call, patch

from tests.support import install_maya_stubs

install_maya_stubs()

maya_scenes = importlib.import_module("jam_asset_manager.maya.scenes")


class MayaSceneTestCase(unittest.TestCase):
    def setUp(self):
        self.cmds = MagicMock()
        self.cmds_patcher = patch.object(maya_scenes, "cmds", self.cmds)
        self.cmds_patcher.start()
        self.lock_patcher = patch.object(
            maya_scenes,
            "publish_lock",
            side_effect=lambda _path: nullcontext(),
        )
        self.lock_patcher.start()

    def tearDown(self):
        self.lock_patcher.stop()
        self.cmds_patcher.stop()

    def test_check_quality_accepts_minimum_resolution(self):
        self.cmds.getAttr.side_effect = [1600, 900]
        self.assertEqual(maya_scenes.check_quality(), [1, ""])

    def test_check_quality_rejects_small_resolution(self):
        self.cmds.getAttr.side_effect = [1599, 900]
        result, message = maya_scenes.check_quality()
        self.assertEqual(result, 0)
        self.assertIn("1600 x 900", message)

    def test_check_camera_name_requires_saved_scene(self):
        self.cmds.file.return_value = ""
        self.assertEqual(
            maya_scenes.check_camera_name(),
            [0, "Save the scene before validating its camera name."],
        )

    def test_check_camera_name_requires_renderable_camera(self):
        self.cmds.file.return_value = "/shots/ep001_001.ma"
        self.cmds.ls.return_value = ["perspShape"]
        self.cmds.getAttr.return_value = False
        self.assertEqual(
            maya_scenes.check_camera_name(),
            [0, "Set a renderable camera before publishing the scene."],
        )

    def test_check_camera_name_reports_invalid_renderable_cameras(self):
        self.cmds.file.return_value = "/shots/ep001_001.ma"
        self.cmds.ls.return_value = ["wrongCamera", "ep001_001_renderCam"]
        self.cmds.getAttr.return_value = True
        result, message = maya_scenes.check_camera_name()
        self.assertEqual(result, 0)
        self.assertIn("wrongCamera", message)
        self.cmds.warning.assert_called_once_with(message)

    def test_check_camera_name_accepts_matching_camera(self):
        self.cmds.file.return_value = "/shots/ep001_001.ma"
        self.cmds.ls.return_value = ["ep001_001_renderCam"]
        self.cmds.getAttr.return_value = True
        self.assertEqual(maya_scenes.check_camera_name(), [1, ""])

    def test_scene_check_combines_failures(self):
        with patch.object(
            maya_scenes, "check_camera_name", return_value=[0, "Camera"]
        ), patch.object(maya_scenes, "check_quality", return_value=[0, "Resolution"]):
            self.assertEqual(
                maya_scenes.scene_check_message(),
                [0, "Camera\n\nResolution"],
            )

    def test_check_scene_returns_boolean_and_displays_result(self):
        with patch.object(maya_scenes, "scene_check_message", return_value=[1, ""]):
            self.assertTrue(maya_scenes.check_scene())
        self.cmds.confirmDialog.assert_called_once_with(
            title="Scene check complete",
            message="No scene problems were found.",
            button=["OK"],
        )

    def test_save_changes_honors_cancel(self):
        self.cmds.file.side_effect = [True, "/shots/current.ma"]
        self.cmds.confirmDialog.return_value = "Cancel"
        self.assertFalse(maya_scenes._save_changes_before_opening())
        self.assertNotIn(call(save=True), self.cmds.file.call_args_list)

    def test_save_changes_saves_when_requested(self):
        self.cmds.file.side_effect = [True, "/shots/current.ma", None]
        self.cmds.confirmDialog.return_value = "Save"
        self.assertTrue(maya_scenes._save_changes_before_opening())
        self.cmds.file.assert_any_call(save=True)

    def test_create_render_scene_rejects_missing_inputs(self):
        with patch.object(maya_scenes, "_save_changes_before_opening", return_value=True):
            self.assertFalse(
                maya_scenes.create_render_scene(
                    "ep001_001", "missing-animation.ma", "render.ma", "missing-template.ma"
                )
            )
        self.cmds.warning.assert_called_once_with(
            "Required scene file does not exist: missing-animation.ma"
        )

    def test_create_render_scene_copies_opens_and_references_animation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            animation = root / "animation.ma"
            template = root / "template.ma"
            render = root / "render" / "ep001_001.ma"
            animation.write_text("animation", encoding="utf-8")
            template.write_text("template", encoding="utf-8")
            with patch.object(maya_scenes, "_save_changes_before_opening", return_value=True):
                self.assertTrue(
                    maya_scenes.create_render_scene(
                        "ep001_001", str(animation), str(render), str(template)
                    )
                )

            checked = render.parent / "ep001_001_check_v01.ma"
            self.assertEqual(render.read_text(encoding="utf-8"), "template")
            self.assertEqual(checked.read_text(encoding="utf-8"), "animation")
            self.cmds.file.assert_has_calls(
                [
                    call(new=True, force=True, bls=True),
                    call(str(render), open=True, force=True),
                    call(
                        str(checked),
                        reference=True,
                        mergeNamespacesOnClash=True,
                        namespace="anim",
                    ),
                ]
            )

    def test_create_render_scene_never_overwrites_existing_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            animation = root / "animation.ma"
            template = root / "template.ma"
            render = root / "render" / "shot.ma"
            render.parent.mkdir()
            animation.write_text("animation", encoding="utf-8")
            template.write_text("template", encoding="utf-8")
            render.write_text("existing render", encoding="utf-8")

            self.assertFalse(
                maya_scenes.create_render_scene(
                    "shot",
                    str(animation),
                    str(render),
                    str(template),
                )
            )

            self.assertEqual(render.read_text(encoding="utf-8"), "existing render")
            self.cmds.warning.assert_called_once_with(
                "Render-scene output already exists: {}".format(render)
            )
            self.cmds.file.assert_not_called()

    def test_open_render_scene_rejects_missing_file(self):
        self.assertFalse(maya_scenes.open_render_scene("missing.ma"))
        self.cmds.file.assert_not_called()

    def test_open_render_scene_opens_existing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            scene = Path(directory) / "render.ma"
            scene.touch()
            with patch.object(maya_scenes, "_save_changes_before_opening", return_value=True):
                self.assertTrue(maya_scenes.open_render_scene(str(scene)))
        self.cmds.file.assert_called_once_with(str(scene), open=True, force=True)

    def test_update_render_scene_requires_existing_render(self):
        self.assertFalse(maya_scenes.update_render_scene("shot", "anim.ma", "render.ma"))
        self.cmds.confirmDialog.assert_called_once()

    def test_update_render_scene_replaces_checked_animation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            animation = root / "animation.ma"
            render = root / "render" / "shot.ma"
            render.parent.mkdir()
            animation.write_text("new animation", encoding="utf-8")
            render.touch()
            with patch.object(maya_scenes, "_save_changes_before_opening", return_value=True):
                self.assertTrue(
                    maya_scenes.update_render_scene("shot", str(animation), str(render))
                )
            checked = render.parent / "shot_check_v01.ma"
            self.assertEqual(checked.read_text(encoding="utf-8"), "new animation")
        self.cmds.file.assert_has_calls(
            [call(new=True, force=True, bls=True), call(str(render), open=True, force=True)]
        )

    def test_publish_scene_handles_validation_and_save_errors(self):
        self.cmds.file.return_value = "/shots/render.ma"
        with patch.object(maya_scenes, "scene_check_message", return_value=[0, "Broken"]):
            self.assertFalse(maya_scenes.publish_scene())
        self.cmds.confirmDialog.assert_called_once_with(
            title="Scene was not published", message="Broken", button=["OK"]
        )

        self.cmds.reset_mock()
        self.cmds.file.side_effect = ["/shots/render.ma", RuntimeError("save failed")]
        with patch.object(maya_scenes, "scene_check_message", return_value=[1, ""]):
            with self.assertLogs(maya_scenes.LOGGER, level="ERROR"):
                self.assertFalse(maya_scenes.publish_scene())
        self.cmds.warning.assert_called_once()

    def test_publish_scene_saves_and_confirms_success(self):
        self.cmds.file.side_effect = ["/shots/render.ma", None]
        dependencies = [{"kind": "reference", "path": "/shots/animation.ma"}]
        with patch.object(
            maya_scenes,
            "scene_check_message",
            return_value=[1, ""],
        ), patch.object(
            maya_scenes,
            "collect_dependencies",
            return_value=SimpleNamespace(dependencies=dependencies, errors=()),
        ) as collect_dependencies, patch.object(
            maya_scenes,
            "record_publish",
            return_value={"versionLabel": "v012", "dependencyStatus": "complete"},
        ) as record_publish:
            self.assertTrue(maya_scenes.publish_scene())

        self.cmds.file.assert_any_call(save=True)
        collect_dependencies.assert_called_once_with("/shots/render.ma")
        record_publish.assert_called_once_with(
            "/shots/render.ma",
            "render_scene",
            dependencies=dependencies,
            dependency_errors=(),
        )
        self.cmds.confirmDialog.assert_called_once_with(
            title="Publish complete",
            message="The scene was published successfully as v012.",
            button=["OK"],
        )

    def test_publish_scene_reports_metadata_failure_after_save(self):
        self.cmds.file.side_effect = ["/shots/render.ma", None]
        with patch.object(
            maya_scenes,
            "scene_check_message",
            return_value=[1, ""],
        ), patch.object(
            maya_scenes,
            "collect_dependencies",
            return_value=SimpleNamespace(dependencies=(), errors=()),
        ), patch.object(
            maya_scenes,
            "record_publish",
            side_effect=TimeoutError("metadata lock unavailable"),
        ):
            with self.assertLogs(maya_scenes.LOGGER, level="ERROR"):
                self.assertFalse(maya_scenes.publish_scene())

        self.cmds.file.assert_any_call(save=True)
        self.cmds.warning.assert_called_once_with(
            "The scene was saved, but its publish metadata could not be recorded. "
            "See the Script Editor for details."
        )
        self.cmds.confirmDialog.assert_not_called()

    def test_publish_scene_stops_when_the_publish_lock_is_busy(self):
        self.cmds.file.return_value = "/shots/render.ma"
        with patch.object(
            maya_scenes,
            "scene_check_message",
            return_value=[1, ""],
        ), patch.object(
            maya_scenes,
            "publish_lock",
            side_effect=TimeoutError("busy"),
        ):
            with self.assertLogs(maya_scenes.LOGGER, level="ERROR"):
                self.assertFalse(maya_scenes.publish_scene())

        self.assertNotIn(call(save=True), self.cmds.file.call_args_list)
        self.cmds.warning.assert_called_once_with(
            "Another publish is active or the scene publish lock is unavailable."
        )


if __name__ == "__main__":
    unittest.main()
