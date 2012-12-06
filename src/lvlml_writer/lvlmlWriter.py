#!/usr/bin/python

__author__ = "MJ-meo-dmt"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

## IMPORTS ##
import os
import sys

from xml.etree import ElementTree as xml


class LvlmlWriter():
    
    def __init__(self):
        
        # Test vars
        id = "jumplevel"
        authorname = "Someone"
        datetext = "2012-12-12"
        levelname = "levelname"
        
        ##########################
        
        # level is root (outer)
        level = xml.Element('level')
        level.attrib['id'] = id
        
        ## Add the inners
        
        # author
        author = xml.Element('author') 
        author.text = authorname
        level.append(author)
        
        # date
        date = xml.Element('date')
        date.text = datetext
        level.append(date)
        
        # level name
        name = xml.Element('name')
        name.text = levelname
        level.append(name)
        
        ## basemodel ##
        basemodel = xml.Element('basemodel')
        
        # Sub element
        model = xml.Element('model')
        model.text = modelPath
        basemodel.append(model)
        
        scale = xml.Element("scale")
        scale.text = modelScale
        basemodel.append(scale)
        ##>
        
        ## GroundCol ##
        groundCol = xml.Element('groundCollision')
        
        # Sub element
        collision = xml.Element('collision')
        collision.attrib['modelname'] = "collision"
        groundCol.append(collision)
        ##>
        
        ## Startpos ##
        startPosition = xml.Element('startpos')
        
        # Sub element
        startPos = xml.Element('position')
        startPos.attrib['nodeName'] = "startpos"
        startPosition.append(startPos)
        
        startHpr = xml.Element('hpr')
        startHpr.attrib["nodename"] = "startpos"
        startPosition.append(startHpr)
        ##>
        
        ## Level exit ##
        levelExit = xml.Element('exit')
        
        # Sub element
        exitCollision = xml.Element('collision')
        exitCollision.attrib['modelName'] = "exit"
        levelExit.append(exitCollision)
        ##>
        
        ## Lights ##
        lights = xml.Element('lights')
        
        # inside lights run method to add more lights
        
        
        
        
        
        
        
        file = open("test.lvlml", 'w')
        
        xml.ElementTree(level).write(file)
        
        file.close()
    


writer = LvlmlWriter()
