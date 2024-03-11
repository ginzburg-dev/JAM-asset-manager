import os
import sys
import shutil

from datetime import datetime
from functools import partial

import maya.cmds as cmds
import maya.mel as mel

def disable_rgba_chanel():
     mel.eval('rmanGetComputeBehavior "rmanFinalOutputGlobals0"; rmanSetComputeBehavior "rmanFinalOutputGlobals0" 0; rmanGetComputeBehavior "rmanFinalGlobals";')

def get_denoise_filter(layer):
     defilter = "-nf 5 -ncores -1 -oPostfix _filtered -runMode multiple -runBlock 5 -fmode ST -exrlayers standard -ffkernel 2 -ffgain 5 -ffgamma 0.5 -ffsigma 10 -ffRefractionStrange 0.001 -ffIndirectSpecularStrange 0.0015 -fsw 1 -fse 0.001 -fsFallof 100 -fsKernel 2 -fsRadius 3 -fsSigmaColor 0.4 -fsSigmaAlbedo 0.4 -fsSigmaNormal 0.3 -fsSigmaDepth 10 -fstSigmaColor 0.05 -fstSigmaAlbedo 0.07 -fstSigmaNormal 0.2 -fstSigmaDepth 1000 -fsSpecularStrength 1 -fsad 1 -fsfw 0 -fsfFallof 1000 -fsfKernel 0 -fsfRadius 0 -fsfSigmaColor 0.05 -fsfSigmaAlbedo 0.2 -fsfSigmaNormal 0.2 -fsfSigmaDepth 10 -fsfSpecularStrength 0.7 -fsfad 1 -ftw 1 -ftFallof 0.7 -ftPRadius 1 -ftKernel 1 -ftbs 8 -ftISize 3 -ftSigmaColor 0.05 -ftSigmaAlbedo 0.07 -ftmt 3 -ftct 0.1 -ftpww 1 -ftpwFallof 0.01 -ftpwPRadius 1 -ftpwKernel 3 -ftpwSRadius 10 -ftpwSigmaColor 3 -ftpwSigmaAlbedo 0.07 -ftpwSigmaDistance 0.5 -ftpwst 20 -ftpwi 120"     
     if cmds.getAttr("rmanFinalGlobals.rman__riopt__Format_resolution0") >= 999:
          defilter = "-nf 11 -ncores -1 -oPostfix _filtered -runMode multiple -runBlock 5 -fmode STPW -exrlayers standard -ffkernel 2 -ffgain 5 -ffgamma 0.5 -ffsigma 7 -ffRefractionStrange 0.001 -ffIndirectSpecularStrange 0.0015 -fsw 1 -fse 0.001 -fsFallof 1000 -fsKernel 2 -fsRadius 3 -fsSigmaColor 2 -fsSigmaAlbedo 0.2 -fsSigmaNormal 0.5 -fsSigmaDepth -1 -fstSigmaColor 0.2 -fstSigmaAlbedo 0.07 -fstSigmaNormal 0.5 -fstSigmaDepth -1 -fsSpecularStrength 0.1 -fsad 1 -fsfw 0 -fsfFallof 1000 -fsfKernel 0 -fsfRadius 0 -fsfSigmaColor 0.1 -fsfSigmaAlbedo 0.2 -fsfSigmaNormal 0.2 -fsfSigmaDepth 1000 -fsfSpecularStrength 0.7 -fsfad 1 -ftw 1 -ftFallof 0.01 -ftKernel 3 -ftbs 16 -ftISize 2 -ftSigmaColor 5 -ftSigmaAlbedo 0.08 -ftmt 6 -ftct 0.0017 -ftpww 1 -ftpwFallof 0.7 -ftpwKernel 3 -ftpwSRadius 10 -ftpwSigmaColor 0.7 -ftpwSigmaAlbedo 0.07 -ftpwSigmaDistance 5 -ftpwst 20 -ftpwi 120"
     if cmds.getAttr("rmanFinalGlobals.rman__riopt__Format_resolution0") >= 1499:
          defilter = "-nf 11 -ncores -1 -oPostfix _filtered -runMode multiple -runBlock 5 -fmode STPW -exrlayers standard -ffkernel 2 -ffgain 5 -ffgamma 0.5 -ffsigma 7 -ffRefractionStrange 0.001 -ffIndirectSpecularStrange 0.0015 -fsw 1 -fse 0.001 -fsFallof 1000 -fsKernel 2 -fsRadius 3 -fsSigmaColor 0.4 -fsSigmaAlbedo 0.2 -fsSigmaNormal 0.5 -fsSigmaDepth -1 -fstSigmaColor 0.2 -fstSigmaAlbedo 0.07 -fstSigmaNormal 0.5 -fstSigmaDepth -1 -fsSpecularStrength 0.4 -fsad 1 -fsfw 0 -fsfFallof 1000 -fsfKernel 0 -fsfRadius 0 -fsfSigmaColor 0.1 -fsfSigmaAlbedo 0.2 -fsfSigmaNormal 0.2 -fsfSigmaDepth 1000 -fsfSpecularStrength 0.7 -fsfad 1 -ftw 1 -ftFallof 0.01 -ftKernel 3 -ftbs 16 -ftISize 2 -ftSigmaColor 5 -ftSigmaAlbedo 0.08 -ftmt 6 -ftct 0.0017 -ftpww 1 -ftpwFallof 0.7 -ftpwKernel 3 -ftpwSRadius 10 -ftpwSigmaColor 0.15 -ftpwSigmaAlbedo 0.07 -ftpwSigmaDistance 2 -ftpwst 20 -ftpwi 120"
     if cmds.getAttr("rmanFinalGlobals.rman__riopt__Format_resolution0") >= 1998:
          defilter = "-nf 5 -ncores -1 -oPostfix _filtered -runMode multiple -runBlock 5 -fmode ST -exrlayers standard -ffkernel 2 -ffgain 5 -ffgamma 0.5 -ffsigma 10 -ffRefractionStrange 0.001 -ffIndirectSpecularStrange 0.0015 -fsw 1 -fse 0.001 -fsFallof 100 -fsKernel 2 -fsRadius 3 -fsSigmaColor 0.4 -fsSigmaAlbedo 0.4 -fsSigmaNormal 0.3 -fsSigmaDepth 10 -fstSigmaColor 0.05 -fstSigmaAlbedo 0.07 -fstSigmaNormal 0.2 -fstSigmaDepth 1000 -fsSpecularStrength 1 -fsad 1 -fsfw 0 -fsfFallof 1000 -fsfKernel 0 -fsfRadius 0 -fsfSigmaColor 0.05 -fsfSigmaAlbedo 0.2 -fsfSigmaNormal 0.2 -fsfSigmaDepth 10 -fsfSpecularStrength 0.7 -fsfad 1 -ftw 1 -ftFallof 0.7 -ftPRadius 1 -ftKernel 1 -ftbs 8 -ftISize 3 -ftSigmaColor 0.05 -ftSigmaAlbedo 0.07 -ftmt 3 -ftct 0.1 -ftpww 1 -ftpwFallof 0.01 -ftpwPRadius 1 -ftpwKernel 3 -ftpwSRadius 10 -ftpwSigmaColor 3 -ftpwSigmaAlbedo 0.07 -ftpwSigmaDistance 0.5 -ftpwst 20 -ftpwi 120"
     if len(layer.split("volume")) > 1:
          defilter ="-nf 3 -ncores -1 -oPostfix _filtered -runMode multiple -runBlock 5 -fmode S -exrlayers standard -ffkernel 2 -ffgain 5 -ffgamma 0.5 -ffsigma 1 -ffRefractionStrange 0.001 -ffIndirectSpecularStrange 0.0015 -fsw 1 -fse 0.001 -fsFallof 1 -fsKernel 2 -fsRadius 4 -fsSigmaColor 2 -fsSigmaAlbedo -1 -fsSigmaNormal -1 -fsSigmaDepth -1 -fsSigmaAlpha 0.07 -fstSigmaColor 0.07 -fstSigmaAlbedo -1 -fstSigmaNormal -1 -fstSigmaDepth -1 -fstSigmaAlpha 0.07 -fsSpecularStrength 1 -fsad 0 -fsfw 0 -fsfFallof 1000 -fsfKernel 0 -fsfRadius 0 -fsfSigmaColor 0.7 -fsfSigmaAlbedo 0.02 -fsfSigmaNormal 0.7 -fsfSigmaDepth 100 -fsfSpecularStrength 1 -fsfad 0 -ftw 1 -ftFallof 0.01 -ftKernel 3 -ftbs 16 -ftISize 3 -ftSigmaColor 0.1 -ftSigmaAlbedo 0.08 -ftmt 6 -ftct 0.0015 -ftpww 1 -ftpwFallof 0.01 -ftpwKernel 3 -ftpwSRadius 10 -ftpwSigmaColor 3 -ftpwSigmaAlbedo 0.07 -ftpwSigmaDistance 0.5 -ftpwst 20 -ftpwi 120"
     
     #defilter = "-nf 5 -ncores -1 -oPostfix _filtered -runMode multiple -runBlock 5 -fmode ST -exrlayers standard -ffkernel 2 -ffgain 5 -ffgamma 0.5 -ffsigma 6 -ffRefractionStrange 0.001 -fsw 1 -fse 1 -fsFallof 1000 -fsKernel 3 -fsRadius 3 -fsSigmaColor 5 -fsSigmaAlbedo 0.4 -fsSigmaNormal 0.76 -fsSigmaDepth 1000 -fstSigmaColor 0.7 -fstSigmaAlbedo 0.3 -fstSigmaNormal 0.7 -fstSigmaDepth 1000 -fsSpecularStrength 1 -fsad 1 -fsfw 1 -fsfFallof 1000 -fsfKernel 0 -fsfRadius 7 -fsfSigmaColor 0.7 -fsfSigmaAlbedo 0.2 -fsfSigmaNormal 0.2 -fsfSigmaDepth 1000 -fsfSpecularStrength 1 -fsfad 1 -ftw 1 -ftFallof 0.5 -ftKernel 5 -ftbs 16 -ftISize 3 -ftSigmaColor 5 -ftSigmaAlbedo 0.08 -ftmt 6 -ftct 0.0017 -ftpww 1 -ftpwFallof 1.2 -ftpwKernel 5 -ftpwSRadius 10 -ftpwSigmaColor 0.5 -ftpwSigmaAlbedo 0.07 -ftpwSigmaDistance 0.5 -ftpwst 20 -ftpwi 120"
     #if len(layer.split("chars")) > 1:
     #     defilter = "-nf 5 -ncores -1 -oPostfix _filtered -runMode multiple -runBlock 5 -fmode ST -exrlayers standard -ffkernel 2 -ffgain 5 -ffgamma 0.5 -ffsigma 10 -ffRefractionStrange 0.001 -ffIndirectSpecularStrange 0.0015 -fsw 1 -fse 1 -fsFallof 100 -fsKernel 3 -fsRadius 2 -fsSigmaColor 3 -fsSigmaAlbedo 0.4 -fsSigmaNormal 0.76 -fsSigmaDepth 1000 -fstSigmaColor 0.5 -fstSigmaAlbedo 0.12 -fstSigmaNormal 0.3 -fstSigmaDepth 2 -fsSpecularStrength 1 -fsad 1 -fsfw 1 -fsfFallof 1000 -fsfKernel 0 -fsfRadius 7 -fsfSigmaColor 0.07 -fsfSigmaAlbedo 0.2 -fsfSigmaNormal 0.2 -fsfSigmaDepth 10 -fsfSpecularStrength 1 -fsfad 1 -ftw 1 -ftFallof 0.01 -ftKernel 3 -ftbs 16 -ftISize 3 -ftSigmaColor 3 -ftSigmaAlbedo 0.08 -ftmt 6 -ftct 0.002 -ftpww 1 -ftpwFallof 0.01 -ftpwKernel 3 -ftpwSRadius 10 -ftpwSigmaColor 3 -ftpwSigmaAlbedo 0.07 -ftpwSigmaDistance 0.5 -ftpwst 20 -ftpwi 120"

     #if len(layer.split("decor")) > 1:
     #     if len(layer.split("front")) > 1:
     #          defilter = "-nf 11 -ncores -1 -oPostfix _filtered -runMode multiple -runBlock 5 -fmode STPW -exrlayers standard -ffkernel 2 -ffgain 5 -ffgamma 0.5 -ffsigma 7 -ffRefractionStrange 0.001 -ffIndirectSpecularStrange 0.0015 -fsw 1 -fse 1 -fsFallof 1000 -fsKernel 3 -fsRadius 2 -fsSigmaColor 3 -fsSigmaAlbedo 0.4 -fsSigmaNormal 0.76 -fsSigmaDepth 1000 -fstSigmaColor 0.6 -fstSigmaAlbedo 0.3 -fstSigmaNormal 0.45 -fstSigmaDepth 5 -fsSpecularStrength 1 -fsad 1 -fsfw 1 -fsfFallof 1000 -fsfKernel 0 -fsfRadius 7 -fsfSigmaColor 0.07 -fsfSigmaAlbedo 0.2 -fsfSigmaNormal 0.2 -fsfSigmaDepth 1000 -fsfSpecularStrength 1 -fsfad 1 -ftw 1 -ftFallof 0.01 -ftKernel 3 -ftbs 16 -ftISize 2 -ftSigmaColor 3 -ftSigmaAlbedo 0.08 -ftmt 6 -ftct 0.0017 -ftpww 1 -ftpwFallof 0.01 -ftpwKernel 3 -ftpwSRadius 10 -ftpwSigmaColor 3 -ftpwSigmaAlbedo 0.07 -ftpwSigmaDistance 1.5 -ftpwst 20 -ftpwi 120"
     #if len(layer.split("middle")) > 1:
     #     defilter = "-nf 11 -ncores -1 -oPostfix _filtered -runMode multiple -runBlock 5 -fmode STPW -exrlayers standard -ffkernel 2 -ffgain 5 -ffgamma 0.5 -ffsigma 7 -ffrefractionStrange 0.001 -ffIndirectSpecularStrange 0.0015 -fsw 1 -fse 1 -fsFallof 1000 -fsKernel 3 -fsRadius 2 -fsSigmaColor 3 -fsSigmaAlbedo 0.4 -fsSigmaNormal 0.76 -fsSigmaDepth 1000 -fstSigmaColor 0.6 -fstSigmaAlbedo 0.3 -fstSigmaNormal 0.45 -fstSigmaDepth 5 -fsSpecularStrength 1 -fsad 1 -fsfw 1 -fsfFallof 1000 -fsfKernel 0 -fsfRadius 7 -fsfSigmaColor 0.07 -fsfSigmaAlbedo 0.2 -fsfSigmaNormal 0.2 -fsfSigmaDepth 1000 -fsfSpecularStrength 1 -fsfad 1 -ftw 1 -ftFallof 0.01 -ftKernel 3 -ftbs 16 -ftISize 2 -ftSigmaColor 3 -ftSigmaAlbedo 0.08 -ftmt 6 -ftct 0.0017 -ftpww 1 -ftpwFallof 0.01 -ftpwKernel 3 -ftpwSRadius 10 -ftpwSigmaColor 3 -ftpwSigmaAlbedo 0.07 -ftpwSigmaDistance 1.5 -ftpwst 20 -ftpwi 120"
     #if len(layer.split("back")) > 1:
     #     defilter = "-nf 11 -ncores -1 -oPostfix _filtered -runMode multiple -runBlock 5 -fmode STPW -exrlayers standard -ffkernel 2 -ffgain 5 -ffgamma 0.5 -ffsigma 7 -ffRefractionStrange 0.001 -ffIndirectSpecularStrange 0.0015 -fsw 1 -fse 1 -fsFallof 1000 -fsKernel 3 -fsRadius 2 -fsSigmaColor 5 -fsSigmaAlbedo 0.4 -fsSigmaNormal 0.76 -fsSigmaDepth 1000 -fstSigmaColor 0.7 -fstSigmaAlbedo 0.3 -fstSigmaNormal 0.45 -fstSigmaDepth 5 -fsSpecularStrength 1 -fsad 1 -fsfw 1 -fsfFallof 1000 -fsfKernel 0 -fsfRadius 7 -fsfSigmaColor 0.1 -fsfSigmaAlbedo 0.2 -fsfSigmaNormal 0.2 -fsfSigmaDepth 1000 -fsfSpecularStrength 1 -fsfad 1 -ftw 1 -ftFallof 0.01 -ftKernel 3 -ftbs 16 -ftISize 2 -ftSigmaColor 5 -ftSigmaAlbedo 0.08 -ftmt 6 -ftct 0.0017 -ftpww 1 -ftpwFallof 0.01 -ftpwKernel 3 -ftpwSRadius 10 -ftpwSigmaColor 5 -ftpwSigmaAlbedo 0.07 -ftpwSigmaDistance 5 -ftpwst 20 -ftpwi 120"
     #defilter = filterPath + "denoise4kernel_9_16.8_5.filter.json"
     #if cmds.getAttr("renderManRISGlobals.rman__riopt__Hider_maxsamples") == 512 :
     #     defilter = filterPath + "denoise4kernel_9_16.1_1.filter.json"
     #if cmds.getAttr("renderManRISGlobals.rman__riopt__Hider_maxsamples") == 256 :
     #     defilter = filterPath + "denoise4kernel_9_16.5_3.filter.json"
     #if cmds.getAttr("renderManRISGlobals.rman__riopt__Hider_maxsamples") == 128 :
     #     defilter = filterPath + "denoise4kernel_9_16.8_5.filter.json"
          
     return defilter

