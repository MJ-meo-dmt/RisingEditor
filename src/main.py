#!/usr/bin/python

__author__ = "MJ-meo-dmt"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

## IMPORTS ##
import os

import sys

from pandac.PandaModules import loadPrcFileData
loadPrcFileData("",
"""
    window-title Rising Editor
    fullscreen 0
    win-size 1154 768
    cursor-hidden 0
    show-frame-rate-meter 1
    notify-level-rocket warning

"""
)

### PANDA Imports ###
from direct.showbase.ShowBase import ShowBase
#from pandac.PandaModules import
from panda3d.rocket import RocketRegion, RocketInputHandler, LoadFontFace
from panda3d.core import Filename

# to find all the editor modules even in other modules of the editor
sys.path.append(Filename(__file__).getFullpath())

### EDITOR IMPORTS ###
from Gizmo_tools import Gizmo
from editor_core.fileBrowser import FileBrowser
from editor_core.fileSaveDialog import FileSaveDialog
from level.LevelLoader import LevelLoader
from level.LevelData import LevelData
from lvlml_writer.lvlmlWriter import LvlmlWriter
########################################################################
########################################################################

### EDITOR BASE ###

class Editor(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

    #------------------------------------------------------------------#
    #
    #   SETUP BASIC LIBROCKET
    #
    #------------------------------------------------------------------#

        ## LOAD FONT ##
        LoadFontFace("../data_src/gui/fonts/verdana.ttf")

        ## SETUP REGION & INPUT HANDLER ##
        rw = RocketRegion.make('pandaRocket', base.win)
        rw.setActive(1)

        ih = RocketInputHandler()
        base.mouseWatcher.attachNewNode(ih)
        rw.setInputHandler(ih)

        ## CONTEXT ##
        self.context = rw.getContext()

        ## SETUP MAIN EDITOR WINDOW & GUI ##
        self.editorGui = self.context.LoadDocument('gui_src/editor_main.rml')
        self.editorGui.Show()


    #------------------------------------------------------------------#
    #
    #   EDITOR DEFAULT SETUP
    #
    #------------------------------------------------------------------#

        ## BASE DIR ##
        currentDir = os.getcwd()
        self.baseDir = currentDir + os.sep + "models"

        self.levelData = LevelData(self)
        
        ## NEW LEVEL VAR ##
        newLevelName = "unknownLevel"

    #------------------------------------------------------------------#
    #
    #   EDITOR EVENTS
    #
    #------------------------------------------------------------------#

        self.accept('new', self.New)
        self.accept('open', self.Open)
        self.accept('save', self.Save)
        self.accept('import', self.Import)
        self.accept('export', self.Export)


        ########################
        # Just build a basic simple file folder loader viewer thing for now
        # Something that loads or shows the contents of a dir hard coded
        #
        # editor: model, model1, model2, model3
        # and the texture folders, so that when clicked they can be added into the editor scene


        # Temp gizmo runner/ state=1
        self.gizmo = Gizmo(self, 1)


        ##
        # This should run when open file is used.
        self.levelload = LevelLoader(self)
        self.levelload.read("models/jump.lvlml", False)
        self.levelload.run()


    #------------------------------------------------------------------#
    #
    #   FILE DROP LIST
    #
    #------------------------------------------------------------------#

    def New(self):
        """
        Handle the clearing for a new fresh scene.
        """
        
        # Should add a check here to make sure that you dont delete a level
        # your working on, like one of those are you sure question crap..
        
        for node in self.gizmo.rootNp.getChildren():
            node.remove_node()
            
        
        # Set new level name
        newLevelName = newName

    def Open(self):
        """
        Handle the opening of a file browser dialog, browsing and
        opening of files selected.
        """
        self.fileBrowser = FileBrowser(self, self.baseDir)
        print self.fileBrowser.open(self.context)

    def Save(self):
        """
        Handle the saving of the scene, maybe even write out to file.
        Also handle the lvlml writeout.
        """
        #filename = "testLevel.lvlml"

        #TODO: open "file save dialog"

        #lvlmlWriter = LvlmlWriter()
        #LvlmlWriter.levelData = self.levelData
        #lvlmlWriter.write(filename)
        
        self.fileSaveDialog = FileSaveDialog(self, self.baseDir)
        print self.fileSaveDialog.open(self.context)

    def Import(self):
        """
        Handle importing files.
        *Atm not needed
        """
        pass

    def Export(self):
        """
        Handle exporting files.
        *Could be used for lvlml files and direct write out to bam or egg only??
        *Not used atm
        """
        pass


    #------------------------------------------------------------------#
    #
    #   EDIT DROP LIST
    #
    #------------------------------------------------------------------#

    #------------------------------------------------------------------#
    #
    #   VIEW DROP LIST
    #
    #------------------------------------------------------------------#

    #------------------------------------------------------------------#
    #
    #   HELP DROP LIST
    #
    #------------------------------------------------------------------#



########################################################################>
#
#  EDITOR BASE END
#
########################################################################>



app = Editor()

app.run()


















