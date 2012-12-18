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
from panda3d.core import Filename
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
		self.baseDir = currentDir + "\models"
		
		
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
		self.fileBrowser = FileBrowser(self, self.baseDir)
		
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

class FileBrowser(DirectObject):
	
	def __init__(self, _base, baseDir):
		
		self.base = _base
		
		self.currentDir = baseDir
		
		print self.currentDir
		self.selectedFile = None
		
		## EVENTS ##
		self.accept('b', self.goBack)
		
		## LOOP DIR ##
		for root, dirs, files in os.walk(baseDir):
			for name in files:
				filepath = os.path.join(root, name)
	
				if filepath.endswith(".egg"):
					
					self.createElementModel("div", name, filepath)
					
				if filepath.endswith(".lvlml"):
					
					self.createElementLvlml("div", name, filepath)
			
			for dir in dirs:
				
				self.createElementDir("div", dir)
	
	def goBack(self):
		
		self.tempDir = str(Filename.fromOsSpecific(self.currentDir))
		
		filepathlist = self.tempDir.split('/')
		del filepathlist[-1]
		
		self.tempStr = os.path.sep.join(filepathlist)
		self.currentDir = self.tempStr
		print filepathlist
		print self.tempStr
	
	def createElementModel(self, element, data, filepath):
		
		# Get element on document
		fileview = self.base.editorGui.GetElementById("filepathlist")
		# Create element
		entry = self.base.editorGui.CreateElement(element)
		entry.SetAttribute("id", data)
		entry.AddEventListener('click', lambda:self.importModelToScene(data, filepath), True)
		entry2 = self.base.editorGui.CreateElement('br')
		
		# Add text to display
		entry.inner_rml = data
		print data
		# Add element to base element
		fileview.AppendChild(entry2)
		fileview.AppendChild(entry)
	
	def createElementLvlml(self, element, data, filepath):
		
		# Get element on document
		fileview = self.base.editorGui.GetElementById("filepathlist")
		# Create element
		entry = self.base.editorGui.CreateElement(element)
		entry.SetAttribute("id", data)
		entry.AddEventListener('click', lambda:self.addModelToScene(data, filepath), True)
		entry2 = self.base.editorGui.CreateElement('br')
		
		# Add text to display
		entry.inner_rml = data
		print data
		# Add element to base element
		fileview.AppendChild(entry2)
		fileview.AppendChild(entry)
		
	def createElementDir(self, element, data):
		
		# Get element on document
		fileview = self.base.editorGui.GetElementById("filepathlist")
		# Create element
		entry = self.base.editorGui.CreateElement(element)
		entry.SetAttribute("id", data)
		entry.AddEventListener('click', lambda:self.openFolderDir(data), True)
		entry2 = self.base.editorGui.CreateElement('br')
		
		# Add text to display
		entry.inner_rml = data
		print data
		# Add element to base element
		fileview.AppendChild(entry2)
		fileview.AppendChild(entry)


	def importModelToScene(self, path, filepath):
		self.path = path 
		
		# Add a if type check in here so that it checks
		# if file.egg ask to open
		# el if not .egg say its not right is other type
		# else if dir open that dir and display the files 
		
		# use open for lvlml type files and normal egg files get imported
		
		modelDir = Filename.fromOsSpecific(filepath)
		
		self.model = loader.loadModel(modelDir)
		self.model.reparentTo(self.base.gizmo.rootNp)
		
		
		#print Filename.exists(modelDir)
		#self.levelload = LevelLoader(self)
		#self.levelload.read(str(modelDir), False)
		#self.levelload.run()
		
	def addModelToScene(self, path, filepath):
		self.path = path
		
		modelDir = Filename.fromOsSpecific(filepath)
		
		print Filename.exists(modelDir)
		self.levelload = LevelLoader(self)
		self.levelload.read(str(modelDir), False)
		self.levelload.run()

	def openFolderDir(self, path):
		self.path = path 
		print self.path, "Folder Dir"






app = Editor()

app.run()


















