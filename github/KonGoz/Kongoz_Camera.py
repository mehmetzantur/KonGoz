# -*- coding: utf-8 -*-

from picamera import PiCamera
from picamera import Color
from time import sleep
import cv2
import numpy as np

#camera.resolution = (3280, 2464)			# framerate = 1-15 olmalı
#camera.framerate = 15

reWidth = 1024
reHeight = 768
FONT = cv2.FONT_HERSHEY_SIMPLEX

camera = PiCamera()
camera.resolution = (reWidth, reHeight)		# framerate = 1-30 olmalı 
camera.framerate = 30                    	
camera.rotation = 90
camera.brightness = 55                 		# Işık
camera.sharpness = 100                   	# Keskinlik
camera.iso = 200                       	# Gün ışığında 100-200 , düşük ışıkta 400-800
camera.saturation = 0                    	# Renklerin canlılık ayarı
camera.contrast = 0                      	# Kontrast 0 iken yazı alanının kenarları daha iyi gözüküyor



def CamGoz():   
    
    imgsrc = '/home/pi/Desktop/github/KonGoz/images/camcap.jpg'
    camera.capture(imgsrc)
     
    return imgsrc


def ShowLiveValues():
    camera.start_preview()
    for i  in range(20):
        if(i == 0):
            i = 5
        camera.framerate = i
        camera.annotate_foreground = Color('black')
        camera.annotate_background = Color('green')
        camera.annotate_text = "KonGoz Test " + " - i: " + str(i)
        sleep(0.5)
    camera.stop_preview()


if __name__ == '__main__':

    #ShowLiveValues()
    
    CamGoz()
