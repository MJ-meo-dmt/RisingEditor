from pandac.PandaModules import NodePath, CardMaker, LineSegs, Point2

import gizmo_core


TOLERANCE = 1e-3


class Marquee( NodePath, gizmo_core.Object ):
    
    """Class representing a 2D marquee drawn by the mouse."""
    
    def __init__( self, name, colour=(1, 1, 1, .2) ):
        gizmo_core.Object.__init__( self, name )

        # Create a card maker
        cm = CardMaker( self.name )
        cm.setFrame( 0, 1, 0, 1 )
        
        # Init the node path, wrapping the card maker to make a rectangle
        NodePath.__init__( self, cm.generate() )
        self.setColor( colour )
        self.setTransparency( 1 )
        self.reparentTo( render2d )
        self.hide()
        
        # Create the rectangle border
        ls = LineSegs()
        ls.moveTo( 0, 0, 0 )
        ls.drawTo( 1, 0, 0 )
        ls.drawTo( 1, 0, 1 )
        ls.drawTo( 0, 0, 1 )
        ls.drawTo( 0, 0, 0 )
        
        # Attach border to rectangle
        self.attachNewNode( ls.create() )
        
    def UpdateTask( self, task ):
        
        """
        Called every frame to keep the marquee scaled to fit the region marked
        by the mouse's initial position and the current mouse position.
        """
        
        # Check for mouse first, in case the mouse is outside the Panda window
        if base.mouseWatcherNode.hasMouse():
        
            # Get the other marquee point and scale to fit
            pos = base.mouseWatcherNode.getMouse() - self.initMousePos
            self.setScale( pos[0] if pos[0] else TOLERANCE, 1, pos[1] if pos[1] else TOLERANCE )
        
        return task.cont
    
    def IsPoint3Inside( self, camera, rootNode, point3d ):
    
        """Test if the specified point3 lies within the marquee area."""
        
        # Convert the point to the 3-d space of the camera
        p3 = camera.getRelativePoint( rootNode, point3d )

        # Convert it through the lens to render2d coordinates
        p2 = Point2()
        if not camera.GetLens().project( p3, p2 ):
            return False
        
        # Test point is within bounds of the marquee
        min, max = self.getTightBounds()
        if ( p2.getX() > min.getX() and p2.getX() < max.getX() and 
             p2.getY() > min.getZ() and p2.getY() < max.getZ() ):
            return True
        
        return False
        
    def Start( self ):
        gizmo_core.Object.Start( self )
        
        # Move the marquee to the mouse position and show it
        self.initMousePos = Point2( base.mouseWatcherNode.getMouse() )
        self.setPos( self.initMousePos[0], 1, self.initMousePos[1] )
        self.show()
                    
    def Stop( self ):
        gizmo_core.Object.Stop( self )
        
        # Hide the marquee
        self.hide()
        
   
