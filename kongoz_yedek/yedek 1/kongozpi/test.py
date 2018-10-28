import cv2
import numpy as np
from time import time
import glob

from PIL import Image

inputImage = "images/page1.jpg"
inputBigImage = "res/BigImg.png"
kernel = np.ones((5, 5), np.uint8)
fgbg = cv2.createBackgroundSubtractorMOG2()

def convertToBigImage(img,multiple):
    img = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    height = np.size(img, 0)
    width = np.size(img, 1)
    big = cv2.resize(img, (multiple * width, multiple * height))
    return big

def convertToImg(matrix):
    #cv2.imwrite(inputBigImage, convertToBigImage(img, 5))
    im = Image.fromarray(matrix)
    outputConvertedImage = "res/convertedImage.jpeg"
    im.save(outputConvertedImage)
    return outputConvertedImage

def convertToImg2(matrix):
    im = Image.fromarray(matrix)
    return im

def yenideneme(img):
    img = cv2.imread(img)
    img = img[0:100, 0:100]
    grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #grayscaled = cv2.bitwise_not(grayscaled)
    #gauss = cv2.GaussianBlur(grayscaled, (3, 3), 0)

    gauss = cv2.bilateralFilter(grayscaled, 10, 10, 10)
    result = cv2.adaptiveThreshold(gauss, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 3)
    #gauss = cv2.GaussianBlur(gauss, (3, 3), 0)
    return result

print("--- baslangic ---")
start = time()

cv2.imshow('yenibilate4', yenideneme(inputImage))

print ("%f saniye surdu" % (time() - start))

cv2.waitKey(0)
cv2.destroyAllWindows()

print("--- bitis ---")
