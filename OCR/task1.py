import cv2
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

from PIL import Image

def getSkewAngle(cvImage) -> float:
    # Prep image, copy, convert to gray scale, blur, and threshold
    newImage = cvImage.copy()
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Apply dilate to merge text into meaningful lines/paragraphs.
    # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
    # But use smaller kernel on Y axis to separate between different blocks of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=2)

    # Find all contours
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)
    for c in contours:
        rect = cv2.boundingRect(c)
        x,y,w,h = rect
        cv2.rectangle(newImage,(x,y),(x+w,y+h),(0,255,0),2)

    # Find largest contour and surround in min area box
    largestContour = contours[0]
    print (len(contours))
    minAreaRect = cv2.minAreaRect(largestContour)
    cv2.imwrite("temp/boxes.jpg", newImage)
    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAreaRect[-1]
    if angle < -45:
        angle = 90 + angle
    return -1.0 * angle
# Rotate the image around its center
def rotateImage(cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage




def deskew(cvImage):
    angle = getSkewAngle(cvImage)
    return rotateImage(cvImage, -0.1 * angle)

img = cv2.imread('OCR/rotatedimg.jpg')
fixed = deskew(img)
cv2.imwrite("OCR/rotated_fixed.jpg", fixed)


#img = cv2.resize(img,(800, 800))
#cv2.imshow('page',img)
inverted_image = cv2.bitwise_not(fixed)
cv2.imwrite("OCR/inverted.jpg", inverted_image)
#cv2.imshow('inverted_image',inverted_image)


def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

gray_image = grayscale(fixed)
cv2.imwrite("OCR/gray.jpg", gray_image)
#cv2.imshow('gray',gray_image)

def noise_removal(image):
    import numpy as np
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return (image)

    
def thick_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,2),np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)

dilated_image = thick_font(gray_image)
cv2.imwrite("OCR/dilated_image.jpg", dilated_image)

thresh, im_bw = cv2.threshold(gray_image,165,165, cv2.THRESH_BINARY)
cv2.imwrite("OCR/bw_image.jpg", im_bw)
#cv2.imshow('thresh_img',im_bw)




noise_Rem=noise_removal(im_bw)
cv2.imwrite("OCR/noise_Rem_image.jpg", noise_Rem)




img_file = "OCR/bw_image.jpg"
ocr_result = pytesseract.image_to_string(img_file)
print(ocr_result)









cv2.waitKey(0) 
cv2.destroyAllWindows() 
 
