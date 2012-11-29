#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Documentation: SensorWallRun.py
  Classes and functions:
    N.A.
  Description:
    This class is responsible for handling wall run areas, which means all
    walls in the game
"""

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from SensorBase import SensorBase

class SensorWallRun(SensorBase):
    def __init__(self):
        SensorBase.__init__(self)

    def activateSensor(self):
        self.acceptEvents()
        SensorBase.accept(self, "doInteligentAction", self.sensorAction)
        SensorBase.accept(self, "stopCollideSensor", self.stopWallRun)
        SensorBase.accept(self, "checkSensorEvents", self.__sensorAction)

    def deactivateSensor(self):
        self.ignoreEvents()
        SensorBase.ignore(self, "canStartWallRun")
        SensorBase.ignore(self, "doInteligentAction")
        SensorBase.ignore(self, "sensorAction" + self.sensorID)
        SensorBase.ignore(self, "checkSensorEvents")

    def sensorAction(self):
        SensorBase.accept(self, "sensorAction" + self.sensorID,
                          self.__sensorAction)
        self.requestAct()

    def doWallRun(self):
        SensorBase.ignore(self, "canStartWallRun")
        base.messenger.send("startWallRun")

    def stopWallRun(self, node):
        if node == self.modelGeom.node():
            SensorBase.ignore(self, "canStartWallRun")
            base.messenger.send("checkWallCollision", [self.modelGeom.node()])
            base.messenger.send("stopWallRun")

    def __sensorAction(self):
        SensorBase.accept(self, "canStartWallRun", self.doWallRun)
        base.messenger.send("setWallCollision", [self.modelGeom.node()])

