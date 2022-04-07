import numpy as np
import imutils
import cv2
import matplotlib.pyplot as plt
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
from PIL import Image

img = cv2.imread('OCR2/image.jpg')
img=cv2.resize(img,(800,800))
gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite("OCR2/gray.jpg", gray)
#cv2.imshow('gray_image',gray)


#applying filter
edged = cv2.Canny(img,45,45)
cv2.imwrite("OCR2/edged.jpg", edged)
grayed=cv2.cvtColor(edged, cv2.COLOR_BGR2RGB)


keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(keypoints)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

location = None
for contour in contours:
    approx = cv2.approxPolyDP(contour, 10, True)
    if len(approx) == 4:
        location = approx
        break

"""
mask = np.zeros(edged.shape, np.uint8)
new_image = cv2.drawContours(mask, [location], (36,25,12), 2)
new_image = cv2.bitwise_and(img, img, mask=mask)
(x,y) = np.where(mask==255)
(x1, y1) = (np.min(x), np.min(y))
(x2, y2) = (np.max(x), np.max(y))
cropped_image = gray[x1:x2+1, y1:y2+1]"""

width=800
height=800

p1=np.ndarray(location)
p2=np.float32([[0,0],[width,0],[0,height],[width,height]])
matrix=cv2.getPerspectiveTransform(p1,p2)
imgoutput=cv2.warpPerspective(img,matrix,(width,height))

for x in range(0,4):
    cv2.circle(img,(p1[x][0],p2[x][1]),5,(0,0,255),cv2.FILLED)


cv2.imshow('original_img',img)
cv2.imshow('output',imgoutput)  


cv2.waitKey(0)
cv2.destroyAllWindows()



    
print(type(location))