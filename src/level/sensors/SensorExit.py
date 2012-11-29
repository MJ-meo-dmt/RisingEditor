#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Documentation: SensorClimbeable.py
  Classes and functions:
    N.A.
  Description:
    This class is responsible for handling all sensors of the type exit
    so the spot at the end of a level
"""

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from SensorBase import SensorBase

class SensorExit(SensorBase):
    def __init__(self):
        SensorBase.__init__(self)

    def setActOnCollide(self, act):
        self._actOnCollide = act
        if act:
            SensorBase.accept(self, "checkSensorEvents", self.__sensorAction)

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
        base.messenger.send("exitLevel")

