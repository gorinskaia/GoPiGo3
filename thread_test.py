import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import threading
    
def taking_photo ():
    camera = PiCamera()
    camera.resolution = (320, 240)
    rawCapture = PiRGBArray(camera)
    
    print ("Smile!")
    
    camera.capture(rawCapture, format="bgr")
    
    image = rawCapture.array
    print('1')
    cv2.imshow("image", image)
    print('2')
    cv2.waitKey(0) & 0xFF
    cv2.destroyAllWindows()
    rawCapture.truncate(0)
 
curr_time = time.time()
time.sleep(0.1)

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
print ("Hello!")

while True:
    key = cv2.waitKey(1) & 0xFF

    if key == ord("t"):
        print ("Here it comes...")
        threading.Thread(target=taking_photo).start()
               
    if  key == ord("q"):     # turn off 
        break

