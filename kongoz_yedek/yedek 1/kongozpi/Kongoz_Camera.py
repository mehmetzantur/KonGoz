# -*- coding: utf-8 -*-
from picamera import PiCamera
from picamera import Color
from time import sleep
import cv2

reWidth = 1920
reHeight = 1080

PiCamera().close()
camera = PiCamera()

#camera.resolution = (3280, 2464)         # framerate = 1-15 olmalı
#camera.framerate = 15

camera.resolution = (reWidth, reHeight)        # framerate = 1-30 olmalı 
camera.framerate = 20                    # Min rate 15-20 arasında ?
camera.rotation = 180
camera.brightness = 50                   # Işık
camera.sharpness = 100                   # Keskinlik
camera.iso = 100                         # Gün ışığında 100-200 , düşük ışıkta 400-800
camera.saturation = 0                    # Renklerin canlılık ayarı
camera.contrast = 0                      # Kontrast 0 iken yazı alanının kenarları daha iyi gözüküyor

def showLiveValues():
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




def camGoz():
    #camera.resolution = (600, 600)
    #camera.start_preview()
    #camera.annotate_foreground = Color('black')
    #camera.annotate_background = Color('green')
    #camera.annotate_text = "Test Ekrani \n Goruntu aliniyor..."
    #sleep(5)
    #camera.stop_preview()
    #camera.resolution = (reWidth, reHeight)
    
    imgsrc = 'images/camcap.jpg'
    camera.capture(imgsrc)
    camera.close()
    return imgsrc


if __name__ == '__main__':

    #showLiveValues()


    camGoz()





