# -*- coding: utf-8 -*-
# import the necessary packages
from PIL import Image
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

reWidth = 1024
reHeight = 768
FONT = cv2.FONT_HERSHEY_SIMPLEX
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()

#camera.resolution = (2592, 1944)         # framerate = 1-15 olmalı
#camera.framerate = 15

camera.resolution = (reWidth, reHeight)        # framerate = 1-30 olmalı 
camera.framerate = 30
camera.rotation = 90
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
        
        x, y, w, h = 0,0,reWidth,reHeight
        cv2.rectangle(image,(x,y),( x + w, y + h ),(0,255,0),1)
        
        cv2.imshow("my", image)
        
        roi = image[y:y+h, x:x+w]
        
        cv2.imshow("roi", roi)
        
        '''
        
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        image = cv2.bilateralFilter(image, 10, 10, 10)
        image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 3)
        
        kernel = np.ones((40,40), np.uint8)   # (h,w)
        img_eroded = cv2.erode(image, kernel, iterations=1)
        #find contours
        im2,ctrs, hier = cv2.findContours(img_eroded.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #sort contours
        sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
        image = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)
        img_eroded = cv2.cvtColor(img_eroded,cv2.COLOR_GRAY2RGB)
        
        for i, ctr in enumerate(sorted_ctrs):
            # Get bounding box
            x, y, w, h = cv2.boundingRect(ctr)
             
            #if (w > 300 and w < 1500  and h > 100 and h < 800):  # for 1920x1080          
            if (w > 150 and w < 1100  and h > 50 and h < 600):    # for 1280x720
                # Getting ROI
                roi = image[y:y+h, x:x+w]
                    
                #pil_roi = Image.fromarray(roi)                
                
                # show ROI
                #cv2.imshow('segment no:'+str(i),roi)
            
                
                #cv2.putText(image, str(w) + 'x' + str(h) + ' / x:' + str(x) + ' - y:' + str(y),(x,y), FONT, 0.5,(255,0,0),1, cv2.LINE_AA)
                cv2.putText(img_eroded, str(w) + 'x' + str(h) + ' / x:' + str(x) + ' - y:' + str(y),(x,y), FONT, 0.5,(255,0,0),1, cv2.LINE_AA)

                #roigray  = cv2.cvtColor(roi,cv2.COLOR_RGB2GRAY)
                #rotate(roigray)

                #cv2.rectangle(image,(x,y),( x + w, y + h ),(0,255,0),1)
                cv2.rectangle(img_eroded,(x,y),( x + w, y + h ),(0,255,0),1)
                #cv2.waitKey(0)
                
                #cv2.imshow("300dpi",image)
        
        # show the frame
        cv2.moveWindow("Frame", 40,30)
        cv2.imshow("Frame", img_eroded)
        
        '''

        key = cv2.waitKey(1) & 0xFF

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
                break


cv2.moveWindow("my", 0,0)
cv2.moveWindow("roi", 10,10)
