#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Documentation: SensorClimbeable.py
  Classes and functions:
    N.A.
  Description:
    This class is responsible for handling all sensors of the type climbeable
    like pipes, ladders or fences
"""

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from SensorBase import SensorBase

class SensorClimbeable(SensorBase):
    def __init__(self):
        SensorBase.__init__(self)
        # the directions in which the player can
        # climbe at that thing. Vertical for example
        # means the player can climb up and down but
        # not left or right
        self.direction = "vertical"
        self.setFly = True

    def setActOnCollide(self, act):
        self._actOnCollide = act
        if act:
            SensorBase.accept("checkSensorEvents", self.__sensorAction)

    def activateSensor(self):
        self.acceptEvents()
        SensorBase.accept(self, "doAction", self.sensorAction)
        if self._actOnCollide:
            SensorBase.accept(self, "checkSensorEvents", self.__sensorAction)

    def deactivateSensor(self):
        self.ignoreEvents()
        SensorBase.ignore(self, "doAction")
        SensorBase.ignore(self, "sensorAction" + self.sensorID)
        SensorBase.ignore(self, "checkSensorEvents")

    def sensorAction(self):
        SensorBase.accept(self, "sensorAction" + self.sensorID,
                          self.__sensorAction)
        self.requestAct()

    def __sensorAction(self):
        if not self._actOnCollide:
            SensorBase.ignore(self, "sensorAction" + self.sensorID)
        base.messenger.send("setCharFlyMode", [self.setFly, self.direction])
        self.setFly = not self.setFly

