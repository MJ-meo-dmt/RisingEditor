### EDITOR FILE Save Dialog ###
import os
from direct.showbase.DirectObject import DirectObject
from panda3d.core import Filename

class FileSaveDialog(DirectObject):
    """
    The file browser can be used to open level, model and other files
    in the editor.
    """

    def __init__(self, _base, baseDir):
        self.base = _base
        self.currentDir = baseDir
        self.selectedFile = None


    def open(self, context):
        self.dialog = context.LoadDocument("gui_src/editor_save_dialog.rml")
        self.dialog.Show()

        btnCancel = self.dialog.GetElementById("cancel_btn")
        btnCancel.AddEventListener("click", lambda:self.close(), True)

        btnSave = self.dialog.GetElementById("save_btn")
        btnCancel.AddEventListener("click", lambda:self.save(), True)

        self.viewerList = self.dialog.GetElementById("filepathlist")
        self.viewerNavigationBox = self.dialog.GetElementById("path_txt")

        ## EVENTS ##
        self.accept("b", self.goBack)

        self.openFolderDir(self.currentDir)


    def close(self):
        if self.dialog != None:
            self.dialog.Close()

    def save(self):
        self.close()

    def dirViewer(self, dir):
        # add the special directory ".." to the directory
        # list to be able to navigate one directory level up
        # split up the directory and use the absolut path
        # instead of just adding .. at the end
        tmpPathList = dir.split("/")
        del tmpPathList[-1]
        tmpPath = "/".join(tmpPathList)
        if tmpPath == "": tmpPath = "/"
        self.createElementDir("div", "..", tmpPath)

        ## LOOP DIR ##
        for root, dirs, files in os.walk(dir):
            for name in files:
                filepath = os.path.join(root, name)

                if filepath.endswith(".lvlml"):
                    self.createElementLvlml("div", name, filepath)

            for dir in dirs:
                filepath = os.path.join(root, dir)
                self.createElementDir("div", dir, os.path.join(root, dir))
            # just add the files and folders of the current directory
            # and not of every directory in the tree
            break


    def goBack(self):
        self.tempDir = str(Filename.fromOsSpecific(self.currentDir))

        filepathlist = self.tempDir.split("/")
        del filepathlist[-1]

        self.tempStr = os.path.sep.join(filepathlist)
        print self.tempStr
        self.currentDir = self.tempStr
        self.openFolderDir(self.tempStr)


    def createElementLvlml(self, element, data, filepath):
        # Create element
        entry = self.dialog.CreateElement(element)
        entry.SetAttribute("id", data)
        entry.AddEventListener("click", lambda:self.addModelToScene(filepath), True)
        entry2 = self.base.editorGui.CreateElement("br")

        # Add text to display
        entry.inner_rml = data
        # Add element to base element
        self.viewerList.AppendChild(entry2)
        self.viewerList.AppendChild(entry)


    def createElementDir(self, element, data, filepath):
        # Create element
        entry = self.dialog.CreateElement(element)
        entry.SetAttribute("id", data)
        entry.AddEventListener("click", lambda:self.openFolderDir(filepath, True), True)
        entry2 = self.base.editorGui.CreateElement("br")

        # Add text to display
        entry.inner_rml = data

        # Add element to base element
        self.viewerList.AppendChild(entry2)
        self.viewerList.AppendChild(entry)


    def importModelToScene(self, filepath):
        # Add a if type check in here so that it checks
        # if file.egg ask to open
        # el if not .egg say its not right is other type
        # else if dir open that dir and display the files

        # use open for lvlml type files and normal egg files get imported

        modelDir = Filename.fromOsSpecific(filepath)

        self.model = self.base.loader.loadModel(modelDir)
        self.model.reparentTo(self.base.gizmo.rootNp)


    def addModelToScene(self, filepath):
        modelDir = Filename.fromOsSpecific(filepath)

        self.levelload = LevelLoader(self)
        self.levelload.read(str(modelDir), False)
        self.levelload.run()


    def openFolderDir(self, filepath, test=False):
        self.currentDir = filepath
        self.clearDirViewer()
        self.tempDirView = self.dirViewer(filepath)
        self.viewerNavigationBox.value = self.currentDir


    def clearDirViewer(self):
        # remove all directories and files from the list
        for elem in self.viewerList.GetElementsByTagName("div"):
            self.viewerList.RemoveChild(elem)
        # remove the hidden <br> elements
        for elem in self.viewerList.GetElementsByTagName("br"):
            self.viewerList.RemoveChild(elem)
