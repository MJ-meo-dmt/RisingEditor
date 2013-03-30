#!/usr/bin/python

#----------------------------------------------------------------------#
"""
Editor Core.
Mainly routing and forwarding functions, like the main control centre.

"""

# System imports
import logging

# Panda Engine imports
from direct.showbase.DirectObject import DirectObject
from panda3d.core import Vec3, Vec4, BitMask32
from panda3d.core import Geom, GeomTriangles
from panda3d.core import GeomVertexData, GeomVertexWriter, GeomVertexFormat
from panda3d.bullet import BulletWorld, BulletDebugNode, BulletGhostNode
from panda3d.bullet import BulletTriangleMesh, BulletTriangleMeshShape

# Extra imports
from events import Events
from levelLoader.LevelLoader import LevelLoader
from base.mouseHandler import MouseHandler
#----------------------------------------------------------------------#

### EDITOR CORE ###

class EditorCore(DirectObject):

    def __init__(self, _base):
        self.base = _base

        # Setup Physics World for editor
        # World
        self.bulletWorld = BulletWorld()
        self.bulletWorld.setGravity(Vec3(0, 0, -8.9))

        self.base.taskMgr.add(self.update, 'update')

        #### DEBUG BULLET ####
        debugNode = BulletDebugNode('Debug')
        debugNode.showWireframe(True)
        debugNode.showConstraints(True)
        debugNode.showBoundingBoxes(False)
        debugNode.showNormals(False)
        debugNP = self.base.render.attachNewNode(debugNode)
        #debugNP.show()

        self.bulletWorld.setDebugNode(debugNP.node())

        ######################

        # Node holder
        self.RenderNodes = {}
        self.RenderNodes['master'] = self.base.render. \
                                     attachNewNode('master_renderNodes')

        self.ObjectNodes = {}
        # Bullet Ghost Nodes
        self.ghostNodes = {}

        # Visible Node holder
        self.RenderNodes['visible'] = self.RenderNodes['master']. \
                                      attachNewNode('visible_renderNodes')

        # Hidden Node holder
        self.RenderNodes['hidden'] = self.RenderNodes['master']. \
                                     attachNewNode('hidden_renderNodes')

        # Mouse handling
        self.mouseHandler = MouseHandler(self.bulletWorld)

        # Picker settings
        self.selectedObjects = []

        # Load temp model file
        self.levelload = LevelLoader(self)
        self.levelload.read("tempModels/jump.lvlml", False)
        self.levelload.run()


        self.guiInterface = None

        # Start event mgr
        self.Events = Events(self)

        self.eventHandler = {
            "new-level": self.Events.newLevel,
            "open-level": self.Events.openLevel,
            "save-level": self.Events.saveLevel,
            "exit-event": self.Events.exitEvent,
            "move-gizmo": self.Events.moveGizmo,
            "rotate-gizmo": self.Events.rotateGizmo,
            "scale-gizmo": self.Events.scaleGizmo,
            "mouse-in-rocket-region": self.Events.mouseInRocketRegion,
            "mouse-out-rocket-region": self.Events.mouseOutRocketRegion
        }

        # Accept events
        for eventname in self.eventHandler.keys():
            self.accept(eventname, self.eventHandler[eventname])

    def start(self):
        logging.debug("start editor core")
        self.base.PluginMgr.start()
        self.editorMouseStart()

    def stop(self):
        logging.debug("stop editor core")
        self.base.PluginMgr.stop()
        self.editorMouseStop()

    def editorMouseStart(self):
        self.mouseHandler.start(self.doSelect)

    def editorMouseStop(self):
        self.mouseHandler.stop()

    def doSelect(self, multiSelect):
        selected = self.mouseHandler.rayCheck()
        lastSelections = []
        # clear previous selection
        if len(self.selectedObjects) > 0:
            lastSelections = self.selectedObjects
            if not multiSelect:
                # deselect all objects, so at the end only the
                # current selected object will be marked
                for i in range(len(self.selectedObjects)):
                    self.selectedObjects[i].clearColorScale()
                self.selectedObjects = []

        if selected != None:
            # check which object is selected
            for ghost, obj in self.ghostNodes.items():
                if ghost == selected:
                    # check if the object is or is not in the selection list
                    if not obj in lastSelections:
                        # object is not in the list, select the object
                        if obj.getTag('pickable') == "True":
                            obj.setColorScale(Vec4(0.3, 0.7, 1, 1))
                        self.selectedObjects.append(obj)
                    # as all objects get deselected in singleSelect mode,
                    # just deselect here in multiSelect mode
                    elif multiSelect:
                        # object is in already in the list, deselect the object
                        obj.clearColorScale()
                        self.selectedObjects.remove(obj)
                    # We can only de-/select one object at a time at the
                    # moment, so leave the loop here
                    break

    def buildCollisionNodes(self, obj):
        tmpMesh = BulletTriangleMesh()
        node = obj.node()
        if node.isGeomNode():
            tmpMesh.addGeom(node.getGeom(0))
        elif node.isCollisionNode():
            #tmpMesh.addGeom(self.__getGeomFromCollision(node))
            return
        else:
            return

        ghost = BulletGhostNode(str(obj))
        ghost.addShape(BulletTriangleMeshShape(tmpMesh, dynamic=False))
        ghostNP = self.base.render.attachNewNode(ghost)
        ghostNP.reparentTo(obj)
        self.ghostNodes[ghost] = obj
        obj.setCollideMask(BitMask32(0x0f))
        self.bulletWorld.attachGhost(ghost)


    def update(self, task):
        """Bullet Physic update task"""
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
