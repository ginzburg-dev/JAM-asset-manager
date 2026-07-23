"""Unit tests for render-scene workflows using mocked Maya commands."""

import importlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, call, patch

from tests.support import install_maya_stubs

install_maya_stubs()

jam_maya_scene = importlib.import_module("jam_maya_scene")


class MayaSceneTestCase(unittest.TestCase):
    def setUp(self):
        self.cmds = MagicMock()
        self.cmds_patcher = patch.object(jam_maya_scene, "cmds", self.cmds)
        self.cmds_patcher.start()

    def tearDown(self):
        self.cmds_patcher.stop()

    def test_check_quality_accepts_minimum_resolution(self):
        self.cmds.getAttr.side_effect = [1600, 900]
        self.assertEqual(jam_maya_scene.check_quality(), [1, ""])

    def test_check_quality_rejects_small_resolution(self):
        self.cmds.getAttr.side_effect = [1599, 900]
        result, message = jam_maya_scene.check_quality()
        self.assertEqual(result, 0)
        self.assertIn("1600 x 900", message)

    def test_check_camera_name_requires_saved_scene(self):
        self.cmds.file.return_value = ""
        self.assertEqual(
            jam_maya_scene.check_camera_name(),
            [0, "Save the scene before validating its camera name."],
        )

    def test_check_camera_name_requires_renderable_camera(self):
        self.cmds.file.return_value = "/shots/ep001_001.ma"
        self.cmds.ls.return_value = ["perspShape"]
        self.cmds.getAttr.return_value = False
        self.assertEqual(
            jam_maya_scene.check_camera_name(),
            [0, "Set a renderable camera before publishing the scene."],
        )

    def test_check_camera_name_reports_invalid_renderable_cameras(self):
        self.cmds.file.return_value = "/shots/ep001_001.ma"
        self.cmds.ls.return_value = ["wrongCamera", "ep001_001_renderCam"]
        self.cmds.getAttr.return_value = True
        result, message = jam_maya_scene.check_camera_name()
        self.assertEqual(result, 0)
        self.assertIn("wrongCamera", message)
        self.cmds.warning.assert_called_once_with(message)

    def test_check_camera_name_accepts_matching_camera(self):
        self.cmds.file.return_value = "/shots/ep001_001.ma"
        self.cmds.ls.return_value = ["ep001_001_renderCam"]
        self.cmds.getAttr.return_value = True
        self.assertEqual(jam_maya_scene.check_camera_name(), [1, ""])

    def test_scene_check_combines_failures(self):
        with patch.object(
            jam_maya_scene, "check_camera_name", return_value=[0, "Camera"]
        ), patch.object(jam_maya_scene, "check_quality", return_value=[0, "Resolution"]):
            self.assertEqual(
                jam_maya_scene.scene_check_message(),
                [0, "Camera\n\nResolution"],
            )

    def test_check_scene_returns_boolean_and_displays_result(self):
        with patch.object(jam_maya_scene, "scene_check_message", return_value=[1, ""]):
            self.assertTrue(jam_maya_scene.check_scene())
        self.cmds.confirmDialog.assert_called_once_with(
            title="Scene check complete",
            message="No scene problems were found.",
            button=["OK"],
        )

    def test_save_changes_honors_cancel(self):
        self.cmds.file.side_effect = [True, "/shots/current.ma"]
        self.cmds.confirmDialog.return_value = "Cancel"
        self.assertFalse(jam_maya_scene._save_changes_before_opening())
        self.assertNotIn(call(save=True), self.cmds.file.call_args_list)

    def test_save_changes_saves_when_requested(self):
        self.cmds.file.side_effect = [True, "/shots/current.ma", None]
        self.cmds.confirmDialog.return_value = "Save"
        self.assertTrue(jam_maya_scene._save_changes_before_opening())
        self.cmds.file.assert_any_call(save=True)

    def test_create_render_scene_rejects_missing_inputs(self):
        with patch.object(jam_maya_scene, "_save_changes_before_opening", return_value=True):
            self.assertFalse(
                jam_maya_scene.createRenderScene(
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
            with patch.object(jam_maya_scene, "_save_changes_before_opening", return_value=True):
                self.assertTrue(
                    jam_maya_scene.createRenderScene(
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

    def test_open_render_scene_rejects_missing_file(self):
        self.assertFalse(jam_maya_scene.openRenderScene("missing.ma"))
        self.cmds.file.assert_not_called()

    def test_open_render_scene_opens_existing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            scene = Path(directory) / "render.ma"
            scene.touch()
            with patch.object(jam_maya_scene, "_save_changes_before_opening", return_value=True):
                self.assertTrue(jam_maya_scene.openRenderScene(str(scene)))
        self.cmds.file.assert_called_once_with(str(scene), open=True, force=True)

    def test_update_render_scene_requires_existing_render(self):
        self.assertFalse(jam_maya_scene.updateRenderScene("shot", "anim.ma", "render.ma"))
        self.cmds.confirmDialog.assert_called_once()

    def test_update_render_scene_replaces_checked_animation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            animation = root / "animation.ma"
            render = root / "render" / "shot.ma"
            render.parent.mkdir()
            animation.write_text("new animation", encoding="utf-8")
            render.touch()
            with patch.object(jam_maya_scene, "_save_changes_before_opening", return_value=True):
                self.assertTrue(
                    jam_maya_scene.updateRenderScene("shot", str(animation), str(render))
                )
            checked = render.parent / "shot_check_v01.ma"
            self.assertEqual(checked.read_text(encoding="utf-8"), "new animation")
        self.cmds.file.assert_has_calls(
            [call(new=True, force=True, bls=True), call(str(render), open=True, force=True)]
        )

    def test_publish_scene_handles_validation_and_save_errors(self):
        self.cmds.file.return_value = "/shots/render.ma"
        with patch.object(jam_maya_scene, "scene_check_message", return_value=[0, "Broken"]):
            self.assertFalse(jam_maya_scene.publish_scene())
        self.cmds.confirmDialog.assert_called_once_with(
            title="Scene was not published", message="Broken", button=["OK"]
        )

        self.cmds.reset_mock()
        self.cmds.file.side_effect = ["/shots/render.ma", RuntimeError("save failed")]
        with patch.object(jam_maya_scene, "scene_check_message", return_value=[1, ""]):
            with self.assertLogs(jam_maya_scene.LOGGER, level="ERROR"):
                self.assertFalse(jam_maya_scene.publish_scene())
        self.cmds.warning.assert_called_once()

    def test_publish_scene_saves_and_confirms_success(self):
        self.cmds.file.side_effect = ["/shots/render.ma", None]
        with patch.object(jam_maya_scene, "scene_check_message", return_value=[1, ""]):
            self.assertTrue(jam_maya_scene.publish_scene())
        self.cmds.file.assert_any_call(save=True)
        self.cmds.confirmDialog.assert_called_once_with(
            title="Publish complete",
            message="The scene was published successfully.",
            button=["OK"],
        )


if __name__ == "__main__":
    unittest.main()
