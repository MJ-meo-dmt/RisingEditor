#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Documentation: SensorBase.py
  Classes and functions:
    N.A.
  Description:
    This class is the base class for all sensor types
"""

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.showbase.DirectObject import DirectObject

class SensorBase(DirectObject):
    def __init__(self):
        self.model = None
        self.modelGeom = None
        self.hasContact = False
        self.sensorType = ""
        self.sensorID = ""
        self._actOnCollide = False

    def acceptEvents(self):
        self.accept("collideSensor", self.onCollide)
        self.accept("stopCollideSensor", self.onStopCollide)

    def ignoreEvents(self):
        self.ignore("collideSensor")
        self.ignore("stopCollideSensor")
        self.ignore("sensorAction" + self.sensorID)

    def cleanup(self):
        self.ignoreEvents()
        self.model.removeNode()
        if self.modelGeom != None:
            self.modelGeom.removeNode()

    def onCollide(self, node):
        """If the collideSensor event is called the
        hasContact variable will be set if the sender
        collides with this sensor."""
        if node == self.modelGeom:
            self.hasContact = True
            base.messenger.send("sensorAction" + self.sensorID)

    def onStopCollide(self, node):
        """This event is called if the 'Sender Object' doesn't
        has a contact with this sensor anymore"""
        if node == self.modelGeom.node():
            self.hasContact = False
            self.ignore("sensorAction" + self.sensorID)

    def requestAct(self):
        """This function will check if there is a collision between
        this sensor and the one who triggered the event"""
        base.messenger.send("checkCollision", [self.modelGeom.node(), "stopCollideSensor"])


