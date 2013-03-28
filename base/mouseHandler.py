from direct.showbase.DirectObject import DirectObject
from panda3d.core import Point3, LPoint2f

class MouseHandler(DirectObject):
    def __init__(self, bulletWorld):
        self.bulletWorld = bulletWorld
        self.multiSelect = False

    def start(self, onMouse1):
        self.accept('mouse1', self.checkMouseDown)
        self.accept('mouse1-up', self.checkMouseUp, [onMouse1])
        self.accept('control-mouse1',  self.checkMouseDown)
        self.accept('control-mouse1-up', self.checkMouseUp, [onMouse1])
        self.accept('control',  self.setMultiSelect, [True])
        self.accept('control-up', self.setMultiSelect, [False])

    def stop(self):
        self.ignore('mouse1')
        self.ignore('mouse1-up')
        self.ignore('control-mouse1')
        self.ignore('control-mouse1-up')
        self.ignore('control')
        self.ignore('control-up')

    def setMultiSelect(self, arg):
        self.multiSelect = arg

    def checkMouseDown(self):
        if base.mouseWatcherNode.hasMouse():
            # save the mouse position on mousedown events
            self.lastMousePos = LPoint2f(base.mouseWatcherNode.getMouse())

    def checkMouseUp(self, func):
        if base.mouseWatcherNode.hasMouse():
            # get the current mouse position
            curPos = base.mouseWatcherNode.getMouse()
            # compare it to the mousedown mouse position
            distance = curPos - self.lastMousePos
            if abs(distance.getX()) < 0.005 and abs(distance.getY()) < 0.005:
                # and call the mouse down func if the mouse didn't move to far
                func(self.multiSelect)

    def rayCheck(self):
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

            selected_object = objNode

        return selected_object
