#!/usr/bin/python

"""
Gui plugin
"""
# System imports
import os
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
        self.editorGui.Show()
        
        ## EVENTS ##
        
        

    
    def start(self):
        
        pass
        
    def stop(self):
        
        pass

