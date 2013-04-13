#!/usr/bin/python

#----------------------------------------------------------------------#
"""
Events Handler

"""

# System imports
import sys
import logging

# Panda Engine imports

# Extra imports
from editorCfg import GUI_PLUGIN_NAME


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
        logging.info("quit editor")
        print "exit-event"
        self.EditorCore.stop()
        # finally quit the application
        self.EditorCore.base.shutdown()
        sys.exit(0)

    def moveObject(self):
        print "move-object"
        if len(self.EditorCore.selectedObjects) > 0:
            base.messenger.send(
                "startTransformObject",
                [self.EditorCore.selectedObjects[0],
                "move"])

    def rotateObject(self):
        print "rotate-object"
        if len(self.EditorCore.selectedObjects) > 0:
            base.messenger.send(
                "startTransformObject",
                [self.EditorCore.selectedObjects[0],
                "rotate"])

    def scaleObject(self):
        print "scale-object"
        if len(self.EditorCore.selectedObjects) > 0:
            base.messenger.send(
                "startTransformObject",
                [self.EditorCore.selectedObjects[0],
                "scale"])

    def mouseInRocketRegion(self):
        self.EditorCore.editorMouseStop()

    def mouseOutRocketRegion(self):
        self.EditorCore.editorMouseStart()
