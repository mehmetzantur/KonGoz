# -*- coding: utf-8 -*-

import tempfile
import cv2
import numpy as np
from PIL import Image
import time
from Queue import Queue
import os
import shutil
from threading import Thread
import threading
import pytesseract
import Kongoz_Say as kgSay
import RPi.GPIO as GPIO

IMAGE_SIZE = 1800
BINARY_THREHOLD = 180
OUTPUT_DPI = 300
global lastRoi
totaltime = 0   
sira = Queue()
imgDoc = []





def rotate(img):
    imgor = img
    img = cv2.bitwise_not(img)
    coords = np.column_stack(np.where(img > 0))
    angle = cv2.minAreaRect(coords)[-1]
     
    # the `cv2.minAreaRect` function returns values in the
    # range [-90, 0); as the rectangle rotates clockwise the
    # returned angle trends to 0 -- in this special case we
    # need to add 90 degrees to the angle
    if angle < -45:
            angle = -(90 + angle)
     
    # otherwise, just take the inverse of the angle to make
    # it positive
    else:
            angle = -angle
    
    # rotate the image to deskew it
    (h, w) = imgor.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(imgor, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    # draw the correction angle on the image so we can validate it
    cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle),
            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
     
    # show the output image
    print("[INFO] angle: {:.3f}".format(angle))
    cv2.imshow("Input", imgor)
    cv2.imshow("Rotated", rotated)
    cv2.waitKey(0)



def getFiltered(imgsrc):
    TOTAL_RECT = 0
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    #imgsrc = "images/camcap.jpg"
    image = cv2.imread(imgsrc)
    imageorg = cv2.imread(imgsrc)
    imgsrcThresholded = "/home/pi/Desktop/kongozpi/images/camcap_threshold_my.jpg"
    
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    #cv2.imshow("gray",image)
    
    imagebilateral = cv2.bilateralFilter(image, 10, 10, 10) 
    #cv2.imshow("bilateral",imagebilateral)
    
    

    image = cv2.adaptiveThreshold(imagebilateral, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 3)
    #cv2.imshow("thresholded_bilateral",image)

    pil_image = Image.fromarray(image)
    threshfile = '/home/pi/Desktop/kongozpi/images/mynewadap_thresh.png'
    pil_image.save(threshfile, dpi=(OUTPUT_DPI, OUTPUT_DPI))
    
    #laplacian_afterth = cv2.Laplacian(image,cv2.CV_64F)
    #cv2.imshow("laplacian_afterth",laplacian_afterth)
    
    #kernel = np.ones((15,20), np.uint8)


    kernel = np.ones((30,30), np.uint8)   # (h,w)
    img_eroded = cv2.erode(image, kernel, iterations=1)
    
    #find contours
    im2,ctrs, hier = cv2.findContours(img_eroded.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #sort contours
    sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
    image = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)
    img_eroded = cv2.cvtColor(img_eroded,cv2.COLOR_GRAY2RGB)
    
    
    
    roiList = []
    roiId = 0
    lastRoi = 0
    maxThread = 3
    counter = 0
    shutil.rmtree('seg', ignore_errors=True)
    shutil.rmtree('text', ignore_errors=True)
    
    for i, ctr in enumerate(sorted_ctrs):
        # Get bounding box
        x, y, w, h = cv2.boundingRect(ctr)
             
        if (w > 100 and h > 50 and h < 1000):
            counter += 1
            
            # Getting ROI
            roi = image[y:y+h, x:x+w]
            
            roiList.append(str(counter))
            #roiList.append(str(counter))
            
            imgDoc.append('KongozBeforeString')
            
            if not os.path.exists('seg'):
                os.makedirs('seg')
            if not os.path.exists('text'):
                os.makedirs('text')
                
            pil_roi = Image.fromarray(roi)
            segname = str(counter)
            pil_roi.save('/home/pi/Desktop/kongozpi/seg/' + segname + '.png', dpi=(OUTPUT_DPI, OUTPUT_DPI))
            
            
            # show ROI
            #cv2.imshow('segment no:'+str(i),roi)
        
            TOTAL_RECT += 1
            
            cv2.putText(image, str(w) + 'x' + str(h) + ' / x:' + str(x) + ' - y:' + str(y),(x,y), FONT, 0.5,(255,0,0),1, cv2.LINE_AA)
            cv2.putText(img_eroded, str(w) + 'x' + str(h) + ' / x:' + str(x) + ' - y:' + str(y),(x,y), FONT, 0.5,(255,0,0),1, cv2.LINE_AA)

            print("segment no: " + str(i) + "  -  " + str(w) + "x" + str(h))
            #roigray  = cv2.cvtColor(roi,cv2.COLOR_RGB2GRAY)
            #rotate(roigray)

            cv2.rectangle(image,(x,y),( x + w, y + h ),(0,255,0),1)
            cv2.rectangle(img_eroded,(x,y),( x + w, y + h ),(0,255,0),1)
            #cv2.waitKey(0)

    
    

    counter = 0
    for ros in roiList:
        print("seg/" + str(ros) + ".png " + "yazildi.")
    
    print("\033[0;37;40m")  
    print("\033[1;37;41m " + str(maxThread) + " thread baslatiliyor...")
    basla = time.time()   
    for i in range(maxThread):
        t = Thread(target = toString, args = (sira,))
        t.daemon = True
        t.start()
            
    for ro in roiList:
        sira.put(ro)
        
    sira.join()
    print("\033[1;36;40m Tum threadler %f saniye surdu  \n" % (time.time() - basla))
    
        
    cv2.putText(image, 'Toplam isaretlenen: ' + str(TOTAL_RECT),(100,80), FONT, 0.7,(255,0,0),1, cv2.LINE_AA)
    pil_image = Image.fromarray(image)
    #pil_image = pil_image.convert('1')  # görüntüyü siyah-beyaz yapıyor. zaten öyle olduğu için kapatıldı
    threshfile = '/home/pi/Desktop/kongozpi/images/mynew_thresh.png'
    pil_image.save(threshfile, dpi=(OUTPUT_DPI, OUTPUT_DPI))
    image = cv2.imread(threshfile)
    
    pil_image2 = Image.fromarray(img_eroded)
    threshfile2 = '/home/pi/Desktop/kongozpi/images/mynew_thresh2.png'
    pil_image2.save(threshfile2, dpi=(OUTPUT_DPI, OUTPUT_DPI))
    
    #cv2.imshow("300dpi",image)
    #cv2.imshow('dilated', img_eroded)
    return image



