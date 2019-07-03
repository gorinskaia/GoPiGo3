import numpy as np
import argparse
import cv2
import datetime
import sys

class Image_Processing:

    def __init__(self, image_name):
    
        self.image_name = image_name
        image = cv2.imread(image_name)
        
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray_image,100,255,cv2.THRESH_BINARY)
        thresh = cv2.bitwise_not(thresh)

        M = cv2.moments(thresh)

        try:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            cv2.circle(image, (cX, cY), 5, (255, 255, 255), -1)
            cv2.putText(image, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

            # Display Image
            now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
            file_name = 'results/'+ now + '.jpg'
            cv2.imwrite(file_name, image)


        except ZeroDivisionError:
            print ('Target not on screen')
            pass
             
        
        #cv2.imshow("Images", image)
        #cv2.waitKey(0)
