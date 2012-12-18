#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Documentation: LevelData.py
  Classes and functions:
    N.A.
  Description:
    This modul stores all the data which is
    needed to present a level of the game.
"""

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""
PICK_TAG = 'pickable'
class LevelData:
    """The level Data class stores all available information
    about a level in the game"""

    def __init__(self, _base):
        """initialise the base variables"""
        
        self.base = _base
        
        # General informations
        self.author = ""
        self.date = ""
        self.levelID = ""
        self.name = ""

        # Base model
        self.model = None

        # Collision Models
        self.colModel = None
        # geometry for walls and ground
        self.groundGeom = None
        self.wallGeom = None
        # the collideable objects in the model
        self.colWall = None
        self.colGround = None

        # Physics management of this level
        self.levelPhysics = None

        # Player specific things
        self.playerStartPos = (0, 0, 0)
        self.playerStartHpr = (0, 0, 0)

        # Objects
        self.objects = []

        # Items
        self.items = []

        # Lights
        self.lights = []

        # AI units
        self.aiUnits = []

        # Sensors
        self.sensors = []

    def generate(self):
        """The Generate function will load all the level data
        and reparent it to the base renderer, so the level shows up"""
        # load the lights
        for light in self.lights:
            self.model.setLight(light)
            if __debug__:
                lmodel = loader.loadModel("models/misc/Pointlight")
                lmodel.setPos(light.getPos())
                lmodel.reparentTo(self.model)

        if __debug__ :
            startposmodel = loader.loadModel("models/zup-axis")
            startposmodel.setPos(self.playerStartPos)
            startposmodel.reparentTo(self.model)
            startposmodel.setScale(0.2)
        # reparent the level model to the base renderer,
        # so it will be displayed
        
        objects = self.model.findAllMatches('**')
        for obj in objects:
            print obj
            obj.setTag( PICK_TAG, '1' )
        print self.model
        self.model.reparentTo(self.base.base.gizmo.rootNp)

    def cleanup(self):
        """Remove all models and other level data entirely"""

        if self.model != None:
            for light in self.lights:
                self.model.clearLight(light)
            self.model.removeNode()
            self.model = None

        if self.colModel != None:
            self.colModel.removeNode()
            self.colModel = None

        if self.colGround != None:
            self.colGround.removeNode()
            self.colGround = None

        if self.colWall != None:
            self.colWall.removeNode()
            self.colWall = None

        for i in range(len(self.sensors)):
            self.sensors[i].cleanup()
            self.sensors[i].deactivateSensor()

        self.groundGeom = None
        self.wallGeom = None

        # clear all lists of objects lights and units
        self.objects = []
        self.items = []
        self.lights = []
        self.aiUnits = []
        self.sensors = []
