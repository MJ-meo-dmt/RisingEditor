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
from pandac.PandaModules import *
from panda3d.core import *
from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenText import OnscreenText 

from panda3d.rocket import *
from panda3d.bullet import *

# Main imports

# From Editor core
from pluginManager import *

# Configs
from editorCfg import *

#----------------------------------------------------------------------#

### MAIN CLASS ###

class Main(ShowBase):


    def __init__(self):
        
        # Create Log file
        logging.basicConfig(filename='editor.log', level=logging.DEBUG)
        
        ShowBase.__init__(self)
        
        ## Start: Editor
        
        ## Start: PluginMgr & Plugins ##
        self.PluginMgr = PluginMgr()
        
        sys.path.extend(PLUGIN_DIR.split(os.pathsep))
        print "Current System Path: %s" % (sys.path)
        
        logging.info('Attempting to load plugins')
        self.PluginMgr.importPlugins(PLUGIN_DIR, globals())
        



# Goooo Panda...
app = Main()
app.run()






















