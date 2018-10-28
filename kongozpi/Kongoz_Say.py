# -*- coding: utf-8 -*-

import os 
import time
import pygame
 	
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
 	
def Alert():
	os.system('mpg321 "{0}"'.format("/home/pi/Desktop/kongozpi/newalert.mp3"))

def Save(number,text):
        os.system('espeak -vtr+m3 -s150 -w /home/pi/Desktop/kongozpi/wav/"{0}".wav "{1}"'.format(number,text.encode('utf-8')))

def Say(number):
	
##	os.system("aplay wav/{0}.wav".format(number))
	
	Play('wav/' + number + '.wav')
        
def SS(filename, text):
    os.system('espeak -vtr+m3 -s150 -w /home/pi/Desktop/kongozpi/"{0}".wav "{1}"'.format(filename,text.encode('utf-8')))

def Start():
    Play('voStart.wav')
    
def Capture():
    Play('voCapture.wav')
    
def Next():
    Play('voNext.wav')
    
def PowerOff():
    Play('voPowerOff.wav')
    
def timeNow():
    timeNow = 'Saat:' +  str(time.strftime('%H:%M'))
    os.system('espeak -vtr+m3 -s150 -w /home/pi/Desktop/kongozpi/"{0}".wav "{1}"'.format("timeNow",timeNow.encode('utf-8')))
    time.sleep(0.5)
    Play('timeNow.wav')
        
def Control():

        Play('control.wav')
        
        
def Play(filename):
    pygame.mixer.init()
    pygame.mixer.music.load("/home/pi/Desktop/kongozpi/" + filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    #text = "sistem aktif"
    #os.system('espeak -vtr+m3 -s150 -w control.wav "{0}"'.format(text.encode('utf-8')))