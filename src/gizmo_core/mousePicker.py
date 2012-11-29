from pandac.PandaModules import CollisionTraverser, CollisionHandlerQueue, BitMask32
from pandac.PandaModules import CollisionNode, CollisionRay

import gizmo_core


class MousePicker( gizmo_core.Object ):
    
    """
    Class to represent a ray fired from the input camera lens using the mouse.
    """
    
    def __init__( self, name, camera=None, rootNp=None, fromCollideMask=None, pickTag=None ):
        gizmo_core.Object.__init__( self, name, camera, rootNp )
        
        self.fromCollideMask = fromCollideMask
        self.pickTag = pickTag
        
        self.selection = []
        self.node = None
        self.collEntry = None
        
        # Create a marquee
        self.marquee = gizmo_core.Marquee( '%sMarquee' % self.name )
        
        # Create collision nodes
        self.collTrav = CollisionTraverser()
        #self.collTrav.showCollisions( render )
        self.collHandler = CollisionHandlerQueue()
        self.pickerRay = CollisionRay()
        
        # Create collision ray
        pickerNode = CollisionNode( self.name )
        pickerNode.addSolid( self.pickerRay )
        pickerNode.setIntoCollideMask( BitMask32.allOff() )
        pickerNp = camera.attachNewNode( pickerNode )
        self.collTrav.addCollider( pickerNp, self.collHandler )
        
        # Create collision mask for the ray if one is specified
        if self.fromCollideMask is not None:
            pickerNode.setFromCollideMask( self.fromCollideMask )
        
        # Bind mouse button events
        eventNames = ['mouse1', 'control-mouse1', 'mouse1-up']
        for eventName in eventNames:
            self.accept( eventName, self.FireEvent, [eventName] )
        
    def FireEvent( self, event ):
        
        # Send a message containing the node name and the event name, including
        # the collision entry as arguments
        if self.node is not None:
            messenger.send( '%s-%s' % ( self.node.getName(), event ), [self.collEntry] )
    
    def UpdateTask( self, task ):
        
        # Traverse the hierarchy and find collisions
        self.collTrav.traverse( self.rootNp )
        if self.collHandler.getNumEntries():
            
            # If we have hit something, sort the hits so that the closest is first
            self.collHandler.sortEntries()
            collEntry = self.collHandler.getEntry( 0 )
            node = collEntry.getIntoNode()
            
            # If this node is different to the last node, send a mouse leave
            # event to the last node, and a mouse enter to the new node
            if node != self.node:
                if self.node is not None:
                    messenger.send( '%s-mouse-leave' % self.node.getName(), [self.collEntry] )
                messenger.send( '%s-mouse-enter' % node.getName(), [collEntry] )
            
            # Send a message containing the node name and the event over name,
            # including the collision entry as arguments
            messenger.send( '%s-mouse-over' % node.getName(), [collEntry] )
            
            # Keep these values
            self.collEntry = collEntry
            self.node = node
            
        elif self.node is not None:
            
            # No collisions, clear the node and send a mouse leave to the last
            # node that stored
            messenger.send( '%s-mouse-leave' % self.node.getName(), [self.collEntry] )
            self.node = None
        
        # Update the ray's position
        if base.mouseWatcherNode.hasMouse():
            mp = base.mouseWatcherNode.getMouse()
            self.pickerRay.setFromLens( self.camera.node(), mp.getX(), mp.getY() )
            
        return task.cont
            
    def StartSelection( self, clearSelection=True ):
        
        # Start the marquee
        self.marquee.Start()
        
        # Clear selection list if required
        if clearSelection:
            self.selection = []
    
    def StopSelection( self ):
        
        # Stop the marquee
        self.marquee.Stop()
        
        nodes = []
        for node in self.rootNp.findAllMatches( '**' ):
            if self.marquee.IsPoint3Inside( self.camera, self.rootNp, node.getPos() ):
                
                if self.pickTag is not None:
                    if node.getTag( self.pickTag ):
                        nodes.append( node )
                else:
                    nodes.append( node )
        
        # Add any node which was under the mouse to the selection
        if self.collHandler.getNumEntries():
            collEntry = self.collHandler.getEntry( 0 )
            node = collEntry.getIntoNodePath().getParent()
            nodes.append( node )
            
        # If the node was already in the selection then remove it, otherwise
        # add the node to the selection
        for node in nodes:
            if node in self.selection:
                self.selection.remove( node )
            else:
                self.selection.append( node )
        
        # Remove duplicated
        self.selection = list( set( self.selection ) )
