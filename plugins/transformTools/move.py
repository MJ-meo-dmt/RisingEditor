
#TODO: Load model for move transformation (x/y/z axis arrows)
#TODO: Model should be always on top of all models to be selectable all the time
#TODO: add bullet geom around axis to select axis to move object (tube or box)
#TODO: actual model transformation (check if collision solid gets transformed correct too!)

#from panda3d.bullet import ...

selectedObject = None

axisModel = loader.loadModel("misc/xyzAxis")
axisModel.reparentTo(render)
axisModel.hide()

def startTransform(object):
    print "start move", object
    global selectedObject
    selectedObject = object
    #axisModel.reparentTo(selectedObject)
    #print selectedObject.getPos()
    axisModel.setPos(selectedObject, selectedObject.getPos())
    #axisModel.setHpr(selectedObject.getHpr())
    axisModel.show()

def stopTransform():
    print "stop move"
    axisModel.hide()
