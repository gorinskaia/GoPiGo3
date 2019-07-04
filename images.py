import numpy as np
import argparse
import cv2
import datetime
import sys

class Image_Processing:

    def __init__(self, image_name):

        self.cX = 320
        self.cY = 240
        
        self.image_name = image_name
        image = cv2.imread(image_name)
        image = equalize_hist(image)
        
        # FInding binary regions of red
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        mask1 = cv2.inRange(hsv, (0,50,20), (5,255,255))
        mask2 = cv2.inRange(hsv, (175,50,20), (180,255,255))
        mask = cv2.bitwise_or(mask1, mask2 ) # Important

        
        kernel = np.ones((5,5),np.uint8)
        mask = cv2.erode(mask,kernel,iterations = 1)

        # Find the biggest red region
        (cnts, _) = cv2.findContours(mask.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        c = max(cnts, key = cv2.contourArea)
        res = np.mean(c, axis=0)
        res = res[0]
        cX = int(round(res[0]))
        cY = int(round(res[1]))

    # Equalizing the histogramm
    def equalize_hist(img):
        img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
        img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
        img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
        return img

    def coord(self):
        return self.cX, self.cY
