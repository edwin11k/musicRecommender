# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 19:15:19 2018

@author: edwin
"""
from pyAudioAnalysis.audioSegmentation import *
from pyAudioAnalysis.audioBasicIO import *
import matplotlib.pyplot as plt
from pydub import AudioSegment
from musicHandler import *
import numpy as np
import logging


    

def loadMusicFeatures(listMusic,listDir,window,windowStep):
    musicFeatures=[]
    newFactory=musicFactory()
    for i, mem in enumerate(listMusic):
        if window[i]==None and windowStep[i]==None:
            Music=newFactory.loadMusic(mem,listDir[i])
        else:
            logging.warning('New Step And Window Size Assigned!')
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
        
# Music Duration must be less than 40sec,,
def thumbNailProcess(inputFile,musicDuration=20):
    [Fs, x] = readAudioFile(inputFile)
    [A1, A2, B1, B2,S] = musicThumbnailing(x, Fs,thumbnailSize=musicDuration)
    print(A1,A2)
    
    return A1
        
#find the peak of cross-correlation between two music features
import scipy as sp
def xorrFeatureMax(feature1,feature2,window,step=1):
    size1=len(feature1);size2=len(feature2);
    maxValue=0;
    if window>size1 or window>size2:
        print('Window size is too large')
        return 0
    for i in range(0,size1-window,step):
        for j in range(0,size2-window,step):
            xorrValue=sp.correlate(feature1[i:(i+window)],feature2[i:(i+window)])
            if xorrValue>maxValue:
                maxValue=xorrValue
    return maxValue

import math
def xorrFeatureVec(feature1,feature2,window,step,begin,end):
    distanceVec=[]
    sumDistance=0
    numOfFeature=len(feature1)
    for i in range(begin,end):
        featureDist=xorrFeatureMax(feature1[i],feature2[i],window,step)
        distanceVec.append(featureDist)
        sumDistance+=featureDist*featureDist
    return distanceVec,math.sqrt(sumDistance)
        
    
## seem to be already normalized.
def featureWhitten(feature):
    numOfFeature=len(feature)
    newFeature=[]
    for i in range(numOfFeature):
        newFeature.append((feature[i]-mean(feature[i]))/std(feature[i]))
    return newFeature
    
    
