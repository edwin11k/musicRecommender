# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 11:35:01 2018

@author: edwin
"""
""" This file will get music!!!! """

from music import *
import os

class MusicFactory(object):
     
    
    def loadMusic(self,music_genre=None,directory=os.curdir,window1=0.4,step1=0.4):
        self.musicFiles=Music(dirPath=directory,music_genre=music_genre,window=window1,step=step1)
        return self.musicFiles
    
    def printMusicFileInfo(self):
        print(self.musicFiles)
        
    def saveMusicInfo(self):
        self.musicFiles.saveMusicInfo()
