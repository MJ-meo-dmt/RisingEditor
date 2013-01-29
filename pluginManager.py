#!/usr/bin/python

#----------------------------------------------------------------------#
"""
Plugin Manager
"""

# System imports
import sys
import os
import logging

# Panda Engine imports

# Extra imports

#----------------------------------------------------------------------#

### PLUGIN CORE ###

class PluginMgr():


    def __init__(self):
        
        # Could be used for "In editor list viewing or something"
        self.Plugin = {}
        
    # Find all plugins in given Dir.
    def pluginList(self, pluginDir):
        
        for path in pluginDir.split(os.pathsep):
            for filename in os.listdir(path):
                name, ext = os.path.splitext(filename)
                
                if ext.endswith(".py"):
                    yield name
                    
    
    # Import Plugins.
    def importPlugins(self, pluginDir, env):
        for plugin in self.pluginList(pluginDir):
            module = __import__(plugin, env)
            env[plugin] = module
            self.activePlugin[plugin] = module
            print "Imported: %s" % module
            
            
            
            
