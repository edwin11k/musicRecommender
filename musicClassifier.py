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
    #MLAlgorithm="SVM_RBF"
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
    



    """ Vanilla binary Classifier"""
    def binaryClassifier(self,mode=None):
        self.MLAlgorithm='SVM'
        
        posFeature=[];negFeature=[];features=[]
        if MusicHandler.posMusic:
            for pIndex in MusicHandler.posMusic:
                if mode==None:
                    posFeature.append(self.newFactory.musicFiles.mtFeatures[pIndex])    
                elif mode=='MFCC_Chromatic':
                    posFeature.append(self.newFactory.musicFiles.mtFeatures[pIndex][8:33])   
                else:
                    print("Please enter valid mode");
                    
        if MusicHandler.negMusic:
            for nIndex in MusicHandler.negMusic:  
                if mode==None:
                    negFeature.append(self.newFactory.musicFiles.mtFeatures[pIndex])
                elif mode=='MFCC_Chromatic':
                    negFeature.append(self.newFactory.musicFiles.mtFeatures[pIndex][8:33])
                else:
                    print("Please enter valid mode")
                
        features.append(posFeature);features.append(negFeature)
        #print(features)
        print(len(features),features[0][0].shape,features[1][0].shape)
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
            
            
            

    """ Vanilla binary Classifier using 2D PCA reduced data"""
    def binaryClassifierPCA(self,mode=None):
        self.MLAlgorithm='SVM'
        
        posFeature=[];negFeature=[];features=[]
        if MusicHandler.posMusic:
            for pIndex in MusicHandler.posMusic:
                if mode==None:
                    posFeature.append(self.newFactory.musicFiles.mtFeaturesFullPCA[pIndex])    
                elif mode=='MFCC_Chromatic':
                    posFeature.append(self.newFactory.musicFiles.mtFeaturesMFCCChromaticPCA[pIndex])   
                else:
                    print("Please enter valid mode");
                    
        if MusicHandler.negMusic:
            for nIndex in MusicHandler.negMusic:  
                if mode==None:
                    negFeature.append(self.newFactory.musicFiles.mtFeaturesFullPCA[pIndex])
                elif mode=='MFCC_Chromatic':
                    negFeature.append(self.newFactory.musicFiles.mtFeaturesMFCCChromaticPCA[pIndex])
                else:
                    print("Please enter valid mode")
                
           
        features.append(posFeature);features.append(negFeature)
        #print(features)
        print(len(features),features[0][0].shape,features[1][0].shape)
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


    
    """ Binary co Work Classifier """
    def binaryCoMLClassifier(self,mode='MFCC',MLAlgorithm='SVM_Linear'):
        #self.posMusic=[4];self.negMusic=[1,2]
        posFeature=[];negFeature=[];features=[]
        
        if mode=='MFCC':
            bIndex=9;eIndex=21;
        if mode=='Chromatic':
            bIndex=22;eIndex=33;
        if mode=='Tempolar':
            bIndex=1;eIndex=8;
            
        if MusicHandler.posMusic:
            for pIndex in MusicHandler.posMusic:
                if pIndex!=None:
                    posFeature.append(self.newFactory.musicFiles.mtFeatures[pIndex][bIndex-1:eIndex])
                                      
        if MusicHandler.negMusic:
            for nIndex in MusicHandler.negMusic: 
                if nIndex!=None:
                    negFeature.append(self.newFactory.musicFiles.mtFeatures[nIndex][bIndex-1:eIndex])
                
        ## zero= True, one=false
        features.append(posFeature);features.append(negFeature)
        print('Features(positive,negative):',len(posFeature),len(negFeature))     
        features=featureStack(features)
        
        if MLAlgorithm=='SVM_RBF':
            print('SVM RBF Classifier')
            if mode=='MFCC':
                MusicHandler.modelMFCC=trainSVM_RBF(features,0.1)
            if mode=='Chromatic':
                MusicHandler.modelChromatic=trainSVM_RBF(features,0.1)
            if mode=='Tempolar':
                MusicHandler.modelTempolar=trainSVM_RBF(features,0.1)
            
                
        if MLAlgorithm=='SVM_Linear':    
            if mode=='MFCC':
                MusicHandler.modelMFCC=trainSVM(features,0.1)
                print('SVM Linear Classifier with MFCC features')
            if mode=='Chromatic':
                MusicHandler.modelChromatic=trainSVM(features,0.1)
                print('SVM Linear Classifier with Chromatic features')
            if mode=='Tempolar':
                MusicHandler.modelTempolar=trainSVM(features,0.1)
                print('SVM Linear Classifier with Tempolar features')
                
        if MLAlgorithm=='RandomForest':
            print('Random Forest Classifier')
            if mode=='MFCC':
                MusicHandler.modelMFCC=trainRandomForest(features,100)
            if mode=='Chromatic':
                MusicHandler.modelChromatic=trainRandomForest(features,100)
            if mode=='Tempolar':
                MusicHandler.modelTempolar=trainRandomForest(features,100)

        if MLAlgorithm=='GradientBoosting':
            print('Gradient Boosting Classifier')
            if mode=='MFCC':
                MusicHandler.modelMFCC=trainGradientBoosting(features,100)
            if mode=='Chromatic':
                MusicHandler.modelChromatic=trainGradientBoosting(features,100)
            if mode=='Tempolar':
                MusicHandler.modelTempolar=trainGradientBoosting(features,100)
                

        if MLAlgorithm=='ExtraTrees':
            print('Extra Trees Classifier')
            if mode=='MFCC':
                MusicHandler.modelMFCC=trainExtraTrees(features,100)
            if mode=='Chromatic':
                MusicHandler.modelChromatic=trainExtraTrees(features,100)
            if mode=='Tempolar':
                MusicHandler.modelTempolar=trainExtraTrees(features,100)
                
                
                
    
    """ Binary co Work Classifier """
    def binaryCoMLClassifierPCA(self,mode='MFCC',MLAlgorithm='SVM_Linear'):
        #self.posMusic=[4];self.negMusic=[1,2]
        posFeature=[];negFeature=[];features=[]
        
        if mode=='MFCC':
            musicFeatures=self.newFactory.musicFiles.mtFeaturesMFCCPCA
        if mode=='Chromatic':
            musicFeatures=self.newFactory.musicFiles.mtFeaturesChromaticPCA
        if mode=='Tempolar':
            musicFeatures=self.newFactory.musicFiles.mtFeaturesTempPCA
            
        if MusicHandler.posMusic:
            for pIndex in MusicHandler.posMusic:
                if pIndex!=None:
                    posFeature.append(musicFeatures[pIndex])
                                      
        if MusicHandler.negMusic:
            for nIndex in MusicHandler.negMusic: 
                if nIndex!=None:
                    negFeature.append(musicFeatures[pIndex])
                
        ## zero= True, one=false
        features.append(posFeature);features.append(negFeature)
        print('Features(positive,negative):',len(posFeature),len(negFeature))     
        features=featureStack(features)
        
        if MLAlgorithm=='SVM_RBF':
            print('SVM RBF Classifier')
            if mode=='MFCC':
                MusicHandler.modelMFCC=trainSVM_RBF(features,0.1)
            if mode=='Chromatic':
                MusicHandler.modelChromatic=trainSVM_RBF(features,0.1)
            if mode=='Tempolar':
                MusicHandler.modelTempolar=trainSVM_RBF(features,0.1)
            
                
        if MLAlgorithm=='SVM_Linear':    
            if mode=='MFCC':
                MusicHandler.modelMFCC=trainSVM(features,0.1)
                print('SVM Linear Classifier with MFCC features')
            if mode=='Chromatic':
                MusicHandler.modelChromatic=trainSVM(features,0.1)
                print('SVM Linear Classifier with Chromatic features')
            if mode=='Tempolar':
                MusicHandler.modelTempolar=trainSVM(features,0.1)
                print('SVM Linear Classifier with Tempolar features')
                
        if MLAlgorithm=='RandomForest':
            print('Random Forest Classifier')
            if mode=='MFCC':
                MusicHandler.modelMFCC=trainRandomForest(features,100)
            if mode=='Chromatic':
                MusicHandler.modelChromatic=trainRandomForest(features,100)
            if mode=='Tempolar':
                MusicHandler.modelTempolar=trainRandomForest(features,100)

        if MLAlgorithm=='GradientBoosting':
            print('Gradient Boosting Classifier')
            if mode=='MFCC':
                MusicHandler.modelMFCC=trainGradientBoosting(features,100)
            if mode=='Chromatic':
                MusicHandler.modelChromatic=trainGradientBoosting(features,100)
            if mode=='Tempolar':
                MusicHandler.modelTempolar=trainGradientBoosting(features,100)
                

        if MLAlgorithm=='ExtraTrees':
            print('Extra Trees Classifier')
            if mode=='MFCC':
                MusicHandler.modelMFCC=trainExtraTrees(features,100)
            if mode=='Chromatic':
                MusicHandler.modelChromatic=trainExtraTrees(features,100)
            if mode=='Tempolar':
                MusicHandler.modelTempolar=trainExtraTrees(features,100)
                            


    def saveClassifier(self,modelString=None,model=None):
        print('Model is being saved! This may take a while!')
        if modelString==None:
            modelString=MusicHandler.defaultDir+os.sep+self.MLAlgorithm+'_Model';
        else:
            modelString=MusicHandler.defaultDir+os.sep+modelString;
        
        with open(modelString, 'wb') as fid:
            if model==None:
                pickle.dump(self.model,fid)
            if model=="Chromatic":
                pickle.dump(MusicHandler.modelChromatic,fid)
            if model=="MFCC":
                pickle.dump(MusicHandler.modelMFCC,fid)
            
        print(' Model Has been Saved')         
        
    
    

            
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
        
  
            
    def validateClassifier(self,testIndex,mode=None):   
        classifierModel=None
        if mode==None:
            begin=0;end=34;classifierModel=self.model
        elif mode=="MFCC_Chromatic":
            begin=8;end=33;classifierModel=self.model
        elif mode=='MFCC':
            begin=8;end=21;classifierModel=MusicHandler.modelMFCC
        elif mode=='Chromatic':
            begin=21;end=33;classifierModel=MusicHandler.modelChromatic
        features=self.newFactory.musicFiles.mtFeatures
        total=0;correct=0
        for i,feature in enumerate(features):
            if i in testIndex:        
                #print(features[i][0:34].reshape(1,-1))
                #result[i]=self.model.predict(features[i][0:34].reshape(1,-1))
                #print(i,self.newFactory.musicFiles.like[i])
                if(self.newFactory.musicFiles.like[i]==classifierModel.predict(features[i][begin:end].reshape(1,-1))):
                    correct+=1
                    print(self.newFactory.musicFiles.like[i],classifierModel.predict(features[i][begin:end].reshape(1,-1)))
                total+=1
        print("Value:",correct/total)

 
    def validateClassifierPCA(self,testIndex,mode=None):   
        classifierModel=None
        if mode==None:
            classifierModel=self.model;features=self.newFactory.musicFiles.mtFeaturesFullPCA
        elif mode=="MFCC_Chromatic":
            classifierModel=self.model;features=self.newFactory.musicFiles.mtFeaturesMFCCChromaticPCA
        elif mode=='MFCC':
            classifierModel=MusicHandler.modelMFCC;features=self.newFactory.musicFiles.mtFeaturesMFCCPCA
        elif mode=='Chromatic':
            classifierModel=MusicHandler.modelChromatic;features=self.newFactory.musicFiles.mtFeaturesChromaticPCA
        
        total=0;correct=0
        for i,feature in enumerate(features):
            if i in testIndex:        
                if(self.newFactory.musicFiles.like[i]==classifierModel.predict(features[i].reshape(1,-1))):
                    correct+=1
                    print(self.newFactory.musicFiles.like[i],classifierModel.predict(features[i].reshape(1,-1)))
                total+=1
        print("Value:",correct/total)       
   
        
        
    def viewPCA(self,mode="Full"):  
        xPdata=[];yPdata=[]
        xNdata=[];yNdata=[]
        if mode=="Full":
            features=self.newFactory.musicFiles.mtFeaturesFullPCA
        if mode=="Tempolar":
            features=self.newFactory.musicFiles.mtFeaturesTempPCA
        if mode=="MFCC":
            features=self.newFactory.musicFiles.mtFeaturesMFCCPCA
        if mode=="Chromatic":
            features=self.newFactory.musicFiles.mtFeaturesChromaticPCA            
        if mode=="MFCC_Chromatic":
            features=self.newFactory.musicFiles.mtFeaturesMFCCChromaticPCA
            
        Likes=self.newFactory.musicFiles.like    
        for i,mem in enumerate(features):
            if Likes[i]==True:
                xPdata.append(mem[0]);yPdata.append(mem[1])
            else:
                xNdata.append(mem[0]);yNdata.append(mem[1])
            
        plt.scatter(xPdata,yPdata,color="red")
        plt.scatter(xNdata,yNdata,color="blue")
        
        
            
        
        
        
