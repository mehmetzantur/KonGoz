# -*- coding: utf-8 -*-
# import the necessary packages
from PIL import Image
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import Kongoz_MyFilter as kgMyFilter

kernel = np.ones((5, 5), np.uint8)
reWidth = 1920
reHeight = 1080

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()

#camera.resolution = (2592, 1944)         # framerate = 1-15 olmalı
#camera.framerate = 15

camera.resolution = (reWidth, reHeight)        # framerate = 1-30 olmalı 
camera.framerate = 30
camera.rotation = 180
camera.brightness = 50                   # Işık
camera.sharpness = 100                   # Keskinlik
camera.iso = 100                         # Gün ışığında 100-200 , düşük ışıkta 400-800
camera.saturation = 0                    # Renklerin canlılık ayarı
camera.contrast = 0                      # Kontrast 0 iken yazı alanının kenarları daha iyi gözüküyor
#camera.zoom = (0.25, 0.25, 0.25, 0.25)

rawCapture = PiRGBArray(camera, size=(reWidth, reHeight))
 
# allow the camera to warmup
time.sleep(0.1)
 
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array
        
        
        
        
        #image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        #image = cv2.bilateralFilter(image, 10, 10, 10)
                
        #image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 3)
        
            
        # show the frame
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
                break
