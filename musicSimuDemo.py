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
    print("Music Simulator: Based On Response, It Will Find Your Favorites")
    print()
    
    selector=MusicSelector();player=MusicPlayer();classifier=MusicClassifier()
    
    while True:
        print()
        print('Finding Random Choice of Music!')
        newValue=selector.randomSelect()
        if newValue==-10000:
            print()
            print('Music Data Has Run Out!')
            player.displayHistory()
            return
        player.musicPlay(newValue)
        if len(selector.posMusic)>0 and len(selector.negMusic)>0:           
            break
    
    while True:
        if player.musicStop():
            print()
            print('Thank You For Using The System!')
            player.displayHistory()
            return
        
        print('Making Model based on Past answer!')
        classifier.binaryClassifier();classifier.testClassifier();
        newMusicIndex=selector.mostFavSelect()
        if newMusicIndex==-10000:
            print('Music Data has run out!')
            break
        else:
            player.musicPlay(newMusicIndex)
      
    player.displayHistory()
    
musicRecommender()

