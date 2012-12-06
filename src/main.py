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
		
		#self.dialog = self.context.LoadDocument('gui_src/editor_open_dialog.rml')
		#self.dialog.Show()
		
		
		
		########################
		# Just build a basic simple file folder loader viewer thing for now
		# Something that loads or shows the contents of a dir hard coded
		# 
		# editor: model, model1, model2, model3
		# and the texture folders, so that when clicked they can be added into the editor scene
		cwd = os.getcwd()
		self.baseModelDir = cwd + "\models"
		
		
		for root, dirs, files in os.walk(self.baseModelDir):
			for name in files:
				filepath = os.path.join(root, name)
				if filepath.endswith(".egg"):
					
					self.createElement("div", name)
					
		
		
		
		# Make a list type and then build a custom element with added
		# script onclick
		
		# Temp gizmo runner
		self.gizmo = Gizmo(self)
		
		
		## 
		# This should run when open file is used.
		self.levelload = LevelLoader(self)
		self.levelload.read("level/jump.lvlml", False)
		self.levelload.run()
		
	def createElement(self, element, data):
		
		# Get element on document
		fileview = self.editorGui.GetElementById("filepathlist")
		print fileview
		# Create element
		entry = self.editorGui.CreateElement(element)
		entry.DispatchEvent("onclick", {"object" : "hello"}, True)
		entry2 = self.editorGui.CreateElement('br')
		
		# Add text to display
		entry.inner_rml = data
		
		# Add element to base element
		fileview.AppendChild(entry2)
		fileview.AppendChild(entry)


app = Editor()

app.run()
