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
        print('Music Playing Initiated!')
        MusicHandler.newFactory.musicFiles.printMusicInfo(fileIndex)
        play(AudioSegment.from_file(self.newFactory.musicFiles.filePath[fileIndex]))
        
        while True:
            answer=input('Do you like the music(Yes|No|Abstain)?[Y|N|A]')
            print()
            if answer=='Y':
                MusicHandler.posMusic.append(fileIndex)
                return True
            if answer=='N':
                MusicHandler.negMusic.append(fileIndex)
                return False
            if answer=='A':
                MusicHandler.absMusic.append(fileIndex)
                return None
            print ('Wrong input: Answer must be N,Y,or A')
        
