# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 10:57:37 2018

@author: edwin
"""

from musicClassifier import *
from musicPlayer import *
from musicSelector import *



def musicRecommender():
    print()
    print("Music Simulator: Based on your response, it finds likely favorites")
    print()
    
    selector=MusicSelector();player=MusicPlayer();classifier=MusicClassifier()
    
    while True:
        print('Finding Random Choice of Music!')
        newValue=selector.randomSelect()
        player.musicPlay(newValue)
        
        if len(selector.posMusic)>0 and len(selector.negMusic)>0:
            print('Making Model based on Past answer!')
            break
    
    while True:
        classifier.binaryClassifier();classifier.testClassifier();
        classifier.emptyResults()
        newMusicIndex=selector.mostFavSelect()
        #print(newMusicIndex)
        if newMusicIndex==-100:
            print('Music Data has run out!')
            break
        else:
            player.musicPlay(newMusicIndex)
        
    
musicRecommender()

