
#TODO: Load model for rotation transformation (h/p/r rings)
#TODO: Model should be always on top of all models to be selectable all the time
#TODO: add bullet geom around axis to select axis to rotate object (torus or something else)
#TODO: actual model transformation (check if collision solid gets transformed correct too!)

selectedObject = None

def transform(object):
    global selectedObject
    selectedObject= object
    print "rotate", object

def stopTransform():
    global selectedObject
    print "stop rotate"
