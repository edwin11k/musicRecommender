# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 11:18:49 2018

@author: edwin
"""

from musicFactory import *

defaultDir='C:/Users/edwin/Documents/music/musicSimulator/musicFile/Test2'
genre='Test'
window=0.4;step=0.4

class MusicHandler(object):
    newFactory=MusicFactory()  
    newFactory.loadMusic(genre,defaultDir,window,step);newFactory.saveMusicInfo()
    #Saving index of the musicfile that received either positive or negative result
    # Class variables to be shared by all instances
    posMusic=[];negMusic=[];absMusic=[];results=[]
    
    #Past choices will be saved in history
    history={}
      
    # will be overwritten 

    ###player----
    def musicPlay(self):
        pass
    
    def displayHistory(self):
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
    
    
