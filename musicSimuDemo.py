# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 10:57:37 2018

@author: edwin
"""

from musicClassifier import *
from musicPlayer import *
from musicSelector import *

# Path where model file exists
modelDir1='C:/Users/edwin/Documents/music/musicSimulator/musicFile/Test'
modelDir2='C:/Users/edwin/Documents/music/musicSimulator/musicFile/Test2'

# Path to music data files need to be set in musicHandler.py 
alpha=0.5;




def modelMaker():
    print()
    print("Play random music in the folder and Generate Machine Learning Model ")
    print()
    
    selector=MusicSelector();player=MusicPlayer();classifier=MusicClassifier()
    numOfTest=10;currentNum=0;
    while True:
        print()
        print('Finding Random Choice of Music!')
        newValue=selector.randomSelect()
        if newValue==-10000:
            print()
            print('Music Data Has Run Out!')
            player.displayHistory()
            return
        
        if currentNum>=numOfTest:
            break
        currentNum+=1;print('Current Music Count:',str(currentNum))
        player.musicPlay(newValue)
           
    player.displayHistory()
    ##Saving the music model : ex)svm_RBFModel 
    classifier.binaryClassifier()
    classifier.saveClassifier()
    

def modelPredictionTester():
    print()
    print("Compare two models for testing prediction rate ")
    print()
    
    selector=MusicSelector();player=MusicPlayer();classifier=MusicClassifier()
    numOfTest=39;currentNum=0;
#    while True:
#        print()
#        print('Finding Random Choice of Music!')
#        newValue=selector.randomSelect()
#        if newValue==-10000:
#            print()
#            print('Music Data Has Run Out!')
#            player.displayHistory()
#            return
#        
#        if currentNum>=numOfTest:
#            break
#        currentNum+=1;print('Current Music Count:',str(currentNum))
#        player.musicPlayTwinSimuAnswer(modelDir1,modelDir2,newValue)
           
    for newValue in range(numOfTest):
        currentNum+=1;print('Current Music Count:',str(currentNum))
        player.musicPlayTwinSimuAnswer(modelDir1,modelDir2,newValue)
    player.displayPredict()
    ##Saving the music model : ex)svm_RBFModel 
    #classifier.binaryClassifier()
    #classifier.saveClassifier()


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
        if player.musicStopSimuAnswer():
            print()
            print('Thank You For Using The System!')
            player.displayHistory()
            return
        
        print('Making Model based on Past answer!')
        classifier.binaryClassifier();classifier.testClassifier(alpha);
        newMusicIndex=selector.mostFavSelect()
        if newMusicIndex==-10000:
            print('Music Data has run out!')
            break
        else:
            player.musicPlay(newMusicIndex)
    
    player.displayHistory()
    ##Saving the music model : ex)svm_RBFModel 
    #classifier.saveClassifier()
    
    
    ## feature selection needs to be set in util function.Y
def musicXorrRecommender():
    print()
    print("Music Simulator: Based On Response, It Will Find Your Favorites")
    print()
    
    selector=MusicSelector();player=MusicPlayer();classifier=MusicClassifier()
    
    print("Random Choice of Music")
    newRandomValue=selector.randomSelect()
    player.musicPlay(newRandomValue)
    while True:
        classifier.computeMeanFeatureXorrSum()
        newMusicValue=selector.minXorrSelect()
        if newMusicValue==-1:
            print('Music has run out!')
            break
        else:
            player.musicPlay(newMusicValue)
            
        
        
    
    
    
    
    
    
def musicSimulator(modelDir):
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
        #player.musicPlay(newValue)
        player.musicPlaySimuAnswer(modelDir,newValue)
        if len(selector.posMusic)>0 and len(selector.negMusic)>0:           
            break
    
    while True:
        if player.musicStopSimuAnswer():
            print()
            print('Thank You For Using The System!')
            player.displayHistory()
            return
        
        print('Making Model based on Past answer!')
        classifier.binaryClassifier();classifier.testClassifier(alpha);
        newMusicIndex=selector.mostFavSelect()
        if newMusicIndex==-10000:
            print('Music Data has run out!')
            break
        else:
            #player.musicPlay(newMusicIndex)
            player.musicPlaySimuAnswer(modelDir,newMusicIndex)
    
    player.displayHistory()
    ##Saving the music model : ex)svm_RBF_Model 
    #classifier.saveClassifier()
    
    

def musicRecommenderAlpha():
    print()
    print("Music Recommender: Recommends Music Based On Alpha Value:"+str(alpha))
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
        if player.musicStopSimuAnswer():
            print()
            print('Thank You For Using The System!')
            player.displayHistory()
            return
        
        print('Making Model based on Past answer!')
        classifier.binaryClassifier();classifier.testClassifier(alpha)
        newMusicIndex=selector.alphaModelSelect()
        if newMusicIndex==-10000:
            print('Music Data has run out!')
            break
        else:
            player.musicPlay(newMusicIndex)
    
    player.displayHistory()
    ##Saving the music model : ex)svm_RBFModel 
    #classifier.saveClassifier()
    

def musicSimulatorAlpha(modelDir):
    print()
    print("Music Recommender: Recommends Music Based On Alpha Value:"+str(alpha))
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
        player.musicPlaySimuAnswer(modelDir,newValue)
        if len(selector.posMusic)>0 and len(selector.negMusic)>0:           
            break
    
    while True:
        if player.musicStopSimuAnswer():
            print()
            print('Thank You For Using The System!')
            player.displayHistory()
            classifier.saveClassifier()
            return
        
        print('Making Model based on Past answer!')
        classifier.binaryClassifier();classifier.testClassifier(alpha);
        newMusicIndex=selector.alphaModelSelect()
        #newMusicIndex=selector.randomSelect()
        if newMusicIndex==-10000:
            print('Music Data has run out!')
            break
        else:
            player.musicPlaySimuAnswer(modelDir,newMusicIndex)
    
    
    player.displayHistory()
    classifier.saveClassifier()
    
        
    
    
#modelMaker()   
musicXorrRecommender()
#musicRecommender()
#musicSimulator(modelDir1)
#musicRecommenderAlpha()
#musicSimulatorAlpha(modelDir1)
#modelPredictionTester()
