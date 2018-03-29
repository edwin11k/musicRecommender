# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 11:18:49 2018

@author: edwin
"""


from musicHandler import *
from pydub import AudioSegment
from pydub.playback import play
from musicUser import *
from util import *

playDuration=20;bPlay=False

class MusicPlayer(MusicHandler):
    
    # Plays the music located at the index given & then obtains boolean input for likability
 
    user1=MusicUser();user2=MusicUser()
    def musicPlay(self,fileIndex,thumbNail=True):
        print()
        print('Music Playing Initiated!')
        MusicHandler.newFactory.musicFiles.printMusicInfo(fileIndex)
        
        song=AudioSegment.from_file(self.newFactory.musicFiles.filePath[fileIndex])
        if thumbNail:
            #print('Thumbnail Music Clip!')
            B,E=MusicHandler.newFactory.musicFiles.thumbNail[fileIndex]
            print(B,E)
        else:
            B=0;E=B+playDuration
            
        song=song[int(1000*B):int(1000*E)];
            
        if bPlay:
           play(song) 
        response=''
        while True:
            answer=input('Do you like the music(Yes|No|Abstain)?[Y|N|A]')
            
            if answer=='Y':
                MusicHandler.posMusic.append(fileIndex);response='YES'
                break
            if answer=='N':
                MusicHandler.negMusic.append(fileIndex);response='NO'
                break
            if answer=='A':
                MusicHandler.absMusic.append(fileIndex);response='ABSTAIN'
                break
            print ('Wrong Input: Answer Must Be N,Y,or A')
        
        
        MusicHandler.history[MusicHandler.newFactory.musicFiles.fileName[fileIndex]]=response
        #print(MusicHandler.history)
        

    def musicPlaySimuAnswer(self,modelDir,fileIndex,thumbNail=True):
        print()
        print('Music Playing Initiated!')
        MusicHandler.newFactory.musicFiles.printMusicInfo(fileIndex)
        
        song=AudioSegment.from_file(self.newFactory.musicFiles.filePath[fileIndex])
        if thumbNail:
            B,E=MusicHandler.newFactory.musicFiles.thumbNail[fileIndex]
        else:
            B=0;E=B+playDuration       
        song=song[1000*B:1000*E];
        
        if bPlay:
           play(song) 
        
        response=''
        while True:
            print('Do you like the music(Yes|No|Abstain)?[Y|N|A]')         
            #answer=self.user.randomAnswer()
            answer=self.user1.prevModelAnswer(fileIndex,modelDir)
            print('Your Answer is ',answer)
            
            if answer=='Y':
                MusicHandler.posMusic.append(fileIndex);response='YES'
                break
            if answer=='N':
                MusicHandler.negMusic.append(fileIndex);response='NO'
                break
            if answer=='A':
                MusicHandler.absMusic.append(fileIndex);response='ABSTAIN'
                break
            print ('Wrong Input: Answer Must Be N,Y,or A')
        
        
        MusicHandler.history[MusicHandler.newFactory.musicFiles.fileName[fileIndex]]=response
        #print(MusicHandler.history)        


    def musicPlayTwinSimuAnswer(self,modelDir1,modelDir2,fileIndex,thumbNail=True):
        print()
        print('Music Playing Initiated!')
        MusicHandler.newFactory.musicFiles.printMusicInfo(fileIndex)
        
        song=AudioSegment.from_file(self.newFactory.musicFiles.filePath[fileIndex])
        if thumbNail:
            B,E=MusicHandler.newFactory.musicFiles.thumbNail[fileIndex]
        else:
            B=0;E=B+playDuration       
        song=song[1000*B:1000*E];
        
        if bPlay:
           play(song) 
        
        response=''
        while True:
            print('Do you like the music(Yes|No|Abstain)?[Y|N|A]')         
            #answer=self.user.randomAnswer()
            answer=self.user1.prevModelAnswer(fileIndex,modelDir1)
            answer2=self.user2.prevModelAnswer(fileIndex,modelDir2)
            print('User Answer is ',answer)
            print('Algorithm Answer is ',answer2)
            if answer==answer2:
                MusicHandler.predictRate+=1
            
            if answer=='Y':
                MusicHandler.posMusic.append(fileIndex);response='YES'
                break
            if answer=='N':
                MusicHandler.negMusic.append(fileIndex);response='NO'
                break
            if answer=='A':
                MusicHandler.absMusic.append(fileIndex);response='ABSTAIN'
                break
            print ('Wrong Input: Answer Must Be N,Y,or A')
        
        
        MusicHandler.history[MusicHandler.newFactory.musicFiles.fileName[fileIndex]]=response
        
    def musicStop(self):        
        while True:
            cAnswer=input('Do You Want To Listen To The Next Song(Yes|No)?[Y|N]')
            if cAnswer=='Y':
                return False
            if cAnswer=='N':
                return True
            print ('Wrong Input: Answer Must Be N or Y')        
        
    def musicStopSimuAnswer(self):        
        while True:
            print('Do You Want To Listen To The Next Song(Yes|No)?[Y|N]')
            cAnswer=self.user1.musicStopAnswer()
            if cAnswer=='Y':
                return False
            if cAnswer=='N':
                return True
            print ('Wrong Input: Answer Must Be N or Y')     
            
    def displayPredict(self):
        totalNumber=len(MusicHandler.posMusic)+len(MusicHandler.negMusic)+len(MusicHandler.absMusic)
        print()
        print('Display The User Choice History')
        print()
        print('Music Play History: (Title: User Choice)')
        for key,value in MusicHandler.history.items():
            print ('{} : {}'.format(key,value))
        print()
        print('User & Model Matched {} out of {} songs'.format(str(MusicHandler.predictRate),str(totalNumber)))
        print('Total prediction Percentage:{:.3f} %'.format(MusicHandler.predictRate*100/totalNumber))
            
                    
            
    def displayHistory(self):
        totalNumber=len(MusicHandler.posMusic)+len(MusicHandler.negMusic)+len(MusicHandler.absMusic)
        print()
        print('Display The User Choice History')
        print()
        print('Music Play History: (Title: User Choice)')
        for key,value in MusicHandler.history.items():
            print ('{} : {}'.format(key,value))
        print('User Liked {} ,disliked {}, abstained {} out of {} songs'.format(str(len(MusicHandler.posMusic)),str(len(MusicHandler.negMusic)),str(len(MusicHandler.absMusic)),str(totalNumber)))
        print('Total Favor Percentage:{:.3f} %'.format(len(MusicHandler.posMusic)*100/totalNumber))
            
            
            
        
