#!/usr/bin/python

"""
Object transformation plugin
"""
# System imports
import logging
# Panda imports
from direct.showbase.DirectObject import DirectObject

from transformTools import move
from transformTools import scale
from transformTools import rotate

########################################################################

class Plugin(DirectObject):

    def __init__(self):
        print "init"
        logging.debug("Init Transformation core")

        self.transformTools = {
            "move": move,
            "scale": scale,
            "rotate": rotate
            }
        self.activeTransformTool = ""

    def start(self):
        print "start"
        logging.info("Start transform core Plugin")
        self.accept("startTransformObject", self.startTransform)
        self.accept("stopTransformObject", self.stopTransform)

    def stop(self):
        print "stop"
        logging.info("Stop transform core Plugin")
        self.ignore("startTransformObject")
        self.ignore("stopTransformObject")

    def startTransform(self, object, transformTool):
        logging.debug("transform %s with %s" % (object, transformTool))
        if transformTool in self.transformTools:
            self.transformTools[transformTool].startTransform(object)
            self.activeTransformTool = transformTool

    def stopTransform(self):
        logging.debug("stop last transformation")
        if self.activeTransformTool != "":
            self.transformTools[self.activeTransformTool].stopTransform()
