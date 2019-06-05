import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('simon.jpg',0)


cv2.namedWindow('image', cv2.WINDOW_NORMAL) #Resize window. Default: cv2.WINDOW_AUTOSIZE
cv2.imshow('image',img)
k =  cv2.waitKey(0)  #The function waits for specified milliseconds for any keyboard event.
if k == 27: #ESC key to exit
    cv2.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    cv2.imwrite('messigray.png',img) #Save new image
    cv2.destroyAllWindows()


plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([]), plt.yticks([])  # Empty list to hide tick values on X and Y axis (scales)
plt.show() #Show in matplotlib