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


### EDITOR BASE ###

class Editor(ShowBase):
	
	def __init__(self):
		
		ShowBase.__init__(self)
		
	#------------------------------------------------------------------#
	#
	# 	SETUP BASIC LIBROCKET
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
		
		#self.dialog = self.context.LoadDocument('gui_src/editor_open_dialog.rml')
		#self.dialog.Show()
	
	
	#------------------------------------------------------------------#
	#
	# 	EDITOR DEFAULT SETUP
	#
	#------------------------------------------------------------------#
		
		## BASE DIR ##
		currentDir = os.getcwd()
		self.baseDir = cwd + "\models"
		
		
	#------------------------------------------------------------------#
	#
	# 	EDITOR EVENTS
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
		
	
		# Temp gizmo runner
		self.gizmo = Gizmo(self)
		
		
		## 
		# This should run when open file is used.
		self.levelload = LevelLoader(self)
		self.levelload.read("level/jump.lvlml", False)
		self.levelload.run()
		
		
	#------------------------------------------------------------------#
	#
	# 	FILE DROP LIST
	#
	#------------------------------------------------------------------#
	
	def New(self):
		"""
		Handle the clearing for a new fresh scene.
		"""
		
		for node in self.gizmo.rootNp.getChildren():
			print node
			node.remove_node()
			
	def Open(self):
		"""
		Handle the opening of a file browser dialog, browsing and
		opening of files selected.
		"""
		pass
		
	def Save(self):
		"""
		Handle the saving of the scene, maybe even write out to file.
		Also handle the lvlml writeout.
		"""
		pass 
		
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
	# 	EDIT DROP LIST
	#
	#------------------------------------------------------------------#
	
	#------------------------------------------------------------------#
	#
	# 	VIEW DROP LIST
	#
	#------------------------------------------------------------------#
	
	#------------------------------------------------------------------#
	#
	# 	HELP DROP LIST
	#
	#------------------------------------------------------------------#



########################################################################>
#
#  EDITOR BASE END
#
########################################################################>



### EDITOR FILE BROWSER ###

class FileBrowser():
	
	def __init__(self, baseDir):
		
		self.selectedFile = None
		
		## LOOP DIR ##
		for root, dirs, files in os.walk(baseDir):
			for name in files:
				filepath = os.path.join(root, name)
				if filepath.endswith(".egg"):
					
					self.createElement("div", name)


	def createElement(self, element, data):
		
		# Get element on document
		fileview = self.editorGui.GetElementById("filepathlist")
		# Create element
		entry = self.editorGui.CreateElement(element)
		entry.SetAttribute("id", data)
		entry.AddEventListener('click', lambda:self.addModelToScene(data), True)
		entry2 = self.editorGui.CreateElement('br')
		
		# Add text to display
		entry.inner_rml = data
		print data
		# Add element to base element
		fileview.AppendChild(entry2)
		fileview.AppendChild(entry)


	def addModelToScene(self, path):
		self.path = path 
		print self.path
		# Add a if type check in here so that it checks
		# if file.egg ask to open
		# el if not .egg say its not right is other type
		# else if dir open that dir and display the files 








app = Editor()

app.run()


















