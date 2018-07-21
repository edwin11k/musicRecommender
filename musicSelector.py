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
        print()
        print('At Least One Positive & One Negative Sample Are Required For Modelling')
        print()
        size=len(self.newFactory.musicFiles.fileData)
        fileIndex=list(range(size))
        for mem in MusicHandler.posMusic:
            fileIndex.remove(mem)
        for mem in MusicHandler.negMusic:
            fileIndex.remove(mem)
        for mem in MusicHandler.absMusic:
            fileIndex.remove(mem)
 
        if fileIndex:
            return random.choice(fileIndex)
        else:
            return -10000
            
        
        
    def mostFavSelect(self):
        maxIndex=-10000;maxValue=-0.1;
        print()
        print('Selecting Your Most Favorite Music!')
        #print(MusicHandler.results)
        #print(MusicHandler.posMusic)
        #print(MusicHandler.negMusic)
        for mem in MusicHandler.results:
            #print(mem)
            if mem[3]>maxValue:
                maxValue=mem[3];maxIndex=mem[0]
        return maxIndex
        
        
    """ 
    Semi Unifying & Recommendation Model: 
    Reference to Yang et al. "Unifying recommendation and active learning for human-algorithm interaction" 
    equation (3)
    """
    
    def alphaModelSelect(self):
        minValue=100;minIndex=-1;
        for mem in MusicHandler.results:
            if mem[4]<minValue:
                minValue=mem[4];minIndex=mem[0];
        return minIndex


    
    def maxXorrSelect(self):
        maxValue=-1000000;maxMusicNum=-1;
        for musicNum,xorrValue in MusicHandler.xorrValueDic.items():
            if xorrValue>maxValue:
                maxValue=xorrValue;maxMusicNum=musicNum
        return maxMusicNum
        
    
    def minXorrSelect(self):
        minValue=1000000;minMusicNum=-1;
        for musicNum,xorrValue in MusicHandler.xorrValueDic.items():
            if xorrValue<minValue:
                minValue=xorrValue;minMusicNum=musicNum
        return minMusicNum    
        
    
        
