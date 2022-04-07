from cgi import test
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
   


#rect = cv2.minAreaRect(location)