def denoiser_info(message):
     cmds.confirmDialog(title= "Ginzburg Denoiser", message = message, button =['OK'])


def get_render_camera():
     cams = cmds.ls( cameras=True)
     rcam = ''
     for i in cams:
          if cmds.getAttr(i+".renderable") == 1:
               rcam = i.replace(':','_')
     return rcam;

def set_dnoiser_to_layer(layer,mode):
     outPath = ''+mel.eval('rman getvar rfmImages;')+'/${LAYER}/$STAGE${JOBSTYLE}'
     denoiseAdditionalPasses = ''
     if layer != '':
          try:
               cmds.editRenderLayerGlobals( currentRenderLayer=layer )
          except:
               pass
     Denoisefilter = get_denoise_filter(layer)
     try:
          cmds.setAttr("renderManRISGlobals.rman__riopt__Hider_pixelfiltermode","weighted",type = "string")
     except:
          print("pixelfiltermode wasn't set to "+layer)
     try:
          mel.eval('editRenderLayerAdjustment rmanDenoiseCrossFramePass.rman__torattr___passCommand;')
     except:
          print("Denoiser wasn't set to "+layer)

     if len(layer.split("volume")) > 1:
          denoiseAdditionalPasses = " -bc" + outPath+"_variance.####.exr"
     else:
          denoiseAdditionalPasses = " -bc" + outPath+"_variance.####.exr"
          denoiseAdditionalPasses += " -ac" + outPath + "_albedo.####.exr"
          denoiseAdditionalPasses += " -pc" + outPath + "_pw.####.exr"
          denoiseAdditionalPasses += " -nc" + outPath + "_nw.####.exr"
          denoiseAdditionalPasses += " -dc" + outPath + "_z.####.exr"
          denoiseAdditionalPasses += " --DiffuseChannel" + outPath+"_diffuse.####.exr"
          denoiseAdditionalPasses += " --SpecularChannel" + outPath+"_specular.####.exr"
          denoiseAdditionalPasses += " --IndirectDiffuseChannel" + outPath+"_indirectdiffuse.####.exr"
          denoiseAdditionalPasses += " --IndirectSpecularChannel" + outPath+"_indirectspecular.####.exr"
          denoiseAdditionalPasses += " --RefractionChannel" + outPath+"_refraction.####.exr"
     denoiserMainCommand = ''
     denoiserMainCommand = "//server/pixar/denoise/ginzburg_denoiser_linux -s " + str(int(cmds.getAttr("defaultRenderGlobals.startFrame"))) + " -e " + str(int(cmds.getAttr("defaultRenderGlobals.endFrame")))
     denoiserMainCommand += " " + denoiseAdditionalPasses
     #if mode == "allchannels":
     #    DenoiseCommand = "denoise "+crossframe+" -f "+Denoisefilter+outPath+"_variance."+frames+".exr"+DenoiseAdditionalPasses;
     #if mode == "onechannel":
     #   DenoiseCommand = "denoise --crossframe -v variance -f "+Denoisefilter+outPath+"_variance."+frames+".exr";
     #if mode == "none":
     #    DenoiseCommand = "";
     #denoiseCommand = '';
     if len(layer.split("mask")) > 1:
          denoiserMainCommand = ''; 
     mel.eval('rmanGetDefaultPass "rmanDenoiseCrossFramePass";');
     cmds.setAttr("rmanDenoiseCrossFramePass.rman__torattr___passCommand",denoiserMainCommand,type = "string");

