# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 11:18:49 2018

@author: edwin
"""

from musicFactory import *

defaultDir='C:/Users/edwin/Documents/music/musicSimulator/musicFile/Test'
genre='Test'

class MusicHandler(object):
    newFactory=MusicFactory();newFactory.loadMusic(genre,defaultDir,0.4,0.4)
    #Saving index of the musicfile that received either positive or negative result
    # Class variables to be shared by all instances
    posMusic=[];negMusic=[];results=[]
    
    # will be overwritten in inhereted class
    ###player----
    def emptyResults(self):
        self.results=[]
    
    def musicPlay(self):
        pass
    
    ## selector-----
    def randomSelect(self):
        pass
    

    
    ## Classifier-----
    def binaryClassifier(self):
        pass
    
    def testClassifier(self):
        pass
    
    
    def mostFavSelect(self):
        pass
    