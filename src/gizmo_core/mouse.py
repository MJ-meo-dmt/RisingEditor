from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from pandac.PandaModules import Vec2


MOUSE_ALT = 0


class Mouse( DirectObject ):

    """Class representing the mouse."""

    def __init__( self ):
        DirectObject.__init__( self )

        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.buttons = [False, False, False]
        self.modifiers = []

        # Bind button events
        self.accept( 'mouse1', self.SetButton, [0, True] )
        self.accept( 'control-mouse1', self.SetButton, [0, True, [MOUSE_ALT]] )
        self.accept( 'mouse1-up', self.SetButton, [0, False, []] )

        self.accept( 'control-mouse2', self.SetButton, [1, True, [MOUSE_ALT]] )
        self.accept( 'mouse2', self.SetButton, [1, True] )
        self.accept( 'mouse2-up', self.SetButton, [1, False, []] )

        self.accept( 'control-mouse3', self.SetButton, [2, True, [MOUSE_ALT]] )
        self.accept( 'mouse3', self.SetButton, [2, True] )
        self.accept( 'mouse3-up', self.SetButton, [2, False, []] )

    def SetButton( self, id, value, modifiers=[] ):

        # Record buttons and modifiers
        self.buttons[id] = value
        self.modifiers = modifiers

    def __UpdateTask( self, task ):

        # Get pointer from screen, calculate delta
        mp = getBase().win.getPointer( 0 )
        self.dx = self.x - mp.getX()
        self.dy = self.y - mp.getY()
        self.x = mp.getX()
        self.y = mp.getY()

        return Task.cont

    def Start( self ):
        taskMgr.add( self.__UpdateTask, 'mouseUpdateTask' )

    def Stop( self ):
        taskMgr.remove( self.__UpdateTask )
