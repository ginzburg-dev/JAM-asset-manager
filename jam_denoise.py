"""RenderMan denoising setup helpers for Maya.

These functions depend on the legacy RenderMan-for-Maya MEL commands used by the
original production pipeline. The denoiser executable can be overridden with the
``JAM_DENOISER_EXECUTABLE`` environment variable.
"""

import logging

import maya.cmds as cmds
import maya.mel as mel

from jam_core.constants import DENOISER_EXECUTABLE

LOGGER = logging.getLogger(__name__)

DEFAULT_FILTER = "-nf 5 -ncores -1 -oPostfix _filtered -runMode multiple -runBlock 5 -fmode ST -exrlayers standard -ffkernel 2 -ffgain 5 -ffgamma 0.5 -ffsigma 10 -ffRefractionStrange 0.001 -ffIndirectSpecularStrange 0.0015 -fsw 1 -fse 0.001 -fsFallof 100 -fsKernel 2 -fsRadius 3 -fsSigmaColor 0.4 -fsSigmaAlbedo 0.4 -fsSigmaNormal 0.3 -fsSigmaDepth 10 -fstSigmaColor 0.05 -fstSigmaAlbedo 0.07 -fstSigmaNormal 0.2 -fstSigmaDepth 1000 -fsSpecularStrength 1 -fsad 1 -fsfw 0 -fsfFallof 1000 -fsfKernel 0 -fsfRadius 0 -fsfSigmaColor 0.05 -fsfSigmaAlbedo 0.2 -fsfSigmaNormal 0.2 -fsfSigmaDepth 10 -fsfSpecularStrength 0.7 -fsfad 1 -ftw 1 -ftFallof 0.7 -ftPRadius 1 -ftKernel 1 -ftbs 8 -ftISize 3 -ftSigmaColor 0.05 -ftSigmaAlbedo 0.07 -ftmt 3 -ftct 0.1 -ftpww 1 -ftpwFallof 0.01 -ftpwPRadius 1 -ftpwKernel 3 -ftpwSRadius 10 -ftpwSigmaColor 3 -ftpwSigmaAlbedo 0.07 -ftpwSigmaDistance 0.5 -ftpwst 20 -ftpwi 120"
MEDIUM_FILTER = "-nf 11 -ncores -1 -oPostfix _filtered -runMode multiple -runBlock 5 -fmode STPW -exrlayers standard -ffkernel 2 -ffgain 5 -ffgamma 0.5 -ffsigma 7 -ffRefractionStrange 0.001 -ffIndirectSpecularStrange 0.0015 -fsw 1 -fse 0.001 -fsFallof 1000 -fsKernel 2 -fsRadius 3 -fsSigmaColor 2 -fsSigmaAlbedo 0.2 -fsSigmaNormal 0.5 -fsSigmaDepth -1 -fstSigmaColor 0.2 -fstSigmaAlbedo 0.07 -fstSigmaNormal 0.5 -fstSigmaDepth -1 -fsSpecularStrength 0.1 -fsad 1 -fsfw 0 -fsfFallof 1000 -fsfKernel 0 -fsfRadius 0 -fsfSigmaColor 0.1 -fsfSigmaAlbedo 0.2 -fsfSigmaNormal 0.2 -fsfSigmaDepth 1000 -fsfSpecularStrength 0.7 -fsfad 1 -ftw 1 -ftFallof 0.01 -ftKernel 3 -ftbs 16 -ftISize 2 -ftSigmaColor 5 -ftSigmaAlbedo 0.08 -ftmt 6 -ftct 0.0017 -ftpww 1 -ftpwFallof 0.7 -ftpwKernel 3 -ftpwSRadius 10 -ftpwSigmaColor 0.7 -ftpwSigmaAlbedo 0.07 -ftpwSigmaDistance 5 -ftpwst 20 -ftpwi 120"
LARGE_FILTER = "-nf 11 -ncores -1 -oPostfix _filtered -runMode multiple -runBlock 5 -fmode STPW -exrlayers standard -ffkernel 2 -ffgain 5 -ffgamma 0.5 -ffsigma 7 -ffRefractionStrange 0.001 -ffIndirectSpecularStrange 0.0015 -fsw 1 -fse 0.001 -fsFallof 1000 -fsKernel 2 -fsRadius 3 -fsSigmaColor 0.4 -fsSigmaAlbedo 0.2 -fsSigmaNormal 0.5 -fsSigmaDepth -1 -fstSigmaColor 0.2 -fstSigmaAlbedo 0.07 -fstSigmaNormal 0.5 -fstSigmaDepth -1 -fsSpecularStrength 0.4 -fsad 1 -fsfw 0 -fsfFallof 1000 -fsfKernel 0 -fsfRadius 0 -fsfSigmaColor 0.1 -fsfSigmaAlbedo 0.2 -fsfSigmaNormal 0.2 -fsfSigmaDepth 1000 -fsfSpecularStrength 0.7 -fsfad 1 -ftw 1 -ftFallof 0.01 -ftKernel 3 -ftbs 16 -ftISize 2 -ftSigmaColor 5 -ftSigmaAlbedo 0.08 -ftmt 6 -ftct 0.0017 -ftpww 1 -ftpwFallof 0.7 -ftpwKernel 3 -ftpwSRadius 10 -ftpwSigmaColor 0.15 -ftpwSigmaAlbedo 0.07 -ftpwSigmaDistance 2 -ftpwst 20 -ftpwi 120"
VOLUME_FILTER = "-nf 3 -ncores -1 -oPostfix _filtered -runMode multiple -runBlock 5 -fmode S -exrlayers standard -ffkernel 2 -ffgain 5 -ffgamma 0.5 -ffsigma 1 -ffRefractionStrange 0.001 -ffIndirectSpecularStrange 0.0015 -fsw 1 -fse 0.001 -fsFallof 1 -fsKernel 2 -fsRadius 4 -fsSigmaColor 2 -fsSigmaAlbedo -1 -fsSigmaNormal -1 -fsSigmaDepth -1 -fsSigmaAlpha 0.07 -fstSigmaColor 0.07 -fstSigmaAlbedo -1 -fstSigmaNormal -1 -fstSigmaDepth -1 -fstSigmaAlpha 0.07 -fsSpecularStrength 1 -fsad 0 -fsfw 0 -fsfFallof 1000 -fsfKernel 0 -fsfRadius 0 -fsfSigmaColor 0.7 -fsfSigmaAlbedo 0.02 -fsfSigmaNormal 0.7 -fsfSigmaDepth 100 -fsfSpecularStrength 1 -fsfad 0 -ftw 1 -ftFallof 0.01 -ftKernel 3 -ftbs 16 -ftISize 3 -ftSigmaColor 0.1 -ftSigmaAlbedo 0.08 -ftmt 6 -ftct 0.0015 -ftpww 1 -ftpwFallof 0.01 -ftpwKernel 3 -ftpwSRadius 10 -ftpwSigmaColor 3 -ftpwSigmaAlbedo 0.07 -ftpwSigmaDistance 0.5 -ftpwst 20 -ftpwi 120"


