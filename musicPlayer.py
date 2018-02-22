# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 11:18:49 2018

@author: edwin
"""


from musicHandler import *
from pydub import AudioSegment
from pydub.playback import play


class MusicPlayer(MusicHandler):
    
    # Plays the music located at the index given & then obtains boolean input for likability
    def musicPlay(self,fileIndex):
        print()
        print('Music Playing Initiated!')
        MusicHandler.newFactory.musicFiles.printMusicInfo(fileIndex)
        song=AudioSegment.from_file(self.newFactory.musicFiles.filePath[fileIndex])
        play(song[:1000*60])
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
        

        
    def musicStop(self):        
        while True:
            cAnswer=input('Do You Want To Listen To The Next Song(Yes|No)?[Y|N]')
            if cAnswer=='Y':
                return False
            if cAnswer=='N':
                return True
            print ('Wrong Input: Answer Must Be N or Y')        
        
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
            
            
            
        
