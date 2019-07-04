import numpy as np
import argparse
import cv2
from matplotlib import pyplot as plt

image = cv2.imread('photos/2.jpg')

# Equalizing the histogramm
def equalize_hist(img):
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
    img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    return img

image = equalize_hist(image)

# FInding binary regions of red
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

mask1 = cv2.inRange(hsv, (0,50,20), (5,255,255))
mask2 = cv2.inRange(hsv, (175,50,20), (180,255,255))
mask = cv2.bitwise_or(mask1, mask2 ) # Important

# Find the biggest red region
(cnts, _) = cv2.findContours(mask.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
c = max(cnts, key = cv2.contourArea)

res = np.mean(c, axis=0)
res = res[0]
cX = int(round(res[0]))
cY = int(round(res[1]))

cv2.circle(image, (cX, cY), 5, (255, 255, 255), -1)
cv2.putText(image, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

# Display Image
cv2.imshow("Images", image)
cv2.waitKey(0)

'''gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray_image,100,255,cv2.THRESH_BINARY)
thresh = cv2.bitwise_not(thresh)

cv2.imshow("output", thresh)
cv2.waitKey(0)

M = cv2.moments(thresh)

cX = int(M["m10"] / M["m00"])
cY = int(M["m01"] / M["m00"])

print (cX, cY)
         
cv2.circle(image, (cX, cY), 5, (255, 255, 255), -1)
cv2.putText(image, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    # Display Image

cv2.imshow("Images", image)
cv2.waitKey(0)
'''
