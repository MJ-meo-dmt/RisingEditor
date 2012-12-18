#!/usr/bin/python

__author__ = "MJ-meo-dmt"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

## IMPORTS ##
import os
import sys


class PluginHandler:
    
    def __init__(self):
        
        print "Plugin Handler"
        
        
        
    def loader(self, plugin):
        
        self.plugin = plugin
        return self.plugin
        
    def initPlugin(self, plugin):
        
        print "Run plugin"


import os

def plugins_list(plugin_Dir):
    """ List all the plugins in the dir """
