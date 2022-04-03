import cv2
import numpy as np
img = cv2.imread("pic.PNG")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 75, 150)
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30, maxLineGap=250)
for line in lines:
   x1, y1, x2, y2 = line[0]
   cv2.putText(img, "number_rect. = 1", (365,390), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0)) 
   cv2.putText(img, "number_rect. = 2", (71,180), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0)) 
   cv2.putText(img, "number_rect. = 3", (306,180), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0)) 
   cv2.putText(img, "number_rect. = 4", (72,410), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0)) 

cv2.imshow("linesDetected", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
