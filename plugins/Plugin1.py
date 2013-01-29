#!/usr/bin/python

"""
This is an Example Plugin module/class setup.
"""

class Plugin1:
    
    def __init__(self):
        
        self.name = "Plugin1 This is the plugin"
        

    
    def start(self):
        
        print self.name
        
    def stop(self):
        
        pass


PLUGIN1 = Plugin1()
