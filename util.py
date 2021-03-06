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
        
    
## all 0-33 ;tempolar 0-7 ;MFCC 8-20;Chromatic 21-33
## MFCC Contribution dominates. 
def simpleFeatureDis(meanFeature1,meanFeature2,bFeat=0,eFeat=33):
    if(len(meanFeature1)!=len(meanFeature2)):
        print("Warning: The size of the features are not the same")
    return sum((meanFeature1[bFeat:eFeat]-meanFeature2[bFeat:eFeat])*(meanFeature1[bFeat:eFeat]-meanFeature2[bFeat:eFeat]))


 
