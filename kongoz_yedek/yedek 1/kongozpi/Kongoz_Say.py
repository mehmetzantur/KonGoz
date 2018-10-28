# -*- coding: utf-8 -*-
import os 
import time
import pygame
 	

def Alert():
	os.system('mpg321 "{0}"'.format("alert.mp3"))

def Save(number,text):
    os.system('espeak -vtr+m3 -s150 -w wav/"{0}".wav "{1}"'.format(number,text.encode('utf-8')))

def Say(number):
	
##	os.system("aplay wav/{0}.wav".format(number))
	
	pygame.mixer.init()
	pygame.mixer.music.load("wav/{0}.wav".format(number))
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy() == True:
            continue
	    

