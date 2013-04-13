
#TODO: Load model for scale transformation (x/y/z axis arrows with box heads)
#TODO: Model should be always on top of all models to be selectable all the time
#TODO: add bullet geom around axis to select the axis to scale the object on (tube or box)
#TODO: actual model transformation (check if collision solid gets transformed correct too!)

selectedObject = None

def transform(object):
    global selectedObject
    selectedObject= object
    print "scale", object

def stopTransform():
    global selectedObject
    print "stop scale"
