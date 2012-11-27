#!/usr/bin/python

# License

#----------------------------------------------------------------------#


## IMPORTS ##
import os
import sys

from pandac.PandaModules import loadPrcFileData
loadPrcFileData("",
"""    
	window-title Rising Editor
	fullscreen 0
	win-size 1280 800
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
	


app = Editor()

app.run()
