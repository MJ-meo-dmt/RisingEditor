#!/usr/bin/python

"""
Gui plugin
"""
# System imports
import logging
# Panda imports
from panda3d.rocket import RocketRegion, RocketInputHandler, LoadFontFace


########################################################################

class Plugin():

    def __init__(self):

        self.temp = "Helloooo From GuiCore"

        ## LOAD: Font
        LoadFontFace("plugins/pluginData/gui/fonts/verdana.ttf")

        ## SETUP REGION & INPUT HANDLER ##
        rw = RocketRegion.make('pandaRocket', base.win)
        rw.setActive(1)
        ih = RocketInputHandler()
        base.mouseWatcher.attachNewNode(ih)
        rw.setInputHandler(ih)

        ## CONTEXT ##
        self.context = rw.getContext()

        ## SETUP MAIN EDITOR WINDOW & GUI ##
        self.editorGui = self.context.LoadDocument('plugins/pluginData/gui/editor_main.rml')

        ## EVENTS ##


    def start(self):
        logging.info("Start GUI core Plugin")
        self.editorGui.Show()

    def stop(self):
        logging.info("Stop GUI core Plugin")
        self.editorGui.Hide()