def disable_rgba_channel():
    mel.eval(
        'rmanGetComputeBehavior "rmanFinalOutputGlobals0"; '
        'rmanSetComputeBehavior "rmanFinalOutputGlobals0" 0; '
        'rmanGetComputeBehavior "rmanFinalGlobals";'
    )


# Backwards-compatible alias for the original misspelling.
disable_rgba_chanel = disable_rgba_channel


def get_denoise_filter(layer):
    """Return the legacy filter preset for a render layer and output resolution."""
    if "volume" in layer:
        return VOLUME_FILTER
    resolution = cmds.getAttr("rmanFinalGlobals.rman__riopt__Format_resolution0")
    if resolution >= 1998:
        return DEFAULT_FILTER
    if resolution >= 1499:
        return LARGE_FILTER
    if resolution >= 999:
        return MEDIUM_FILTER
    return DEFAULT_FILTER


def denoiser_info(message):
    cmds.confirmDialog(title="JAM Denoiser", message=message, button=["OK"])


def get_render_camera():
    """Return the last renderable camera name in RenderMan-safe form."""
    renderable = [
        camera for camera in (cmds.ls(cameras=True) or []) if cmds.getAttr(camera + ".renderable")
    ]
    return renderable[-1].replace(":", "_") if renderable else ""


def _render_layers():
    return [
        layer
        for layer in (cmds.ls(type="renderLayer") or [])
        if ":" not in layer and layer != "defaultRenderLayer"
    ]


def _set_compute_behaviors(denoise_enabled, final_enabled):
    mel.eval('rmanSetComputeBehavior "rmanDenoiseCrossFramePass" {};'.format(int(denoise_enabled)))
    mel.eval('rmanSetComputeBehavior "rmanFinalGlobals" {};'.format(int(final_enabled)))
    camera = get_render_camera()
    if camera:
        mel.eval('rmanSetComputeBehavior "{}_Final" 1;'.format(camera))
        mel.eval('rmanSetComputeBehavior "{}_rmanDenoiseCrossFramePass" 1;'.format(camera))


def _restore_render_layer(layer):
    try:
        cmds.editRenderLayerGlobals(currentRenderLayer=layer)
        disable_rgba_channel()
        delete_rman_tx()
    except RuntimeError:
        LOGGER.debug("Could not fully restore RenderMan layer state", exc_info=True)


