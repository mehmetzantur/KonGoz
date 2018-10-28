import pytesseract
import time
from PIL import Image

def convertImgToString(img):
	
    start = time.time()
    print ('converting img to text...' + img)
    imgString = pytesseract.image_to_string(Image.open(img), lang='tur')
    print ('Tesseract: %f saniye surdu' % (time.time() - start))
    
    imgString = imgString.replace('\"', '')
    imgString = imgString.replace('\'', '')
    imgString = imgString.replace('#', '')
    #print(imgString)
    
    with open("Output.txt", "w") as text_file:
            text_file.write("{0}".format(imgString))

    
    return False



convertImgToString('camcap_thresh.png')