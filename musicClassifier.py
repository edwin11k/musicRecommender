# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 16:09:49 2018

@author: edwin
"""

from musicHandler import *
from pyAudioAnalysis.audioTrainTest import *
from pyAudioAnalysis.audioFeatureExtraction import *
from util import *
import pickle
import os

## If set true, use a single mean data of features in 34 dimension instead of 500 data points.
useMean=True;
class MusicClassifier(MusicHandler):
    MLAlgorithm="SVM_RBF"
    # SVM Classifier for files in posMusic & negMusic
    
    
    def computeMeanFeatureXorrSum(self):
        ## save the xorr values with already tested music files
        # Empty previous information
        MusicHandler.xorrValueDic={}
        ## Remove music files already tested
        size=len(self.newFactory.musicFiles.fileData)
        fileIndex=list(range(size))
        for mem in MusicHandler.posMusic:
            fileIndex.remove(mem)
        for mem in MusicHandler.negMusic:
            fileIndex.remove(mem)
        for mem in MusicHandler.absMusic:
            fileIndex.remove(mem)
        
        bFeature=0;eFeature=34
        #tempolar 0-7, MFCC 8-20,chroma 21-32(chroma STD: 33)
        #If all features are included without normalization, MFCC often dominates
        for musicNum in fileIndex:
            xorrValue=0;
            ## Using average features, next 34 are standard deviation
            meanFeature=self.newFactory.musicFiles.mtFeatures[musicNum][bFeature:eFeature]
           
            for mem in MusicHandler.posMusic: 
                xorrValue+=simpleFeatureDis(meanFeature,self.newFactory.musicFiles.mtFeatures[mem][bFeature:eFeature],0,33)
            for mem in MusicHandler.negMusic:   
                xorrValue-=simpleFeatureDis(meanFeature,self.newFactory.musicFiles.mtFeatures[mem][bFeature:eFeature],0,33)
            MusicHandler.xorrValueDic[musicNum]=xorrValue
        print(MusicHandler.xorrValueDic)
        
        
    ##find data that are far from already labeled independant of the labels
    def computeMeanFeatureAbsXorrSum(self):
        ## save the xorr values with already tested music files
        # Empty previous information
        MusicHandler.xorrAbsValueDic={}
        ## Remove music files already tested
        size=len(self.newFactory.musicFiles.fileData)
        fileIndex=list(range(size))
        for mem in MusicHandler.posMusic:
            fileIndex.remove(mem)
        for mem in MusicHandler.negMusic:
            fileIndex.remove(mem)
        for mem in MusicHandler.absMusic:
            fileIndex.remove(mem)
        
        bFeature=0;eFeature=34
        #tempolar 0-7, MFCC 8-20,chroma 21-32(chroma STD: 33)
        #If all features are included without normalization, MFCC often dominates
        for musicNum in fileIndex:
            absXorrValue=0;
            ## Using average features, next 34 are standard deviation
            meanFeature=self.newFactory.musicFiles.mtFeatures[musicNum][bFeature:eFeature]
            print(meanFeature.shape)
            for mem in MusicHandler.posMusic: 
                absXorrValue+=simpleFeatureDis(meanFeature,self.newFactory.musicFiles.mtFeatures[mem][bFeature:eFeature],0,33)
            for mem in MusicHandler.negMusic:   
                absXorrValue+=simpleFeatureDis(meanFeature,self.newFactory.musicFiles.mtFeatures[mem][bFeature:eFeature],0,33)
            MusicHandler.xorrAbsValueDic[musicNum]=absXorrValue
        print(MusicHandler.xorrAbsValueDic)
    
    
    
    def binaryClassifier(self):
        #self.posMusic=[4];self.negMusic=[1,2]
        posFeature=[];negFeature=[];features=[]
        if MusicHandler.posMusic:
            for pIndex in MusicHandler.posMusic:
                if useMean:
                    posFeature.append(self.newFactory.musicFiles.meanStFeatures[pIndex])
                else:
                    posFeature.append(self.newFactory.musicFiles.stFeatures[pIndex])
                
        if MusicHandler.negMusic:
            for nIndex in MusicHandler.negMusic:   
                if useMean:
                    negFeature.append(self.newFactory.musicFiles.meanStFeatures[pIndex])
                else:
                    negFeature.append(self.newFactory.musicFiles.stFeatures[pIndex])
                
        
        features.append(posFeature);features.append(negFeature)
        features=featureStack(features)
        #print(features[0].shape,features[1].shape)
                    
        if self.MLAlgorithm=='SVM_RBF':
            print('SVM RBF Classifier')
            self.model=trainSVM_RBF(features,0.1)
        
        if self.MLAlgorithm=='SVM':
            print('SVM Linear Classifier')
            self.model=trainSVM(features,0.1)
            
        if self.MLAlgorithm=='RandomForest':
            print('Random Forest Classifier')
            self.model=trainRandomForest(features,100)
        
        if self.MLAlgorithm=='GradientBoosting':
            print('Gradient Boosting Classifier')
            self.model=trainGradientBoosting(features,100)
        
        if self.MLAlgorithm=='ExtraTrees':
            print('Extra Trees Classifier')
            self.model=trainExtraTrees(features,100)
            


    def saveClassifier(self):
        print('Model is being saved! This may take a while!')
        modelString=MusicHandler.defaultDir+os.sep+self.MLAlgorithm+'_Model';
        with open(modelString, 'wb') as fid:
                pickle.dump(self.model,fid)
        print(self.MLAlgorithm+' Model Has been Saved')         
        
    
    

            
    def testClassifier(self,alpha):
        trainTypes=['Like','Not Like'];
        features=self.newFactory.musicFiles.stFeatures
        featureList=list(range(len(self.newFactory.musicFiles.fileName)))
        #print(featureList,self.posMusic,self.negMusic)
        for mem in MusicHandler.posMusic:
            featureList.remove(mem)
        for mem in MusicHandler.negMusic:
            featureList.remove(mem)
        for mem in MusicHandler.absMusic:
            featureList.remove(mem)
        print(featureList,MusicHandler.posMusic,MusicHandler.negMusic,MusicHandler.absMusic)
        #print(MusicHandler.results)
        MusicHandler.results=[]
        for i,feature in enumerate(features):
            if i in featureList:
                feature=features[i];predict=[0,0]
                for j in range(len(feature[1])):
                    predict[int(self.model.predict(feature[:,j].reshape(1,-1)))]+=1
                MusicHandler.results.append((i,self.newFactory.musicFiles.fileName[i],predict,predict[0]/(predict[0]+predict[1]),abs(alpha-predict[0]/(predict[0]+predict[1])),trainTypes[argmax(predict)]))
        viewResults(MusicHandler.results)
        
