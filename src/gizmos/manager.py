from direct.showbase.DirectObject import DirectObject


class Manager( DirectObject ):
    
    def __init__( self ):
        DirectObject.__init__( self )
        
        self.__gizmos = {}
        self.__activeGizmo = None
    
    def AddGizmo( self, gizmo ):
        
        """Add a gizmo to be managed by the gizmo manager."""
        
        self.__gizmos[gizmo.getName()] = gizmo
        
    def GetGizmo( self, name ):
        
        """
        Find and return a gizmo by name, return None if no gizmo with the
        specified name exists.
        """
        
        if name in self.__gizmos:
            return self.__gizmos[name]
        
        return None
    
    def GetActiveGizmo( self ):
        
        """Return the active gizmo."""
        
        return self.__activeGizmo
        
    def SetActiveGizmo( self, name ):
        
        """
        Stops the currently active gizmo then finds the specified gizmo by
        name and starts it.
        """
        
        # Stop the active gizmo
        if self.__activeGizmo is not None:
            self.__activeGizmo.Stop()
        
        # Get the gizmo by name and start it if it is a valid gizmo
        self.__activeGizmo = self.GetGizmo( name )
        if self.__activeGizmo is not None:
            self.__activeGizmo.Start()
        
    def GetGizmoLocal( self, name ):
        
        """Return the gizmos local mode."""
        
        gizmo = self.GetGizmo( name )
        if gizmo is not None:
            return gizmo.local
            
    def SetGizmoLocal( self, name, mode ):
        
        """Set all gizmo local modes, then refresh the active one."""
        
        gizmo = self.GetGizmo( name )
        if gizmo is not None:
            gizmo.local = mode
        
        if self.__activeGizmo is not None:
            self.__activeGizmo.Refresh()
        
    def SetSize( self, factor ):
        
        """Resize the gizmo by a factor."""
        
        for gizmo in self.__gizmos.values():
            gizmo.SetSize( factor )
            
    def AttachNodePaths( self, nodePaths ):
        
        """Attach a node path to be transformed by the gizmos."""
        
        for gizmo in self.__gizmos.values():
            gizmo.AttachNodePaths( nodePaths )