def denoise_render():
     denoisePassCheck = len(cmds.ls('rmanDenoiseCrossFramePass'))
     if denoisePassCheck == 0:
          mel.eval('rmanCreatePass("DenoiseCrossFrame");')
     currentRLayer = cmds.editRenderLayerGlobals( query=True, currentRenderLayer=True )
     camChDenoise = get_render_camera()+"_rmanDenoiseCrossFramePass"
     camChFinal = get_render_camera()+"_Final"
     cmds.setAttr("defaultRenderGlobals.animation",1)
     cmds.setAttr("renderManRISGlobals.rman__torattr___denoise",0)
     mel.eval('rmanSetComputeBehavior "rmanDenoiseCrossFramePass" 1;')
     mel.eval('rmanSetComputeBehavior "rmanFinalGlobals" 1;')
     mel.eval('rmanSetComputeBehavior "'+camChFinal+'" 1')
     mel.eval('rmanSetComputeBehavior "'+camChDenoise+'" 1')
     mel.eval('rmanGetDefaultPass "rmanDenoiseCrossFramePass";')
     k = 0
     for i in range(0,len(cmds.ls(type = "renderLayer"))):
          if len(cmds.ls(type = "renderLayer")[i].split(":")) == 1:
               if len(cmds.ls(type = "renderLayer")[i].split("defaultRenderLayer")) == 1:
                    if cmds.ls(type = "renderLayer")[i] != "defaultRenderLayer":
                         if len(cmds.ls(type = "renderLayer")[i].split("mask")) > 1:
                              mel.eval('rmanSetComputeBehavior "rmanDenoiseCrossFramePass" 1;')
                              mel.eval('rmanSetComputeBehavior "rmanFinalGlobals" 1;')
                              mel.eval('rmanSetComputeBehavior "'+camChFinal+'" 1')
                              mel.eval('rmanSetComputeBehavior "'+camChDenoise+'" 1')
                              set_dnoiser_to_layer(cmds.ls(type = "renderLayer")[i],"none")
                              k += 1;
                         else:
                              mel.eval('rmanSetComputeBehavior "rmanDenoiseCrossFramePass" 1;')
                              mel.eval('rmanSetComputeBehavior "rmanFinalGlobals" 1;')
                              mel.eval('rmanSetComputeBehavior "'+camChFinal+'" 1')
                              mel.eval('rmanSetComputeBehavior "'+camChDenoise+'" 1')
                              set_dnoiser_to_layer(cmds.ls(type = "renderLayer")[i],"allchannels")
                              k += 1
                         if k == 0:
                              set_dnoiser_to_layer("","allchannels")
                         try:
                              cmds.editRenderLayerGlobals( currentRenderLayer=currentRLayer)
                              disable_rgba_chanel()
                              delete_rman_tx()
                         except:
                              pass

