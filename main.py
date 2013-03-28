#!/usr/bin/python

#----------------------------------------------------------------------#
"""
Main Program class

This runs everything, this Main class could be replaced by any other
main program class so that the editor could be integrated.
"""

# System imports
import sys
import os
import logging

# Panda Engine imports
from pandac.PandaModules import loadPrcFileData
loadPrcFileData("",
"""
    window-title Editor
    fullscreen 0
    win-size 1024 768
    cursor-hidden 0
    sync-video 0
    show-frame-rate-meter 1
"""
)

from direct.showbase.ShowBase import ShowBase

# Main imports
from pluginManager import PluginMgr

# From Editor core
from base.editorCore import EditorCore

# Configs
from editorCfg import PLUGIN_DIR

#----------------------------------------------------------------------#

### MAIN CLASS ###
class Main(ShowBase):
    def __init__(self):

        # Create Log file
        logging.basicConfig(
            filename="editor.log",
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s: %(message)s",
            datefmt="%d-%m-%Y %H:%M:%S")

        ShowBase.__init__(self)

        ## Load: EditorCore
        self.EditorCore = EditorCore(self)

        ## Start: PluginMgr & Plugins ##
        self.PluginMgr = PluginMgr()

        sys.path.extend(PLUGIN_DIR.split(os.pathsep))
        #print "Current System Path: %s" % (sys.path)

        logging.info('Attempting to load plugins')
        # Start importing plugins
        self.PluginMgr.importPlugins(PLUGIN_DIR, globals())

        ## Start: EditorCore
        self.EditorCore.start()


# Goooo Panda...
app = Main()
app.run()






















