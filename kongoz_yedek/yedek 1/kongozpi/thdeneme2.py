import cv2
import glob
from time import time
start = time()
img = cv2.imread("images/page1.jpg")
#crop_img = img[y:y+h, x:x+w]
cropped = img[0:100, 0:100]
cv2.imshow("cropped", cropped)
print ("%f saniye surdu" % (time() - start))

cv2.waitKey(0)