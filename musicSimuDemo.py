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
coXiter=10;



def dataViewPCA():
    print("Dimensional reduction & viewing the data")
    selector=MusicSelector();player=MusicPlayer();classifier=MusicClassifier()
    classifier.viewPCA(mode="MFCC_Chromatic")


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
    import random 
def refSVMvsCoWorkSVMTest():
    ## Reference SVM test to compare with
    
    print()
    print("SVM Training & Test")
    print()
    selector=MusicSelector();player=MusicPlayer();classifier=MusicClassifier()    
    print("TotalNumber of music in the folder:", selector.musicCount) 
    
    #music index Pool
    indexU=list(range(0,selector.musicCount-1))
    
    # Assign random test file from the pool
    numOfTestSample=40;print("Number of test samples: ",numOfTestSample)
    testIndex=random.sample(range(0,selector.musicCount-1),numOfTestSample)
    
    # remove testing file from the pool
    for mem in testIndex:
        if mem in indexU:
            indexU.remove(mem)
    
    # Collect separate response indexes in the index pool
    posUIndex=[];negUIndex=[]
    for mem in indexU:
        if MusicHandler.newFactory.musicFiles.like[mem]==True:
            posUIndex.append(mem)
        if MusicHandler.newFactory.musicFiles.like[mem]==False:
            negUIndex.append(mem)    
      
    # for each response, select same number of samples
    numOfPosTrain=20;numOfNegTrain=numOfPosTrain;   # total 21+21=42
    trainPosNum=random.sample(range(0,len(posUIndex)-1),numOfPosTrain)
    trainNegNum=random.sample(range(0,len(negUIndex)-1),numOfNegTrain)
    print("Number of train samples: ",numOfPosTrain+numOfNegTrain)
    
    # assign random training samples from the pool
    trainIndex=[]
    for mem in trainPosNum:
        trainIndex.append(posUIndex[mem])
    for mem in trainNegNum:
        trainIndex.append(negUIndex[mem])        
        
    selector.addMusicIndex(trainIndex)
    #print(MusicHandler.posMusic,MusicHandler.negMusic)
    classifier.binaryClassifierPCA(mode='MFCC_Chromatic')
    classifier.saveClassifier()
    classifier.validateClassifierPCA(testIndex,mode='MFCC_Chromatic')
    
 
    
    
    ''' CoWork Test. Do not use previous train test '''
    print("Co Work Test Using SVM: Two Features Group")
    print("Same Test data, but train data will be selected using algorithm")
    print("Features are divided into MFCC and Chromatic, tempolar will be ignored")
    ## Positive & Negative index from the pool UIndex
        
       
    beginRandomNumber=6;
    trainIndex=[]
    posRandomNumber=random.sample(range(0,len(posUIndex)-1),beginRandomNumber)
    negRandomNumber=random.sample(range(0,len(negUIndex)-1),beginRandomNumber)
     
    print("Test Index",testIndex)
    print("UIndex",indexU)
    print("Positive Random Number",posRandomNumber)
    print("Negative Random Number",negRandomNumber)
     
    ## pick same number of samples from pool & remove the samples from the pool
    for mem in posRandomNumber:
        trainIndex.append(posUIndex[mem]);indexU.remove(posUIndex[mem])
    for mem in negRandomNumber:
        trainIndex.append(negUIndex[mem]);indexU.remove(negUIndex[mem])
        
    print("Train Index",trainIndex)
    
    # Empty data from previous run
    MusicHandler.posMusic=[];MusicHandler.negMusic=[]
    selector.addMusicIndex(trainIndex)
    print("Positive Index:",MusicHandler.posMusic)
    print("Negative Index:",MusicHandler.negMusic)
    coXiter=7;
    print('Iteration Number :',coXiter)
    iterI=0;
    while iterI<coXiter:
        ## MFCC Data Addition
        classifier.binaryCoMLClassifierPCA(mode='MFCC',MLAlgorithm='SVM_Linear') 
        minMFCCIndex,maxMFCCIndex=selector.findMostOutDataPCA(indexU,ML='SVMLinear',mode='MFCC')
        print(minMFCCIndex,maxMFCCIndex)
        if minMFCCIndex!=None:
            MusicSelector.negMusic.append(minMFCCIndex);indexU.remove(minMFCCIndex)
        if maxMFCCIndex!=None:
            MusicSelector.posMusic.append(maxMFCCIndex);indexU.remove(maxMFCCIndex)
        print("Positive Index:",MusicHandler.posMusic);print("Negative Index:",MusicHandler.negMusic)
        
        ## Chromatic Data Addition
        classifier.binaryCoMLClassifierPCA(mode='Chromatic',MLAlgorithm='SVM_Linear')
        minChromaIndex,maxChromaIndex=selector.findMostOutDataPCA(indexU,ML='SVMLinear',mode='Chromatic')
        print(minChromaIndex,maxChromaIndex)
        if minChromaIndex!=None:
            MusicSelector.negMusic.append(minChromaIndex);indexU.remove(minChromaIndex)
        if maxChromaIndex!=None:
            MusicSelector.posMusic.append(maxChromaIndex);indexU.remove(maxChromaIndex)        
        print("Positive Index:",MusicHandler.posMusic);print("Negative Index:",MusicHandler.negMusic)
        iterI+=1
    print("Co work train sample number:",len(MusicHandler.posMusic)+len(MusicHandler.negMusic))
    classifier.binaryClassifierPCA(mode='MFCC_Chromatic')
    classifier.saveClassifier()
    classifier.validateClassifierPCA(testIndex,mode='MFCC_Chromatic')    
    print(classifier.validateResult)    

    
            
