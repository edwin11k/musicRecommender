# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 12:36:32 2018

@author: edwin
"""

from musicHandler import *
import random 
import os


class MusicUser(MusicHandler):
    print("Simulated User Experience!")
    
    def randomAnswer(self):
        randomNum=random.randint(-1,1);
        if randomNum==-1:
            return "N";
        elif randomNum==1:
            return "Y";
        else:
            return "A"
        
    def prevModelAnswer(self,fileNum,modelDir,MLAlgorithm='SVM_RBF'):
        #loading the pre-existing model
        fileName=modelDir+os.sep+MLAlgorithm+'_Model'
        with open(fileName,'rb') as fid:
            model=pickle.load(fid)
        feature=self.newFactory.musicFiles.stFeatures[fileNum]
        predict=[0,0]
        for j in range(len(feature[1])):
            predict[int(model.predict(feature[:,j].reshape(1,-1)))]+=1
        print(predict)
        total=predict[0]+predict[1];
        ### IF user likes more than 60% segments, give positive response
        if predict[0]/total>0.55:
            return "Y"
        ### negative reponse if like less than 40%
        elif predict[0]/total<0.45:
            return "N"
        ### abstain between 40~60
        else:
            return "A"
       
        
        
    
    def musicStopAnswer(self):
        if True:
            return 'Y'
        else:
            return 'N'
        
    
    