def set_denoiser_to_layer(layer, mode):
    """Set the denoiser post-render command for one render layer."""
    if layer:
        try:
            cmds.editRenderLayerGlobals(currentRenderLayer=layer)
        except RuntimeError:
            LOGGER.warning("Could not switch to render layer %s", layer)
            return False

    try:
        cmds.setAttr(
            "renderManRISGlobals.rman__riopt__Hider_pixelfiltermode",
            "weighted",
            type="string",
        )
        mel.eval("editRenderLayerAdjustment rmanDenoiseCrossFramePass.rman__torattr___passCommand;")
    except RuntimeError:
        LOGGER.exception("Could not prepare the denoiser on layer %s", layer or "default")
        return False

    output_path = mel.eval("rman getvar rfmImages;") + "/${LAYER}/$STAGE${JOBSTYLE}"
    passes = [" -bc" + output_path + "_variance.####.exr"]
    if "volume" not in layer:
        passes.extend(
            [
                " -ac" + output_path + "_albedo.####.exr",
                " -pc" + output_path + "_pw.####.exr",
                " -nc" + output_path + "_nw.####.exr",
                " -dc" + output_path + "_z.####.exr",
                " --DiffuseChannel" + output_path + "_diffuse.####.exr",
                " --SpecularChannel" + output_path + "_specular.####.exr",
                " --IndirectDiffuseChannel" + output_path + "_indirectdiffuse.####.exr",
                " --IndirectSpecularChannel" + output_path + "_indirectspecular.####.exr",
                " --RefractionChannel" + output_path + "_refraction.####.exr",
            ]
        )

    start_frame = int(cmds.getAttr("defaultRenderGlobals.startFrame"))
    end_frame = int(cmds.getAttr("defaultRenderGlobals.endFrame"))
    command = "{} -s {} -e {} {}".format(
        DENOISER_EXECUTABLE, start_frame, end_frame, "".join(passes)
    )
    if mode == "none" or "mask" in layer:
        command = ""

    mel.eval('rmanGetDefaultPass "rmanDenoiseCrossFramePass";')
    cmds.setAttr(
        "rmanDenoiseCrossFramePass.rman__torattr___passCommand",
        command,
        type="string",
    )
    return True


# Backwards-compatible alias for the original misspelling.
set_dnoiser_to_layer = set_denoiser_to_layer


def denoise_render():
    """Configure all local render layers for final rendering plus denoising."""
    if not cmds.ls("rmanDenoiseCrossFramePass"):
        mel.eval('rmanCreatePass("DenoiseCrossFrame");')
    current_layer = cmds.editRenderLayerGlobals(query=True, currentRenderLayer=True)
    cmds.setAttr("defaultRenderGlobals.animation", 1)
    cmds.setAttr("renderManRISGlobals.rman__torattr___denoise", 0)
    _set_compute_behaviors(True, True)
    mel.eval('rmanGetDefaultPass "rmanDenoiseCrossFramePass";')

    layers = _render_layers()
    if not layers:
        set_denoiser_to_layer("", "allchannels")
    for layer in layers:
        _set_compute_behaviors(True, True)
        set_denoiser_to_layer(layer, "none" if "mask" in layer else "allchannels")
    _restore_render_layer(current_layer)


def mblur_state(state):
    """Enable or disable motion blur on every local render layer."""
    enabled = state is True or str(state).lower() == "true"
    layers = _render_layers() or [None]
    for layer in layers:
        if layer:
            try:
                cmds.editRenderLayerGlobals(currentRenderLayer=layer)
            except RuntimeError:
                LOGGER.warning("Could not switch to render layer %s", layer)
                continue
        cmds.setAttr("renderManRISGlobals.rman__torattr___motionBlur", int(enabled))
        cmds.setAttr("renderManRISGlobals.rman__torattr___cameraBlur", int(enabled))


def denoise_off():
    """Disable the denoising pass while retaining the final RenderMan output."""
    current_layer = cmds.editRenderLayerGlobals(query=True, currentRenderLayer=True)
    _set_compute_behaviors(False, True)
    cmds.setAttr("defaultRenderGlobals.animation", 1)
    cmds.setAttr("renderManRISGlobals.rman__torattr___denoise", 0)
    _restore_render_layer(current_layer)


def denoise_only():
    """Configure all local render layers to run only the denoising pass."""
    current_layer = cmds.editRenderLayerGlobals(query=True, currentRenderLayer=True)
    mblur_state(False)
    cmds.setAttr("defaultRenderGlobals.animation", 0)
    cmds.setAttr("renderManRISGlobals.rman__torattr___denoise", 0)
    _set_compute_behaviors(True, False)
    mel.eval('rmanGetDefaultPass "rmanDenoiseCrossFramePass";')

    layers = _render_layers()
    if not layers:
        set_denoiser_to_layer("", "allchannels")
    for layer in layers:
        _set_compute_behaviors(True, False)
        set_denoiser_to_layer(layer, "none" if "mask" in layer else "allchannels")
    _restore_render_layer(current_layer)
    return []


def delete_rman_tx():
    """Select the legacy RenderMan texture-conversion globals when present."""
    try:
        mel.eval("select -r rmanTxMakeGlobals;")
    except RuntimeError:
        LOGGER.debug("rmanTxMakeGlobals is not available")
