#!/usr/bin/python

#----------------------------------------------------------------------#
"""
Events Handler

"""

# System imports
import sys
import os
import logging

# Panda Engine imports

# Extra imports
from editorCfg import *
 

#----------------------------------------------------------------------#

### Events Handler ###

class Events():
    
    
    def __init__(self, _base):
        
        self.EditorCore = _base 
        
    def newLevel(self):
        print "new-level"
        print self.EditorCore.base.PluginMgr.Plugin[GUI_PLUGIN_NAME].temp
        
    def openLevel(self):
        print "open-level"
        
    def saveLevel(self):
        print "save-level"
        
    # Exit Editor
    def exitEvent(self):
        print "exit-event"
    
    def moveGizmo(self):
        print "move-gizmo" 
        
    def rotateGizmo(self):
        print "rotate-gizmo"
        
    def scaleGizmo(self):
        print "scale-gizmo"
        
        
