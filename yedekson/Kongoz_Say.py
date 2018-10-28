# -*- coding: utf-8 -*-

import os 
import time
import pygame
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
 	
 	
def Play(filename):
    pygame.mixer.init()
    pygame.mixer.music.load("/home/pi/Desktop/github/KonGoz/" + filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue


def Stop():
	pygame.mixer.quit()
 	
 	
def Alert():
	os.system('mpg321 "{0}"'.format("/home/pi/Desktop/github/KonGoz/sound/newalert.mp3"))



def Save(number,text):
	os.system('espeak -vtr+m3 -s150 -w /home/pi/Desktop/github/KonGoz/wav/"{0}".wav "{1}"'.format(number,text.encode('utf-8')))



def Say(number):	
	Play('wav/' + number + '.wav')
       
       
        
def Control():
	Play('sound/control.wav')



def Start():
    Play('sound/voStart.wav')
  
  
  
def Capture():
    Play('sound/voCapture.wav')
    
    
    
def Next():
    Play('sound/voNext.wav')
    
    
    
def PowerOff():
    Play('sound/voPowerOff.wav')
            
        
        

        
        
        
def SS(filename, text):
    os.system('espeak -vtr+m3 -s150 -w /home/pi/Desktop/github/KonGoz/"{0}".wav "{1}"'.format(filename,text.encode('utf-8')))
