#!/usr/bin/python

__author__ = "MJ-meo-dmt"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

## IMPORTS ##
import sys
from xml.etree import ElementTree as xml
from panda3d.core import Vec4
from level.LevelData import LevelData
from datetime import date


class LvlmlWriter():

    def __init__(self):

        self.levelData = LevelData

        # Test vars
        #id = "jumplevel"
        #authorname = "Someone"
        #datetext = "2012-12-12"
        #levelname = "levelname"

        self.levelData.levelID = str(id(self))
        self.levelData.author = "anonymous"
        self.levelData.date = date.today().strftime("%d/%m/%y")
        self.levelData.name = "unnamed"

    def write(self, filename):
        filename = "test.lvlml"

        # test values
        modelPath = "blabla/blabla/bla.egg"
        modelScale = "1"

        ##########################
        print "start write lvlml file"

        # level is root (outer)
        level = xml.Element('level')
        level.attrib['id'] = self.levelData.levelID

        ## Add the inners

        # author
        author = xml.Element('author')
        author.text = self.levelData.author
        level.append(author)

        # date
        xmldate = xml.Element('date')
        xmldate.text = self.levelData.date
        level.append(xmldate)

        # level name
        name = xml.Element('name')
        name.text = self.levelData.name
        level.append(name)

        ## basemodel ##
        level.append(self.__writeModel("basemodel", modelPath, modelScale))
        ##>

        ## GroundCol ##
        groundCol = xml.Element('groundCollision')

        # Sub element
        collision = xml.Element('collision')
        collision.attrib['modelname'] = "collision"
        groundCol.append(collision)
        level.append(groundCol)
        ##>

        ## Startpos ##
        startPosition = xml.Element('startpos')

        # Sub element
        startPos = xml.Element('position')
        startPos.attrib['nodeName'] = "startpos"
        startPosition.append(startPos)

        startHpr = xml.Element('hpr')
        startHpr.attrib["nodeName"] = "startpos"
        startPosition.append(startHpr)
        level.append(startPosition)
        ##>

        ## Level exit ##
        levelExit = xml.Element('exit')

        # Sub element
        exitCollision = xml.Element('collision')
        exitCollision.attrib['modelName'] = "exit"
        levelExit.append(exitCollision)
        level.append(levelExit)
        ##>

        ## Lights ##
        lights = xml.Element('lights')

        # inside lights run method to add more lights
        # Add mass and other physics details inside lvlml files
        # they will construct the levels themselfs
        # each egg will be alone apart from all the basic level stuff for a level egg
        # Add the plugin system!!
        # Add config for editor plugins


        #### WRITE OUT ####

        try:

            file = open(filename, 'w')
            xml.ElementTree(level).write(file, "utf-8", "xml")
            file.close()

        except:
            print "Error couldn't write file out!"
            print sys.exc_info()[0]
            print sys.exc_info()[1]

        print "Done..."

    def __writeModel(self, elementName, modelPath, modelScale):
        """
        creates a model specific xml node with the given values
        and returns that node at the end
        """
        modelNode = xml.Element(elementName)

        # Sub element
        model = xml.Element('model')
        model.text = modelPath
        modelNode.append(model)

        scale = xml.Element("scale")
        scale.text = modelScale
        modelNode.append(scale)

        return modelNode

    def addLights(self, type, pos, color=Vec4(.5, .5, .5, 1)):

        self.type = type
        self.position = pos
        self.color = color


writer = LvlmlWriter()
