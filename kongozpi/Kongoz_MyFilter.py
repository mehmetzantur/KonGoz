# -*- coding: utf-8 -*-

import tempfile
import cv2
import numpy as np
from PIL import Image
import time
import os
import shutil
from threading import Thread
import threading
import pytesseract
import Kongoz_Say as kgSay

IMAGE_SIZE = 1800
BINARY_THREHOLD = 180
OUTPUT_DPI = 300
global lastRoi
totaltime = 0   



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
    imgsrcThresholded = "images/camcap_threshold_my.jpg"
    
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    #cv2.imshow("gray",image)
    
    imagebilateral = cv2.bilateralFilter(image, 10, 10, 10) 
    #cv2.imshow("bilateral",imagebilateral)
    
    

    image = cv2.adaptiveThreshold(imagebilateral, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 3)
    #cv2.imshow("thresholded_bilateral",image)

    pil_image = Image.fromarray(image)
    threshfile = 'images/mynewadap_thresh.png'
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
    counter = 0
    roiId = 0
    lastRoi = 0
    maxThread = 3
    
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
            
            
            
            if not os.path.exists('seg'):
                os.makedirs('seg')
            if not os.path.exists('text'):
                os.makedirs('text')
                
            pil_roi = Image.fromarray(roi)
            segname = str(counter)
            pil_roi.save('seg/' + segname + '.png', dpi=(OUTPUT_DPI, OUTPUT_DPI))
            
            
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

    
    
    print("eleman sayisi: " + str(len(roiList)))
    
    
            
    while roiId <= counter:
        currentTh = threading.current_thread()
        roiId += 1
        th1=''
        if (roiId <= counter):
            image_roi = 'seg/' + str(roiId) + '.png'
            th1 = Thread(target = convertImgToString, args = (image_roi,roiId,currentTh,time.time(),lastRoi,counter))
            th1.start()

            lastRoi += 1
            imgDoc.append('') # dizide eleman sayisi kadar alan acmak icin

        if(lastRoi == maxThread):
            
            lastRoi = 0
            th1.join()
            

        
        #print("active th: " + str(threading.active_count()))
        

# NOT --->  1. TH BİTTİĞİNDE SAY E GÖNDER. ORADA DİĞER TH LERİ BEKLE VE ARDIŞIK BAŞLAT
    
    
    cv2.putText(image, 'Toplam isaretlenen: ' + str(TOTAL_RECT),(100,80), FONT, 0.7,(255,0,0),1, cv2.LINE_AA)
    pil_image = Image.fromarray(image)
    #pil_image = pil_image.convert('1')  # görüntüyü siyah-beyaz yapıyor. zaten öyle olduğu için kapatıldı
    threshfile = 'images/mynew_thresh.png'
    pil_image.save(threshfile, dpi=(OUTPUT_DPI, OUTPUT_DPI))
    image = cv2.imread(threshfile)
    
    pil_image2 = Image.fromarray(img_eroded)
    threshfile2 = 'images/mynew_thresh2.png'
    pil_image2.save(threshfile2, dpi=(OUTPUT_DPI, OUTPUT_DPI))
    
    #cv2.imshow("300dpi",image)
    #cv2.imshow('dilated', img_eroded)
    return image







imgDoc = []
def convertImgToString(img,roiId,currentTh,starttime,lastRoi,counter):
    global totaltime
    print("roiId: " + str(roiId) + " - " + str(threading.current_thread()))
    #print("roiId: " + str(roiId) + " - " + currentTh + "%f. th started." % starttime)

    #print ('converting img to text...' + img)
    imgString = pytesseract.image_to_string(Image.open(img), lang='tur')
    print("")
    print ("roiId: " + str(roiId) + " - " + str(threading.current_thread()) + "\n Tesseract: %f saniye surdu " % (time.time() - starttime))
    totaltime = totaltime + (time.time() - starttime)
    print(str(totaltime))
    start = 0
    imgString = imgString.replace('\"', '')
    imgString = imgString.replace('\'', '')
    imgString = imgString.replace('#', '')
    #print(imgString)
    
    with open("text/" + str(roiId) + ".txt", "w") as text_file:
            text_file.write("{0}".format(imgString.encode('utf-8')))


    imgDoc[roiId-1] = imgString

    
    if (roiId == 1):
        thSay = Thread(target = SaySay, args = (roiId,))
        #thSay.start()
    
        
    return False


def SaySay(roiId):
    print("gelen roi: " + str(roiId))
    if (roiId == 1):
        kgSay.Alert()
        kgSay.Say("indis: " + str(roiId-1))
        #kgSay.Say(imgString.encode('utf-8'))
        
        read = roiId-1
        nextRead = read + 1
        
        print("roiId: " + str(roiId))
        print("okunan indis: " + str(read))
        print("icerik: " + str(imgDoc[read].encode('utf-8') ))
        print("okunacak indis: " + str(nextRead))
        
        while(read <= len(imgDoc)-1):
            if(imgDoc[nextRead] != ''):
                roiId += 1
                kgSay.Say(str(imgDoc[read].encode('utf-8') ))
                read = nextRead
                nextRead += 1
                print("roiId: " + str(roiId))
                print("okunan indis: " + str(read))
                print("icerik: " + str(imgDoc[read].encode('utf-8') ))
                print("okunacak indis: " + str(nextRead))
                print("nextRead= " + str(nextRead) + " -> " + str(len(imgDoc)-1))
                
            if(nextRead == len(imgDoc)-1):
                print("son nextRead= " + str(nextRead) + " - " + str(len(imgDoc)-1))
                kgSay.Say("son indis: " + str(nextRead))
                return True
        
        
        
        
##        while(read <= len(imgDoc)-1):
##            if(imgDoc[nextRead] != ''):
##                roiId += 1
##                kgSay.Say("indis: " + str(nextRead))
##                read = nextRead
##                nextRead += 1
##                print("roiId: " + str(roiId))
##                print("okunan indis: " + str(read))
##                print("icerik: " + str(imgDoc[read].encode('utf-8') ))
##                print("okunacak indis: " + str(nextRead))
##                print("nextRead= " + str(nextRead) + " -> " + str(len(imgDoc)-1))
##                
##            if(read == len(imgDoc)-1):
##                print("nextRead= " + str(nextRead) + " - " + str(len(imgDoc)-1))
##                return True

            

    
if __name__ == '__main__':
    
    
##    img = process_image_for_ocr('images/camcap.jpg')
    
    getFiltered('images/camcap.jpg')
    #starttt = time.time()
    #imgString = pytesseract.image_to_string(Image.open('images/mynewadap_thresh.png'), lang='tur')
    #print("toppp: %f" % (time.time() - starttt))
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()