def toString(que):
    global counter
    while True:
        roiId = que.get()
        roi_src = '/home/pi/Desktop/kongozpi/seg/' + str(roiId) + '.png'
        imgString = pytesseract.image_to_string(Image.open(roi_src), lang='tur')
        imgString = imgString.replace('\"', '')
        imgString = imgString.replace('\'', '')
        imgString = imgString.replace('#', '')
        
        with open("/home/pi/Desktop/kongozpi/text/" + str(roiId) + ".txt", "w") as text_file:
            text_file.write("{0}".format(imgString.encode('utf-8')))
        
        roiId = int(roiId)
        roiIdindex = roiId - 1
        
        imgDoc[roiIdindex] = imgString
        
        print("\033[0;37;40m")  
        print("\033[1;36;40m Bitti: " + str(threading.current_thread()) + " - " + str(roi_src))
        kgSay.Save(str(roiId),imgDoc[roiId-1])
        que.task_done()
        
        if(roiId == 1):
            thSay = Thread(target = SaySay, args = (roiId,))
            thSay.daemon = False
            thSay.start()

# ----- metinlerin seslerini wav olarak kaydedip oynat ----

def SaySay(roiId):

    
    print("\033[1;37;43m Okuma Başlıyor: " + str(threading.current_thread()))
    print("\033[1;37;43m " + str(roiId) + ".png okunuyor")
    kgSay.Alert()
    kgSay.Say(str(roiId))
    roiId += 1
        
    
    while(roiId <= len(imgDoc)):
    
        if(imgDoc[roiId-1] != 'KongozBeforeString'):
            print("roiId:" + str(roiId) + " - " + str(len(imgDoc)))
            print("\033[1;37;43m " + str(roiId) + ".png okunuyorrr")
            kgSay.Alert()
            kgSay.Say(str(roiId))
            roiId += 1
     
    
    print("\033[1;37;42m ..Bitti...")
    

    
if __name__ == '__main__':

    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(33, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(7, GPIO.OUT)
    
    
    GPIO.output(7,GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(7,GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(7,GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(7,GPIO.LOW)
    
    kgSay.Control()

    while(True):
        
        btnPowerOff = GPIO.input(31)
        if btnPowerOff == False:
            kgSay.Alert()
            kgSay.PowerOff()
            GPIO.output(7,GPIO.HIGH)
            time.sleep(2)
            GPIO.output(7,GPIO.LOW)
            print('Button Kapat')
            os.system('sudo shutdown now')
        
        btnRead = GPIO.input(33)
        if btnRead == False:
            print('Button Oku')
            time.sleep(0.2)
            kgSay.Alert()
            kgSay.Start()
            getFiltered('/home/pi/Desktop/kongozpi/images/camcap.jpg')
    
    
        btnControl = GPIO.input(35)
        if btnControl == False:
            print('Button Kontrol')
            kgSay.Alert()
            kgSay.Control()
            time.sleep(0.2)
            
        btnTime = GPIO.input(37)
        if btnTime == False:
            print('Button Saat')
            kgSay.Alert()
            kgSay.timeNow()
            time.sleep(0.2)
        
        
    


    #cv2.waitKey(0)
    #cv2.destroyAllWindows()


