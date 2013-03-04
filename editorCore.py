#!/usr/bin/python

#----------------------------------------------------------------------#
"""
Editor Core.
Mainly routing and forwarding functions, like the main control centre.

"""

# System imports
import sys
import os
import logging

# Panda Engine imports
from direct.showbase.DirectObject import DirectObject

# Extra imports
from events import Events

#----------------------------------------------------------------------#

### EDITOR CORE ###

class EditorCore(DirectObject):
    
    
    def __init__(self, _base):
        
        self.base = _base
        
        # Node holder
        self.RenderNodes = {}
        self.RenderNodes['master'] = render.attachNewNode('master_renderNodes')
        
        # Visible Node holder
        self.RenderNodes['visible'] = self.RenderNodes['master'].attachNewNode('visible_renderNodes')
        
        # Hidden Node holder
        self.RenderNodes['hidden'] = self.RenderNodes['master'].attachNewNode('hidden_renderNodes')
        
        self.guiInterface = None
        
        # 
        self.Events = Events(self)
        
        self.eventHandler = {
            "new-level"         : self.Events.newLevel,
            "open-level"        : self.Events.openLevel,
            "save-level"        : self.Events.saveLevel,
            "exit-event"        : self.Events.exitEvent,
            "move-gizmo"        : self.Events.moveGizmo,
            "rotate-gizmo"      : self.Events.rotateGizmo,
            "scale-gizmo"       : self.Events.scaleGizmo
        
        }
        
        # Accept events
        for eventname in self.eventHandler.keys():
            
            self.accept(eventname, self.eventHandler[eventname])
    
    def start(self):
        
        pass
        
        
    def stop(self):
        pass
      
