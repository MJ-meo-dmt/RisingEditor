#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Documentation: LevelLoader.py
  Classes and functions:
    N.A.
  Description:
    This class can load the lvlml xml level files.
"""

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

import sys
import logging
from xml.etree import ElementTree
from LevelData import LevelData
from sensors.SensorClimbeable import SensorClimbeable
from sensors.SensorExit import SensorExit
from sensors.SensorMessage import SensorMessage
from sensors.SensorWallRun import SensorWallRun


from panda3d.core import PointLight
from panda3d.core import DirectionalLight
from panda3d.core import AmbientLight
from panda3d.core import Spotlight
from panda3d.core import NodePath
from panda3d.core import VBase4


class LevelLoader:
    def __init__(self, _base):

        self.EditorCore = _base

        self.leveldata = LevelData(self)
        self.levelPhysics = None

    def run(self):
        self.leveldata.generate()


    def read(self, levelFilename, isInsideMF=True):
        """This function reads the given level file and store the data for
        further use inside the self.levelPhysics and self.levelPhysics.level
        variables"""

        # use try except block for reading the xml file
        # if something happen, we simply return False to
        # indicate the loading failed
        try:
            if isInsideMF:
                # as we can't parse files which are inside multifiles,
                # we need to read them with the vfs and then parse the String
                from panda3d.core import VirtualFileSystem
                vfs = VirtualFileSystem.getGlobalPtr()
                lvlFile = vfs.readFile(levelFilename, False)
                levelTree = ElementTree.XML(lvlFile)
            else:
                lvlFile = levelFilename
                levelTree = ElementTree.parse(lvlFile)

            # read some basic informations of the level like
            # author name and creation date
            author = levelTree.find("author")
            if author != None:
                self.leveldata.author = author.text

            date = levelTree.find("date")
            if date != None:
                self.leveldata.date = date.text

            name = levelTree.find("name")
            if name != None:
                self.leveldata.name = name.text

            model = self.__readModel(levelTree.find("baseModel"))
            if model != None:
                self.leveldata.model = model
            else:
                # We have a problem with loading the base model
                #print model
                return False

            collision = levelTree.find("collisionModel")
            if collision != None:
                colModel = self.__readModel(levelTree.find("collisionModel"))
                if colModel != None:
                    self.leveldata.colModel = colModel

            walls = levelTree.find("wallCollision")
            if walls != None:
                colWall = self.__readCollisionModel(walls)
                if colWall != None:
                    self.leveldata.colWall = colWall

            colGround = self.__readCollisionModel(
                levelTree.find("groundCollision"))
            if colGround != None:
                self.leveldata.colGround = colGround

            wallRunSensor = SensorWallRun()
            wallRunSensor.sensorID = "wallrun"
            if self.leveldata.colWall != None:
                wallRunSensor.model = self.leveldata.colWall
            elif self.leveldata.colModel != None:
                wallRunSensor.model = self.leveldata.colModel
            elif self.leveldata.colGround != None:
                wallRunSensor.model = self.leveldata.colGround
            wallRunSensor.sensorType = "wallRuns"
            self.leveldata.sensors.append(wallRunSensor)

            startPos = levelTree.find("startPos")
            if startPos != None:
                pos = self.__readPos(startPos)
                self.leveldata.playerStartPos = pos
                hpr = self.__readHpr(startPos)
                self.leveldata.playerStartHpr = hpr

            if levelTree.find("exit") is not None:
                colExit = self.__readCollisionModel(levelTree.find("exit"))
                if colExit != None:
                    sensor = SensorExit()
                    sensor.sensorID = "exit"
                    sensor.model = colExit
                    sensor.sensorType = "exit"
                    self.leveldata.sensors.append(sensor)

            objects = levelTree.find("objects")
            if objects != None:
                self.__readObjects(objects)

            sensors = levelTree.find("sensors")
            if sensors != None:
                self.__readSensors(sensors)

            lights = levelTree.find("lights")
            if lights != None:
                self.__readLights(lights)

            aiUnits = levelTree.find("aiUnits")
            if aiUnits != None:
                self.__readAIUnits(aiUnits)

        except:
            logging.error("Error while loading level: %s %s",
                          levelFilename, sys.exc_info())
            return False

        return True

    def __readObjects(self, root):
        """Read the objects stored in the given root node"""
        for entry in list(root):
            newObject = None

            objType = entry.get("type", default="object").lower()
            if objType == "object":
                pass
            elif objType == "item":
                itemType = entry.find("type").text.lower()

                if itemType == "medikit":
                    newObject = ItemHealth()
                elif itemType == "staminarefill":
                    newObject = ItemStamina()

            elif objType == "collectible":
                pass

            if newObject != None:
                pos = self.__readPos(entry)
                newObject.model.setPos(pos)

                scale = self.__readScale(entry)
                newObject.model.setScale(scale)

            if objType == "item":
                self.leveldata.items.append(newObject)
            else:
                self.leveldata.objects.append(newObject)

    def __readSensors(self, root):
        for entry in list(root):
            objType = entry.get("type", default="object").lower()
            if objType == "ladder":
                sensor = SensorClimbeable()
                sensor.sensorID = entry.find("id").text
                sensor.model = self.__readCollisionModel(entry)
                sensor.sensorType = "ladder"
                self.leveldata.sensors.append(sensor)
            elif objType == "pipe":
                sensor = SensorClimbeable()
                sensor.sensorID = entry.find("id").text
                sensor.model = self.__readCollisionModel(entry)
                sensor.sensorType = "pipe"
                self.leveldata.sensors.append(sensor)
            elif objType == "hint":
                sensor = SensorMessage()
                sensor.sensorID = entry.find("id").text
                sensor.model = self.__readCollisionModel(entry)
                textEntry = entry.find("text")
                translateableEntry = entry.find("translateable")
                if textEntry != None:
                    sensor.message = textEntry.text
                if translateableEntry != None:
                    sensor.translated = eval(translateableEntry.text)
                sensor.setActOnCollide(True)
                sensor.sensorType = "hint"
                self.leveldata.sensors.append(sensor)


    def __readLights(self, root):
        lightCounter = 0
        for entry in list(root):
            # read in the type of the light
            lightType = entry.get("type", default="PointLight").lower()
            light = None
            if lightType == "pointlight":
                light = PointLight("Pnt_Light%03d" % lightCounter)
            elif lightType == "directionallight":
                light = DirectionalLight("Dir_Light%03d" % lightCounter)
            elif lightType == "ambientlight":
                light = AmbientLight("Amb_Light%03d" % lightCounter)
            elif lightType == "spotlight":
                light = Spotlight("Spt_Light%03d" % lightCounter)

            if light != None:
                color = entry.find("color")
                if color != None:
                    # set the light"s color
                    r = float(color.get("r", "1"))
                    g = float(color.get("g", "1"))
                    b = float(color.get("b", "1"))
                    a = float(color.get("a", "1"))
                    light.setColor(VBase4(r, g, b, a))

                # now create a new nodepath with the light
                lightnp = NodePath(light)

                # set the light"s position
                pos = self.__readPos(entry)
                lightnp.setPos(pos)

                # and it"s orientation
                hpr = self.__readHpr(entry)
                lightnp.setHpr(hpr)

                # finaly append the light to the list of lights
                self.leveldata.lights.append(lightnp)
            lightCounter += 1

    def __readAIUnits(self, root):
        for entry in list(root):
            aiUnitType = entry.get("type", default="Worker").lower()
            if aiUnitType == "worker":
                pass

    def __readModel(self, root):
        model = None

        if root is None: return None

        # try get the model path
        modelFile = root.find("model")
        if modelFile != None:
            # if we got a path try load it
            try:
                model = loader.loadModel(modelFile.text)
            except:
                logging.error(sys.exc_info()[1])

        # only if the model is loaded correctly, we can proceed
        if model is None: return None

        pos = self.__readPos(root)
        model.setPos(pos)

        scale = self.__readScale(root)
        model.setScale(scale)

        hpr = self.__readHpr(root)
        model.setHpr(hpr)

        return model

    def __readCollisionModel(self, root):
        modelData = root.find("collision")
        if "modelName" in modelData.keys():
            # The model is inside the main Model
            colNodeName = modelData.get("modelName")
            if self.leveldata.colModel != None:
                colModel = self.leveldata.colModel.find("**/" + colNodeName)
            else:
                colModel = self.leveldata.model.find("**/" + colNodeName)
            return colModel
        else:
            # The collision object has its own model file
            return self.__readModel(modelData)

    def __readPos(self, root):
        pos = root.find("position")

        if pos != None:
            if "nodeName" in pos.keys():
                posNodeName = pos.get("nodeName")
                p = self.leveldata.model.find(
                    "**/" + posNodeName).getPos()
                p.setX(p.getX() * self.leveldata.model.getScale().getX())
                p.setY(p.getY() * self.leveldata.model.getScale().getY())
                p.setZ(p.getZ() * self.leveldata.model.getScale().getZ())
                return p
            else:
                x = float(pos.get("x", "0.0")) \
                    * self.leveldata.model.getScale().getX()
                y = float(pos.get("y", "0.0")) \
                    * self.leveldata.model.getScale().getY()
                z = float(pos.get("z", "0.0")) \
                    * self.leveldata.model.getScale().getZ()
                return (x, y, z)
        return (0, 0, 0)

    def __readHpr(self, root):
        """Read heading Pinch and roll from the given root of the xml file.
        if the <hpr> tag is not found in the root tag, then (0, 0, 0) will
        be returned"""
        hpr = root.find("hpr")
        if hpr != None:
            if "nodeName" in hpr.keys():
                hprNodeName = hpr.get("nodeName")
                hpr = self.leveldata.model.find("**/" + hprNodeName).getHpr()
                return hpr
            else:
                h = float(hpr.get("h", "0.0"))
                p = float(hpr.get("p", "0.0"))
                r = float(hpr.get("r", "0.0"))
                return (h, p, r)
        return (0, 0, 0)

    def __readScale(self, root):
        """Read scale from the given root of the xml file. If the <scale>
        tag is not found, the default scale of 1.0 will be returned"""
        scale = root.find("scale")
        if scale != None:
            t = scale.get("type", "float")
            s = scale.text
            return eval("%s('%s')" % (t, s))
        return 1.0
