import numpy as np
import cv2

cap = cv2.VideoCapture(0)

resImage = [640, 480]   # assuming the resolutions of the image and screen are the following
resScreen = [1920, 1080]


while(True):

    ret, frame = cap.read()    # Capture frame-by-frame
    # Convert BGR to HSV
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    lower_blue = np.array([110,50,50])  # Range of a color blue
    upper_blue = np.array([130,255,255])

    mask = cv2.inRange(img, lower_blue, upper_blue)
    
    res = cv2.bitwise_and(frame,frame, mask = mask)    # Bitwise-AND mask and original image
    
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)

    points = cv2.findNonZero(mask) # Non zero points of a mask
    avg = np.mean(points, axis=0) # Barycentre, gives a single point normally

    # points are in x,y coordinates
    pointInScreen = ((resScreen[0] / resImage[0]) * avg[0], (resScreen[1] / resImage[1]) * avg[1] )
    print ("Point:" + str(pointInScreen))
    #img = cv2.circle(img,(pointInScreen), 63, (0,0,255), -1)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Display the resulting frame
        break

cap.release()   # When everything done, release the capture
cv2.destroyAllWindows()

# Barycentre of a robot (square)
# Take a pointin the middle
# Follow a point