def mblur_state(state):
     k = 0
     for i in range(0,len(cmds.ls(type = "renderLayer"))):
          if len(cmds.ls(type = "renderLayer")[i].split(":")) == 1:
               if len(cmds.ls(type = "renderLayer")[i].split("defaultRenderLayer")) == 1:
                    if cmds.ls(type = "renderLayer")[i] != "defaultRenderLayer":
                         try:
                              cmds.editRenderLayerGlobals( currentRenderLayer=cmds.ls(type = "renderLayer")[i])
                         except:
                              pass
                         if state == 'true':
                              cmds.setAttr("renderManRISGlobals.rman__torattr___motionBlur",1)
                              cmds.setAttr("renderManRISGlobals.rman__torattr___cameraBlur",1)       
                              k += 1
                         else:
                              cmds.setAttr("renderManRISGlobals.rman__torattr___motionBlur",0)
                              cmds.setAttr("renderManRISGlobals.rman__torattr___cameraBlur",0)
                              k += 1
                         if k == 0:
                              if state == 'true':
                                   cmds.setAttr("renderManRISGlobals.rman__torattr___motionBlur",1)
                                   cmds.setAttr("renderManRISGlobals.rman__torattr___cameraBlur",1)
                              else:
                                   cmds.setAttr("renderManRISGlobals.rman__torattr___motionBlur",0)
                                   cmds.setAttr("renderManRISGlobals.rman__torattr___cameraBlur",0)

