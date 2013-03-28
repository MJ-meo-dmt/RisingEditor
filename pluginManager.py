#!/usr/bin/python

#----------------------------------------------------------------------#
"""
Plugin Manager
"""

# System imports
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

    def stop(self, plugin=""):
        """Stop the given plugin or all running plugins if none is given"""
        if plugin in self.Plugin:
            self.Plugin[plugin].stop()
        else:
            for modulename in self.Plugin:
                logging.debug("Stop %s" % modulename)
                self.Plugin[modulename].stop()

    def start(self, plugin=""):
        """Start the given plugin or all plugins if none is given"""
        if plugin in self.Plugin:
            self.Plugin[plugin].start()
        else:
            for modulename in self.Plugin:
                logging.debug("Start %s" % modulename)
                self.Plugin[modulename].start()

    def pluginList(self, pluginDir):
        """Find all plugins in given Dir."""
        for path in pluginDir.split(os.pathsep):
            for filename in os.listdir(path):
                name, ext = os.path.splitext(filename)

                if ext.endswith(".py"):
                    yield name

    def importPlugins(self, pluginDir, env):
        """Import all plugins from pluginDir into the give environment"""
        for plugin in self.pluginList(pluginDir):
            module = __import__(plugin, env)
            env[plugin] = module
            self.Plugin[plugin] = module.Plugin()
            logging.info("Load plugin: %s" % module)





