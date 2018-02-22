#from pyAudioAnalysis.audioVisualization import *
from pyAudioAnalysis.audioBasicIO import *
import matplotlib.pyplot as plt
from pyAudioAnalysis.audioFeatureExtraction import *
from pyAudioAnalysis.audioSegmentation import *
from pyAudioAnalysis.audioVisualization import *
from pyAudioAnalysis.audioTrainTest import *
import os
import pickle




class Music(object): 
    """ Music object reading files
    
    Within the given directory, the class will read all the files
    
    """
      
    def __init__(self,dirPath=os.curdir,music_genre=None,window=0.4,step=0.4):
        self.dirPath=dirPath
        self.genre=music_genre
        self.fileName=[]
        self.fileData=[]
        self.Fs=[]
        self.stFeatures=[]
        self.fileInfo=[]
        self.filePath=[]
        print()      
        try:
            fo=open(dirPath+os.sep+'musicDataFile','rb')
            self.genre=pickle.load(fo)
            self.fileName=pickle.load(fo)
            self.fileData=pickle.load(fo)
            self.Fs=pickle.load(fo)
            self.stFeatures=pickle.load(fo)
            self.fileInfo=pickle.load(fo)
            self.filePath=pickle.load(fo)
            fo.close()
            print('Previous Music Data File Exists & Loading the File')
        except:
            print('No Music Data File Exists, Begin Reading!')
            for file in os.listdir(dirPath):
                [fs,x]=readAudioFile(dirPath+os.sep+file);x=stereo2mono(x)   
            ## pydub seems to have already adjusted the frequency sampling for multi channel, hence commented out
#            # If the signal is multichannel, reduce it down to mono for analysis
#            channel=x.shape[1]
#            if x.ndim>1:
#                x=stereo2mono(x);fs=int(fs/channel)
                if music_genre=='Speech':
                    print(music_genre+" File Read Located At :"+dirPath+os.sep+file)
                else:
                    print(music_genre+" Music File Read Located At :"+dirPath+os.sep+file)
                
                x=x[:fs*60]
                
                self.fileData.append(x);self.Fs.append(fs)
                self.stFeatures.append(stFeatureExtraction(x,fs,window*fs,step*fs)) 
                self.fileName.append(file)
                self.filePath.append(dirPath+os.sep+file)
                # fileName, Sample Frame Rate, window duration, total duration,data Points from file
                info=(file,fs,window,window*fs,x.shape[0]/fs,int(x.shape[0]/(step*fs)))
                self.fileInfo.append(info)
        print(self)


    def __str__(self):   
        for i,mem in enumerate(self.fileInfo):
            print()
            print('File '+str(i+1)+':')
            print('File Name:',mem[0])
            print('File Sampling Rate:',mem[1])
            print('Time Duration of each window:',mem[2],' sec')
            print('Sample Number in each window:',mem[3])
            print('Total Duration:',mem[4],'sec')
            print('Data points from the file:',mem[5])
        return 'Music Type:'+self.genre
                            
    
    def printMusicInfo(self,index):
        print()
        print('----Music Information--------------------')
        print('File # '+str(index+1))
        print('Title: ',self.fileInfo[index][0])
        print('Duration:',str(int(self.fileInfo[index][4]))+' sec')
        print('-----------Enjoy The Music --------------')
    
    
    def saveMusicInfo(self):
        if os.path.isfile(self.dirPath+os.sep+'musicDataFile'):
            print()
            print('Previously Saved Music File Exists!')
            print('If you want to update Model with New Music File, erase the file in the folder and run the program again')
        else:
            print()
            print('Saving Music Data File')
            print('This May Take a While. Please Be Patient')
            fo = open(self.dirPath+os.sep+'musicDataFile', "wb")
            pickle.dump(self.genre,fo,protocol=pickle.HIGHEST_PROTOCOL)
            pickle.dump(self.fileName,fo,protocol=pickle.HIGHEST_PROTOCOL)
            pickle.dump(self.fileData,fo,protocol=pickle.HIGHEST_PROTOCOL)
            pickle.dump(self.Fs,fo,protocol=pickle.HIGHEST_PROTOCOL)
            pickle.dump(self.stFeatures,fo,protocol=pickle.HIGHEST_PROTOCOL)
            pickle.dump(self.fileInfo,fo,protocol=pickle.HIGHEST_PROTOCOL)
            pickle.dump(self.filePath,fo,protocol=pickle.HIGHEST_PROTOCOL)
            fo.close()
            print('New Music Data File Has Been Saved!')
            