def denoise_off():
     camChDenoise = get_render_camera()+"_rmanDenoiseCrossFramePass"
     camChFinal = get_render_camera()+"_Final"
     currentRLayer = cmds.editRenderLayerGlobals( query=True, currentRenderLayer=True )
     mel.eval('rmanSetComputeBehavior "rmanDenoiseCrossFramePass" 0;')
     mel.eval('rmanSetComputeBehavior "rmanFinalGlobals" 1;')
     mel.eval('rmanSetComputeBehavior "'+camChFinal+'" 1')
     mel.eval('rmanSetComputeBehavior "'+camChDenoise+'" 1')

     for i in range(0,len(cmds.ls(type = "renderLayer"))):
          if len(cmds.ls(type = "renderLayer")[i].split(":")) == 1:
               if len(cmds.ls(type = "renderLayer")[i].split("defaultRenderLayer")) == 1:
                    if cmds.ls(type = "renderLayer")[i] != "defaultRenderLayer":
                         mel.eval('rmanSetComputeBehavior "rmanDenoiseCrossFramePass" 0;')
                         mel.eval('rmanSetComputeBehavior "rmanFinalGlobals" 1;')
                         mel.eval('rmanSetComputeBehavior "'+camChFinal+'" 1')
                         mel.eval('rmanSetComputeBehavior "'+camChDenoise+'" 1')
     cmds.setAttr("defaultRenderGlobals.animation",1)
     cmds.setAttr("renderManRISGlobals.rman__torattr___denoise",0)
     cmds.editRenderLayerGlobals( currentRenderLayer=currentRLayer)
     try:
          disable_rgba_chanel()
          delete_rman_tx()
     except:
          pass

