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
from pandac.PandaModules import *
from panda3d.core import *
from panda3d.bullet import *

# Extra imports
from events import Events
from levelLoader.LevelLoader import LevelLoader
#----------------------------------------------------------------------#

### EDITOR CORE ###

class EditorCore(DirectObject):
    
    
    def __init__(self, _base):
        
        self.base = _base
        
        # Setup Physics World for editor
        # World
        self.bulletWorld = BulletWorld()
        self.bulletWorld.setGravity(Vec3(0, 0, -8.9))
    
        # Node holder
        self.RenderNodes = {}
        self.RenderNodes['master'] = render.attachNewNode('master_renderNodes')
        
        self.ObjectNodes = {}
        
        # Visible Node holder
        self.RenderNodes['visible'] = self.RenderNodes['master'].attachNewNode('visible_renderNodes')
        
        # Hidden Node holder
        self.RenderNodes['hidden'] = self.RenderNodes['master'].attachNewNode('hidden_renderNodes')
        
        
        # Mouse click 
        self.accept('mouse1', self.doSelect)
        
        # Picker settings
        self.selected_object = None
        
        # Load temp model file
        self.levelload = LevelLoader(self)
        self.levelload.read("tempModels/jump.lvlml", False)
        self.levelload.run()
                
        
        self.guiInterface = None
        
        # Start event mgr
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
        
        
    
    def doSelect(self):
        selected = self.ray()
        if selected != None:
            self.selected_object = selected
            if self.selected_object.getTag('pickable') == True:
                print selected 
                # now add it to a selection node or something i guess
        else:
            pass
        
        
    def ray(self):
        
        selected_object = None
        
        if base.mouseWatcherNode.hasMouse():
            
            posMouse = base.mouseWatcherNode.getMouse()
            pFrom = Point3()
            pTo = Point3()
            base.camLens.extrude(posMouse, pFrom, pTo)
        
            pFrom = render.getRelativePoint(base.cam, pFrom)
            pTo = render.getRelativePoint(base.cam, pTo)
            
            result = self.bulletWorld.rayTestClosest(pFrom, pTo)
            
            objNode = result.getNode()
            print objNode

            selected_object = objNode
            
        return selected_object 
        
        
    def buildCollisionNodes(self, obj):
        
        tmpMesh = BulletTriangleMesh()
        node = obj.node()
        if node.isGeomNode():
            #TODO: Check is collision with node????
            tmpMesh.addGeom(node.getGeom(0))
        else:
            print "Not geom node"#tmpMesh.addGeom(self.__getGeomFromCollision(node))
        #sensorMeshes.append(tmpMesh)
        ghost = BulletGhostNode("test")
        ghost.addShape(BulletTriangleMeshShape(tmpMesh, dynamic=False))
        #self.RenderNodes['visible'][i].modelGeom = render.attachNewNode(ghost)
        #self.level.sensors[i].modelGeom.setCollideMask(BitMask32(0x0f))
        self.bulletWorld.attachGhost(ghost)
