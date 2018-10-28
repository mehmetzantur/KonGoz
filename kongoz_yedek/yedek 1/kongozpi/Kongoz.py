# -*- coding: utf-8 -*-
import numpy as np
import cv2
from PIL import Image
from picamera.array import PiRGBArray
import pytesseract
import os
import picamera
import time
import espeak
import threading
import Kongoz_MyFilter as kgMyFilter
import Kongoz_Say as kgSay
import Kongoz_Speak as kgSpeak
import Kongoz_Camera as kgCam

def convertImgToString(img):
	kgSay.Alert()
	kgSay.Say("Resim yazıya çevriliyor.")
	start = time.time()
	print ('converting img to text...' + img)
	imgString = pytesseract.image_to_string(Image.open(img), lang='tur')
	print ('Tesseract: %f saniye surdu' % (time.time() - start))
	kgSay.Alert()
	kgSay.Say("Resim okunuyor.")
	imgString = imgString.replace('\"', '')
	imgString = imgString.replace('\'', '')
	imgString = imgString.replace('#', '')
	#print(imgString)
	
	with open("Output.txt", "w") as text_file:
    		text_file.write("{0}".format(imgString))

	kgSay.Alert()
	kgSay.Say(imgString.encode('utf-8'))
	return False


#kgSay.Alert()
#kgSay.Say("Merhaba! Ben Kongöz. Sana kitap okuyabilmen konusunda yardımcı olmak için programlandım.")
#kgSay.Say("Şimdi 5 saniye içinde sayfanın görüntüsünü alacağım.")
kgSay.Alert()
kgSay.Say("Sayfa filtreleniyor.")

start = time.time()
imgsrc = kgCam.camGoz()
print ('Return imgsrc: %f saniye surdu' % (time.time() - start))

start = time.time()
#img = kgMyFilter.getFiltered(imgsrc)
img = kgMyFilter.process_image_for_ocr('images/camcap.jpg')
print ('Filter: %f saniye surdu' % (time.time() - start))

#t1 = threading.Thread(target=openFilteredImage, args=(img,))
#t1.start()

print (' ')

t2 = threading.Thread(target=convertImgToString, args=(img,))
t2.start()


cv2.waitKey(0)
cv2.destroyAllWindows()