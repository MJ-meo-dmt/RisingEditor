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
	notify-level-rocket debug
	
"""
)

### PANDA Imports ###
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *
from panda3d.rocket import *
from direct.showbase.DirectObject import DirectObject


### EDITOR IMPORTS ###
from Gizmo_tools import Gizmo
from level.LevelLoader import LevelLoader
########################################################################
########################################################################


### MAIN APP CLASS ###

class Editor(ShowBase):
	
	def __init__(self):
		
		ShowBase.__init__(self)
		
		## Load a font type ##
		LoadFontFace("../data_src/gui/fonts/verdana.ttf")
		
		## Setup librocket and the input handler ##
		rw = RocketRegion.make('pandaRocket', base.win)
		rw.setActive(1)
		
		# Handler
		ih = RocketInputHandler()
		base.mouseWatcher.attachNewNode(ih)
		rw.setInputHandler(ih)
		
		# Setup context
		self.context = rw.getContext()
		
		# Setup Editor gui
		self.editorGui = self.context.LoadDocument('gui_src/editor_main.rml')
		self.editorGui.Show()
		
		## TEMP ##
		self.accept('escape', sys.exit)
		
		
		# Temp gizmo runner
		# This should run when open file is used.
		self.gizmo = Gizmo(self)
		
		self.levelload = LevelLoader(self)
		self.levelload.read("level/jump.lvlml", False)
		self.levelload.run()
		
		

		


app = Editor()

app.run()
