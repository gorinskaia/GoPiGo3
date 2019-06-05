import cv2
import numpy as np

img = cv2.imread('simon.jpg')

res = cv2.resize(img,None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)

res3 = cv2.resize(img,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
# dsize – output image size; if it equals zero (None), it is computed as:
# dsize = Size(round(fx*src.cols), round(fy*src.rows))

#interpolation – interpolation method; a bicubic interpolation over 4x4 pixel neighborhood

#OR

height, width = img.shape[:2]   #Returns a tuple of number of rows, columns and channels (if image is color)
res2 = cv2.resize(img,(2*width, 2*height), interpolation = cv2.INTER_CUBIC)

cv2.imshow('image1',res)
cv2.imshow('image2',res2)
cv2.imshow('image2',res3)

k =  cv2.waitKey(0)  #The function waits for specified milliseconds for any keyboard event.
if k == 27: #ESC key to exit
    cv2.destroyAllWindows()

img2 = cv2.imread('simon.jpg')
rows, cols = img2.shape

M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 90, 1)
dst = cv2.warpAffine(img, M, (cols, rows))