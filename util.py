# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 19:15:19 2018

@author: edwin
"""
from musicHandler import *
import numpy as np


    

def loadMusicFeatures(listMusic,listDir,window,windowStep):
    musicFeatures=[]
    newFactory=musicFactory()
    for i, mem in enumerate(listMusic):
        if window[i]==None and windowStep[i]==None:
            Music=newFactory.loadMusic(mem,listDir[i])
        else:
            print('Warning : New Step and Window size assigned!')
            Music=newFactory.loadMusic(mem,listDir[i],window[i],windowStep[i])
        musicFeatures.append(Music.stFeatures)   
    print('Music Features are loaded')
    return musicFeatures



def displayMusicInfo(musicType,listDir,window,windowStep):
    for i,dir1 in enumerate(listDir):
        newFactory=musicFactory();newFactory.loadMusic(music_genre=musicType[i],directory=dir1,window1=window[i],step1=windowStep[i])
        #newFactory.printMusicFileInfo()
    
    


# Stack the features from various sources in the genre, & Transpose is needed to use list of features
def featureStack(features):
    matrixFeatures=[]
    for feat in features:
        matrixFeatures.append((np.hstack(feat)).T)
    #[matrixFeatures, MEAN, STD] = normalizeFeatures(matrixFeatures)
    return matrixFeatures



def viewResults(results):
    for mem in results:
        print (mem)
        
        
def multiSVM(listMusic,listDir,window,step,RBF):
    features=featureStack(loadMusicFeatures(listMusic,listDir,window,step))
    print()
    print('SVM Model Fitting Initiated! This may take a while~')
    if RBF:
        svm=trainSVM_RBF(features,0.1)
    else:
        svm=trainSVM(features,0.1)
    print('SVM Training Completed!')
    return svm