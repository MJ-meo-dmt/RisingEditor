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


        taskMgr.add(self.update, 'update')

        #### DEBUG BULLET ####
        debugNode = BulletDebugNode('Debug')
        debugNode.showWireframe(True)
        debugNode.showConstraints(True)
        debugNode.showBoundingBoxes(False)
        debugNode.showNormals(False)
        debugNP = render.attachNewNode(debugNode)
        #debugNP.show()

        self.bulletWorld.setDebugNode(debugNP.node())

        ######################

        # Node holder
        self.RenderNodes = {}
        self.RenderNodes['master'] = render.attachNewNode('master_renderNodes')

        self.ObjectNodes = {}
        # Bullet Ghost Nodes
        self.ghostNodes = {}

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
            for ghost, obj in self.ghostNodes.items():
                if ghost == selected:
                    self.selected_object = obj

            if self.selected_object.getTag('pickable') == "True":

                #TODO: check if other objects need to be unselected

                self.selected_object.setColorScale(Vec4(0, 0.3, 1, 1))
                # now add it to a selection node or something i guess
        else:
            #TODO: unselect anything
            print "Nothing"
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
            #print objNode

            selected_object = objNode

        return selected_object


    def buildCollisionNodes(self, obj):
        tmpMesh = BulletTriangleMesh()
        node = obj.node()
        if node.isGeomNode():
            tmpMesh.addGeom(node.getGeom(0))
        elif node.isCollisionNode():
            return
            #tmpMesh.addGeom(self.__getGeomFromCollision(node))
        else:
            return

        ghost = BulletGhostNode(str(obj))
        ghost.addShape(BulletTriangleMeshShape(tmpMesh, dynamic=False))
        #self.RenderNodes['visible'][i].modelGeom = render.attachNewNode(ghost)
        ghostNP = render.attachNewNode(ghost)
        ghostNP.reparentTo(obj)
        self.ghostNodes[ghost] = obj
        obj.setCollideMask(BitMask32(0x0f))
        self.bulletWorld.attachGhost(ghost)


    def update(self, task):
        dt = globalClock.getDt()
        self.bulletWorld.doPhysics(dt, 10, 1.0/180.0)

        return task.cont


    def __getGeomFromCollision(self, node):
        """This function will extract the geom object out of the
        given collision node and return it"""

        # as we have a collision node we can note simply get the
        # geom model of it... at least I don't know a way to do
        # it now, so we get the vertices and create a new geom
        # out of them.

        # some variables needed to create a new geom out of
        # vertices
        vdata = GeomVertexData("colModelVData",
                               GeomVertexFormat.getV3(),
                               Geom.UHStatic)
        vertices = GeomVertexWriter(vdata, "vertex")
        prim = GeomTriangles(Geom.UHStatic)

        # now run through all solids and its vertex points
        i = 0
        for solid in node.getSolids():
            for point in solid.getPoints():
                vertices.addData3f(point)
                i += 1
            # dependend if we have a quad or triangle
            # we add the vertex points to our primitive
            if solid.getNumPoints() > 3:
                # TODO: FixMe Vertice data to Primitive (quads)
                # somethings is wrong with the numbering of the
                # vertex index. Generated Triangles don't collide

                # split a quad into two tris
                prim.addVertices(i - 1, i - 2, i - 4)
                prim.addVertices(i - 3, i - 2, i - 4)
            else:
                # add a triangle
                prim.addVertices(i - 2, i - 3, i - 1)

        # now we create the geom and add the primitive to it
        geom = Geom(vdata)
        geom.addPrimitive(prim)

        return geom
