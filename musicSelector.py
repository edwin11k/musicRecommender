# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 14:53:57 2018

@author: edwin
"""

from musicHandler import *
import random 


class MusicSelector(MusicHandler):
    
    #Randomly select an index that are not selected before which are contained either posMusic or negMusic
    def randomSelect(self):
        size=len(self.newFactory.musicFiles.fileData)
        fileIndex=list(range(size))
        for mem in MusicHandler.posMusic:
            fileIndex.remove(mem)
        for mem in MusicHandler.negMusic:
            fileIndex.remove(mem)
        for mem in MusicHandler.absMusic:
            fileIndex.remove(mem)
        return random.choice(fileIndex)
        
    def mostFavSelect(self):
        maxIndex=-1000000;maxValue=-0.1;
        print('Selecting Your Favorite Music!')
        #print(MusicHandler.results)
        #print(MusicHandler.posMusic)
        #print(MusicHandler.negMusic)
        for mem in MusicHandler.results:
            #print(mem)
            if mem[3]>maxValue:
                maxValue=mem[3];maxIndex=mem[0]
                #print('new favorite!')
            #print(maxValue,maxIndex)
        return maxIndex
        
        
        
