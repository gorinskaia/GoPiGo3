import numpy as np
import argparse
import cv2
import datetime
import sys

class Image_Processing:

    def __init__(self, image_name):

        self.cX = 0
        self.cY = 0
        
        self.image_name = image_name
        image = cv2.imread(image_name)
        
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray_image,100,255,cv2.THRESH_BINARY)
        thresh = cv2.bitwise_not(thresh)

        M = cv2.moments(thresh)

        try:
            self.cX = int(M["m10"] / M["m00"])
            self.cY = int(M["m01"] / M["m00"])

            if self.cX == 199 and self.cY == 299:
                return # for now

            #print (cX, cY)

            cv2.circle(image, (self.cX, self.cY), 5, (255, 255, 255), -1)
            cv2.putText(image, "centroid", (self.cX - 25, self.cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

            cv2.imwrite('centroid.jpg', image)

        except ZeroDivisionError:
            pass


    def coord(self):
        return self.cX, self.cY
