import numpy as np
import argparse
import cv2

image = cv2.imread("results/res.jpg")
hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

lower = np.array([80,0,65], dtype = "uint8")
upper = np.array([120,140,160] , dtype = "uint8")

mask = cv2.inRange(hsv, lower, upper)
output = cv2.bitwise_and(hsv, image, mask = mask)
    
gray_image = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray_image,45,450,cv2.THRESH_BINARY)

cv2.imshow("output", gray_image)
cv2.waitKey(0)

M = cv2.moments(thresh)

cX = int(M["m10"] / M["m00"])
cY = int(M["m01"] / M["m00"])
         
cv2.circle(image, (cX, cY), 5, (255, 255, 255), -1)
cv2.putText(image, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    # Display Image

cv2.imshow("Images", image)
cv2.waitKey(0)
