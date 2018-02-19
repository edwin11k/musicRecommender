# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 16:09:49 2018

@author: edwin
"""

from musicHandler import *
from pyAudioAnalysis.audioTrainTest import *
from pyAudioAnalysis.audioFeatureExtraction import *
from util import *
import _pickle

class MusicClassifier(MusicHandler):
    window=0.4; step=0.4;MLAlgorithm="SVM_RBF"
    # SVM Classifier for files in posMusic & negMusic
    def binaryClassifier(self):
        #self.posMusic=[4];self.negMusic=[1,2]
        posFeature=[];negFeature=[];features=[]
        
        if self.MLAlgorithm=='SVM_RBF':
            print('SVM RBF Classifier')
            if MusicHandler.posMusic:
                for pIndex in MusicHandler.posMusic:
                    posFeature.append(self.newFactory.musicFiles.stFeatures[pIndex])
            if MusicHandler.negMusic:
                for nIndex in MusicHandler.negMusic:
                    negFeature.append(self.newFactory.musicFiles.stFeatures[nIndex])
        
        features.append(posFeature);features.append(negFeature)
        features=featureStack(features)
        #print(features[0].shape,features[1].shape)
        self.model=trainSVM_RBF(features,0.1)
        
        
    def testClassifier(self):
        trainTypes=['Like','Not Like'];
        features=self.newFactory.musicFiles.stFeatures
        featureList=list(range(len(self.newFactory.musicFiles.fileName)))
        print(featureList,self.posMusic,self.negMusic)
        for mem in self.posMusic:
            featureList.remove(mem)
        for mem in self.negMusic:
            featureList.remove(mem)
        print(featureList,self.posMusic,self.negMusic)
        print(MusicHandler.results)
        MusicHandler.results=[]
        for i,feature in enumerate(features):
            if i in featureList:
                feature=features[i];predict=[0,0]
                for j in range(len(feature[1])):
                    predict[int(self.model.predict(feature[:,j].reshape(1,-1)))]+=1
                MusicHandler.results.append((i,self.newFactory.musicFiles.fileName[i],predict,predict[0]/(predict[0]+predict[1]),trainTypes[argmax(predict)]))
        viewResults(MusicHandler.results)
        
    

#A=MusicClassifier();A.binaryClassifier();A.testClassifier()




