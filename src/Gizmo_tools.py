import random

from direct.directtools.DirectGrid import DirectGrid, DirectObject
from pandac.PandaModules import Vec4, Vec3, Vec2, DirectionalLight, GeomNode
from direct.task.Task import Task

import gizmo_core
import gizmos


PICK_TAG = 'pickable'


class Gizmo( DirectObject ):
    
    def __init__( self ):
        
        
        # Create mouse
        base.disableMouse()
        self.mouse = gizmo_core.Mouse()
        self.mouse.Start()
        
        # Create camera
        self.camera = gizmo_core.Camera( pos=(-250, -250, 200), style=
                                  gizmo_core.CAM_USE_DEFAULT | 
                                  gizmo_core.CAM_VIEWPORT_AXES )
        self.camera.Start()
        
        # Create grid
        grid = DirectGrid( parent=render, planeColor=(0.5, 0.5, 0.5, 0.5) )
        
        # Create scene root node
        self.rootNp = render.attachNewNode( 'rootNode' )
        
        # Create node picker
        self.nodePicker = gizmo_core.MousePicker( 'mouse', self.camera, self.rootNp, fromCollideMask=GeomNode.getDefaultCollideMask(), pickTag=PICK_TAG )
        self.nodePicker.Start()
        
        # Bind node picker events
        self.accept( 'mouse1', self.StartSelection )
        #self.accept( 'control-mouse1', self.StartSelection, [False] ) # Can't seem to get this to prioritise properly
        self.accept( 'mouse1-up', self.StopSelection )
        
        # Create gizmo manager
        self.gizmoMgr = gizmos.Manager()
        self.gizmoMgr.AddGizmo( gizmos.Translation( 'pos', self.camera ) )
        self.gizmoMgr.AddGizmo( gizmos.Rotation( 'rot', self.camera ) )
        self.gizmoMgr.AddGizmo( gizmos.Scale( 'scl', self.camera ) )
        
        # Bind gizmo manager events
        self.accept( 'q', self.gizmoMgr.SetActiveGizmo, [None] )
        self.accept( 'w', self.gizmoMgr.SetActiveGizmo, ['pos'] )
        self.accept( 'e', self.gizmoMgr.SetActiveGizmo, ['rot'] )
        self.accept( 'r', self.gizmoMgr.SetActiveGizmo, ['scl'] )
        self.accept( 'space', self.ToggleAllGizmoLocalMode )
        self.accept( '+', self.gizmoMgr.SetSize, [2] )
        self.accept( '-', self.gizmoMgr.SetSize, [0.5] )
        
        # Create gizmo manager mouse picker
        self.gizmoPicker = gizmo_core.MousePicker( 'mouse', self.camera )
        self.gizmoPicker.Start()
        
        # Create some objects
        for i in range( 20 ):
            ball = loader.loadModel( 'smiley' )
            ball.setTag( PICK_TAG, '1' )
            ball.reparentTo( self.rootNp )
            ball.setPos( random.randint( -30, 30 ) * 2, random.randint( -30, 30 ) * 2, random.randint( -30, 30 ) * 2 )
            ball.setScale( 10, 10, 10 )
        
        # Create a light
        dlight = DirectionalLight('dlight')
        dlight.setColor( ( 1, 1, 1, 1 ) )
        dlnp = render.attachNewNode(dlight)
        dlnp.setHpr(0, 0, 0)
        render.setLight(dlnp)
        dlnp.reparentTo( self.camera )
        
        # Create tasks
        taskMgr.add( self.MouseTask, 'mouseTask' )
    
    def ToggleAllGizmoLocalMode( self ):
        
        """Toggle all gizmos local mode on or off."""
        
        value = self.gizmoMgr.GetGizmoLocal( 'pos' )
        self.gizmoMgr.SetGizmoLocal( 'pos', not value )
        self.gizmoMgr.SetGizmoLocal( 'rot', not value )
        self.gizmoMgr.SetGizmoLocal( 'scl', not value )
        
    def StartSelection( self, clearSelection=True ):
        
        """
        Start the marquee if there is no active gizmo or the currently active
        gizmo is not in dragging mode.
        """
        
        activeGizmo = self.gizmoMgr.GetActiveGizmo()
        if activeGizmo is None or ( activeGizmo is not None and 
                                    not activeGizmo.dragging ):
                                    
            # Reset selected node colours
            for i in self.nodePicker.selection:
                i.setColorScale( Vec4(1) )
                
            self.nodePicker.StartSelection( clearSelection )
                    
    def StopSelection( self ):
        
        """
        Stop the marquee and attach the selected node paths to the managed
        gizmos.
        """
        
        # Return if the marquee is not running
        if not self.nodePicker.marquee.IsRunning():
            return
        
        # Stop the marquee
        self.nodePicker.StopSelection()
        
        # Set the colour of the selected objects
        for i in self.nodePicker.selection:
            i.setColorScale( Vec4(1, 0, 0, 1) )
        
        # Attach the selection to the gizmo manager
        self.gizmoMgr.AttachNodePaths( self.nodePicker.selection )
        
        # Get the active gizmo
        activeGizmo = self.gizmoMgr.GetActiveGizmo()
        if activeGizmo is not None:
            
            # Refresh the active gizmo so it appears in the right place
            activeGizmo.Refresh()
    
    def MouseTask( self, task ):
        
        """
        Task to control mouse events. Gets called every frame and will
        update the scene accordingly.
        """
        
        # Return if no mouse is found or alt not down
        if not base.mouseWatcherNode.hasMouse() or not gizmo_core.MOUSE_ALT in self.mouse.modifiers:
            return Task.cont
        
        # ORBIT - If left mouse down
        if self.mouse.buttons[0]:
            self.camera.Orbit( Vec2(self.mouse.dx / 5.0, self.mouse.dy / 5.0) )
        
        # DOLLY - If middle mouse down
        elif self.mouse.buttons[1]:
            self.camera.Move( Vec3(self.mouse.dx / 5.0, 0, -self.mouse.dy / 5.0) )
            
        # ZOOM - If right mouse down
        elif self.mouse.buttons[2]:
            self.camera.Move( Vec3(0, -self.mouse.dx / 5.0, 0) )
            
        return Task.cont
    

