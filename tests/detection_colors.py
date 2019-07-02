# import the necessary packages
import numpy as np
import argparse
import cv2
 
image = cv2.imread("target2.jpg")

# define the list of boundaries
boundaries = [( [1,20,100], [180,255,255] )]
hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

# loop over the boundaries
for (lower, upper) in boundaries:
# create NumPy arrays from the boundaries
    lower = np.array(lower, dtype = "uint8")
    upper = np.array(upper, dtype = "uint8")

    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(hsv, image, mask = mask)
    
    ret,thresh = cv2.threshold(gray_image,127,255,0)
    M = cv2.moments(output)
     
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
     
    cv2.circle(img, (cX, cY), 5, (255, 255, 255), -1)

    #cv2.rectangle(output, (cX,0),(510,128), (0,255,0),3)

    cv2.imshow("Images", np.hstack([image, output]))
    cv2.waitKey(0)
