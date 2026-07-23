"""Tests for the legacy RenderMan denoiser adapter."""

import importlib
import unittest
from unittest.mock import MagicMock, call, patch

from tests.support import install_maya_stubs

install_maya_stubs()

jam_denoise = importlib.import_module("jam_denoise")


class DenoiseTestCase(unittest.TestCase):
    def setUp(self):
        self.cmds = MagicMock()
        self.mel = MagicMock()
        self.cmds_patcher = patch.object(jam_denoise, "cmds", self.cmds)
        self.mel_patcher = patch.object(jam_denoise, "mel", self.mel)
        self.cmds_patcher.start()
        self.mel_patcher.start()

    def tearDown(self):
        self.mel_patcher.stop()
        self.cmds_patcher.stop()

    def test_filter_selection_uses_layer_and_resolution(self):
        self.assertEqual(jam_denoise.get_denoise_filter("volume_smoke"), jam_denoise.VOLUME_FILTER)
        self.cmds.getAttr.assert_not_called()

        cases = (
            (2200, jam_denoise.DEFAULT_FILTER),
            (1998, jam_denoise.DEFAULT_FILTER),
            (1499, jam_denoise.LARGE_FILTER),
            (999, jam_denoise.MEDIUM_FILTER),
            (800, jam_denoise.DEFAULT_FILTER),
        )
        for resolution, expected in cases:
            with self.subTest(resolution=resolution):
                self.cmds.getAttr.return_value = resolution
                self.assertEqual(jam_denoise.get_denoise_filter("beauty"), expected)

    def test_get_render_camera_returns_last_renderable_safe_name(self):
        self.cmds.ls.return_value = ["perspShape", "hero:renderCam"]
        self.cmds.getAttr.side_effect = [False, True]
        self.assertEqual(jam_denoise.get_render_camera(), "hero_renderCam")

    def test_get_render_camera_returns_empty_when_none_renderable(self):
        self.cmds.ls.return_value = None
        self.assertEqual(jam_denoise.get_render_camera(), "")

    def test_render_layers_exclude_default_and_namespaced_layers(self):
        self.cmds.ls.return_value = [
            "defaultRenderLayer",
            "beauty",
            "reference:mask",
            "volume",
        ]
        self.assertEqual(jam_denoise._render_layers(), ["beauty", "volume"])

    def test_set_denoiser_rejects_layer_switch_failure(self):
        self.cmds.editRenderLayerGlobals.side_effect = RuntimeError("unavailable")
        with self.assertLogs(jam_denoise.LOGGER, level="WARNING"):
            self.assertFalse(jam_denoise.set_denoiser_to_layer("beauty", "allchannels"))
        self.cmds.setAttr.assert_not_called()

    def test_set_denoiser_builds_channel_command(self):
        self.mel.eval.side_effect = lambda command: (
            "/renders" if command == "rman getvar rfmImages;" else None
        )

        def get_attribute(name):
            return {
                "defaultRenderGlobals.startFrame": 10,
                "defaultRenderGlobals.endFrame": 20,
            }[name]

        self.cmds.getAttr.side_effect = get_attribute
        self.assertTrue(jam_denoise.set_denoiser_to_layer("beauty", "allchannels"))

        command = self.cmds.setAttr.call_args_list[-1][0][1]
        self.assertIn(jam_denoise.DENOISER_EXECUTABLE, command)
        self.assertIn("-s 10 -e 20", command)
        self.assertIn("_variance.####.exr", command)
        self.assertIn("_albedo.####.exr", command)
        self.assertIn("--SpecularChannel", command)

    def test_set_denoiser_clears_mask_command(self):
        self.mel.eval.side_effect = lambda command: (
            "/renders" if command == "rman getvar rfmImages;" else None
        )
        self.cmds.getAttr.side_effect = [1, 2]
        self.assertTrue(jam_denoise.set_denoiser_to_layer("character_mask", "allchannels"))
        self.assertEqual(self.cmds.setAttr.call_args_list[-1][0][1], "")

    def test_motion_blur_updates_each_local_layer(self):
        with patch.object(jam_denoise, "_render_layers", return_value=["beauty", "volume"]):
            jam_denoise.mblur_state("true")
        self.cmds.editRenderLayerGlobals.assert_has_calls(
            [
                call(currentRenderLayer="beauty"),
                call(currentRenderLayer="volume"),
            ]
        )
        self.assertEqual(
            self.cmds.setAttr.call_args_list,
            [
                call("renderManRISGlobals.rman__torattr___motionBlur", 1),
                call("renderManRISGlobals.rman__torattr___cameraBlur", 1),
                call("renderManRISGlobals.rman__torattr___motionBlur", 1),
                call("renderManRISGlobals.rman__torattr___cameraBlur", 1),
            ],
        )

    def test_backwards_compatible_aliases_point_to_correct_functions(self):
        self.assertIs(jam_denoise.disable_rgba_chanel, jam_denoise.disable_rgba_channel)
        self.assertIs(jam_denoise.set_dnoiser_to_layer, jam_denoise.set_denoiser_to_layer)


if __name__ == "__main__":
    unittest.main()
