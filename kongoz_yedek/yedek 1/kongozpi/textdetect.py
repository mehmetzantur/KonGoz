import cv2

# Load the image
image = cv2.imread('images/camcap.jpg')

# convert to grayscale
#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# smooth the image to avoid noises
#gray = cv2.medianBlur(gray,5)

# Apply adaptive threshold
#thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)
#thresh_color = cv2.cvtColor(thresh,cv2.COLOR_GRAY2BGR)

# apply some dilation and erosion to join the gaps - change iteration to detect more or less area's
#thresh = cv2.dilate(thresh,None,iterations = 15)
#thresh = cv2.erode(thresh,None,iterations = 15)


image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
image = cv2.bilateralFilter(image, 10, 10, 10) 
image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 3)


# Find the contours
image2,contours,hierarchy = cv2.findContours(image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
i = 1
# For each contour, find the bounding rectangle and draw it
for cnt in contours:
    x,y,w,h = cv2.boundingRect(cnt)
    
    # Don't plot small false positives that aren't text
    if w < 20 and h < 20:
        continue
    
    #roi = image[y:y+h, x:x+w]
    #cv2.imwrite("images/cnt/" + str(i) + "_roi.png", roi)
    #i += 1
    
    cv2.rectangle(image,(x,y),(x+w,y+h),(100,200,300),2)
    #cv2.rectangle(thresh_color,(x,y),(x+w,y+h),(0,255,0),2)

cv2.imwrite('images/karakterli.jpg',image)
# Finally show the image
#cv2.imshow('img',image)
#cv2.imshow('res',thresh_color)
#cv2.waitKey(0)
#cv2.destroyAllWindows()