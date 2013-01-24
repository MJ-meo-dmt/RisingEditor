#!/usr/bin/python

__author__ = "MJ-meo-dmt"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

## IMPORTS ##
import os
import sys


class PluginManager:
    """
    Plugin Manager
    
    Loads the plugins and manages them
    """
    
    plugins = {}
    
    def __init__(self, folder):
        """Load plugins from the folder"""
        
        folder = os.path.abspath(folder)
        
        if not os.path.isdir(folder):
            print "Error not able to load because '%s' is not a folder" % folder)
            return 
            
        