def musicCoWorktest(testIndex,Uindex):
    print()
    print("Co Work Test using SVM: Features are divided into two groups")
    print()
    
    selector=MusicSelector();player=MusicPlayer();classifier=MusicClassifier()
    totalNumber=selector.musicCount;iterI=0;
    
    print(totalNumber)  
    trainIndex=[4,6,7,11,12,17,18,21,23,26,28,29,30,34,35,36,37,38,39,40]
    trainInitIndex=[4,6,7,11,12,17,18,21]
    coXiter=5;
    testIndex=[0,1,2,3,5,8,9,10,13,14,15,16,19,20,22,24,25,27,31,32,33]
    
    print(len(trainIndex),len(testIndex))
    selector.addMusicIndex(trainInitIndex)
    print(MusicHandler.posMusic,MusicHandler.negMusic)
    ## coWork algorithm: Divide features into MFCC & Chromatic. Currently not using tempolar
    while iterI<coXiter:
        ## Binary classifier using MFCC features or Chromatic featurss
        classifier.binaryCoMLClassifier(mode='MFCC',MLAlgorithm='SVM_Linear')
        
        #find the most outlier date from the training pool
        minMFCCIndex,maxMFCCIndex=selector.findMostOutData(trainIndex,ML='SVMLinear',mode='MFCC')
        
        #Adding data if exists
        if minMFCCIndex!=None:
            MusicSelector.negMusic.append(minMFCCIndex)
        if maxMFCCIndex!=None:
            MusicSelector.posMusic.append(maxMFCCIndex)
             
        print('Pos',MusicSelector.posMusic);print('Neg',MusicSelector.negMusic)
                
        classifier.binaryCoMLClassifier(mode='Chromatic',MLAlgorithm='SVM_Linear')        
        minChromaIndex,maxChromaIndex=selector.findMostOutData(trainIndex,ML='SVMLinear',mode='Chromatic')
        if minChromaIndex!=None:
            MusicSelector.negMusic.append(minChromaIndex)
        if maxChromaIndex!=None:
            MusicSelector.posMusic.append(maxChromaIndex);
        print('Pos',MusicSelector.posMusic);print('Neg',MusicSelector.negMusic)
        iterI+=1
        
    classifier.validateClassifier(testIndex,mode='MFCC')
    classifier.validateClassifier(testIndex,mode='Chromatic')
    


def musicCowork():
    print()
    print("Random Musics are chosen for label")
    print()
    
    posSample=0;negSample=0;iterI=0;
    selector=MusicSelector();player=MusicPlayer();classifier=MusicClassifier()
    size=len(self.newFactory.musicFiles.fileData) # size of the music data files 
    # Later label may be assigned in different form
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
        if len(selector.posMusic)>posSample and len(selector.negMusic)>negSample:           
            break
    while iterI<coXiter:
        classifier.binaryCoMLClassifier(mode='MFCC',MLAlgorithm='SVM_Linear')
        classifier.binaryCoMLClassifier(mode='Chromatic',MLAlgorithm='SVM_Linear')
        # Find data that are the most outside located from decision boundary
        minMFCCIndex,maxMFCCIndex=selector.findMostOutData(indexPool=list(range(size)), ML='SVMLinear',mode='MFCC')
        MusicSelector.posMusic.append(maxMFCCIndex);MusicSelector.negMusic.append(minMFCCIndex)
        print('Pos',MusicSelector.posMusic);print('Neg',MusicSelector.negMusic)
        classifier.binaryCoMLClassifier(mode='Chromatic',MLAlgorithm='SVM_Linear')
        minChromaIndex,maxChromaIndex=selector.findMostOutData(indexPool=list(range(size)),ML='SVMLinear',mode='Chromatic')
        MusicSelector.posMusic.append(maxChromaIndex);MusicSelector.negMusic.append(minChromaIndex)
        print('Pos',MusicSelector.posMusic);print('Neg',MusicSelector.negMusic)
        iterI+=1
    
    
    classifier.saveClassifier("coSVM_MFCC","MFCC")
    classifier.saveClassifier("coSVM_Chromatic","Chromatic")
    
    
    
    
    

    
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




#dataViewPCA()    
#musicCoWorktest()       
refSVMvsCoWorkSVMTest()
#musicCowork()
#modelMaker()   
#musicXorrRecommender()
#musicRecommender()
#musicSimulator(modelDir1)
#musicRecommenderAlpha()
#musicSimulatorAlpha(modelDir1)
#modelPredictionTester()
