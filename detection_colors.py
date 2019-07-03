# import the necessary packages
import numpy as np
import argparse
import cv2
 
image = cv2.imread("target2.jpg")

boundaries = [( [1,20,100], [180,255,255] )]
hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

for (lower, upper) in boundaries:
    lower = np.array(lower, dtype = "uint8")
    upper = np.array(upper, dtype = "uint8")

    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(hsv, image, mask = mask)

    # Find Centroid
    
    gray_image = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray_image,10,10,0)

    cv2.imshow("Image", thresh)
    cv2.waitKey(0)
    
    M = cv2.moments(thresh)

    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
     
    cv2.circle(output, (cX, cY), 5, (255, 255, 255), -1)
    cv2.putText(output, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    # Display Image

    cv2.imshow("Images", np.hstack([image, output]))
    cv2.waitKey(0)