def denoise_only():
     frameStore__ = []
     currentRLayer = cmds.editRenderLayerGlobals( query=True, currentRenderLayer=True )
     mblur_state('false')
     camChDenoise = get_render_camera()+"_rmanDenoiseCrossFramePass"
     camChFinal = get_render_camera()+"_Final"
     cmds.setAttr("defaultRenderGlobals.animation",0)
     cmds.setAttr("renderManRISGlobals.rman__torattr___denoise",0)
     mel.eval('rmanSetComputeBehavior "rmanDenoiseCrossFramePass" 1;')
     mel.eval('rmanSetComputeBehavior "rmanFinalGlobals" 0;')
     mel.eval('rmanSetComputeBehavior "'+camChFinal+'" 1')
     mel.eval('rmanSetComputeBehavior "'+camChDenoise+'" 1')
     mel.eval('rmanGetDefaultPass "rmanDenoiseCrossFramePass";')
     k = 0
     for i in range(0,len(cmds.ls(type = "renderLayer"))):
          if len(cmds.ls(type = "renderLayer")[i].split(":")) == 1:
               if len(cmds.ls(type = "renderLayer")[i].split("defaultRenderLayer")) == 1:
                    if cmds.ls(type = "renderLayer")[i] != "defaultRenderLayer":
                         if len(cmds.ls(type = "renderLayer")[i].split("mask")) > 1:
                              mel.eval('rmanSetComputeBehavior "rmanDenoiseCrossFramePass" 1;')
                              mel.eval('rmanSetComputeBehavior "rmanFinalGlobals" 0;')
                              mel.eval('rmanSetComputeBehavior "'+camChFinal+'" 1')
                              mel.eval('rmanSetComputeBehavior "'+camChDenoise+'" 1')
                              set_dnoiser_to_layer(cmds.ls(type = "renderLayer")[i],"none")
                              k += 1
                         else:
                              mel.eval('rmanSetComputeBehavior "rmanDenoiseCrossFramePass" 1;')
                              mel.eval('rmanSetComputeBehavior "rmanFinalGlobals" 0;')
                              mel.eval('rmanSetComputeBehavior "'+camChFinal+'" 1')
                              mel.eval('rmanSetComputeBehavior "'+camChDenoise+'" 1')
                              set_dnoiser_to_layer(cmds.ls(type = "renderLayer")[i],"allchannels"); 
                              k += 1
     if k == 0:
          set_dnoiser_to_layer("","allchannels")
     try:
          cmds.editRenderLayerGlobals( currentRenderLayer=currentRLayer)
          disable_rgba_chanel()
          delete_rman_tx()
     except:
          pass
     return frameStore__

def delete_rman_tx():
     try: 
          mel.eval('select -r rmanTxMakeGlobals ;')
     except:
          pass