import cv2
import numpy as np
from matplotlib import pyplot as plt

#Tracking a blue object and a red one.
#In HSV, it is more easier to represent a color than RGB color-space

cap = cv2.VideoCapture(0)


resScreen = [1920, 1080]

while(1):

    # Take each frame
    ret, frame = cap.read()
    resImage = [(frame.shape[0]), (frame.shape[1])]  # assuming the resolutions of the image and screen are the following
    print("Size " + str(img.shape[0]) + " " + str(img.shape[1]))

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV

    #For HSV, Hue range is [0,179], so we need to normalize these ranges

    #To normalize:

    #lower_green = np.array([50, 100, 100])  #Adjust
    #upper_green = np.array([70, 255, 255])

    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])

    #Threshold the HSV image to get only blue colors
    #mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue) #Checks if array elements lie between the elements of two other arrays


    # Bitwise-AND mask and original image
    #mask = mask_green+mask_blue
    mask = mask_blue
    res = cv2.bitwise_and(frame,frame,mask=mask)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)

    points = cv2.findNonZero(mask)  # Non zero points of a mask
    avg = np.mean(points, axis=0)  # Barycentre, gives a single point normally

    print ("Average:"+str(avg))


    #pointInScreen = [(resScreen[0] / resImage[0]) * avg[0], (resScreen[1] / resImage[1]) * avg[1]]

    #print("Point:" + str(pointInScreen))
    
    img = cv2.circle(frame,(avg), 50, Scalar(0,0,255), -1)
    cv2.imshow('frame', img)

    '''img = cv2.circle(frame, avg, 50, (0, 0, 255), -1)'''
    #cv2.imshow('frame', frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:     #ESC key to exit
        break

cv2.destroyAllWindows()