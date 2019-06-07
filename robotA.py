import time
from easygopigo3 import EasyGoPiGo3
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import threading

camera = PiCamera()
rawCapture = PiRGBArray(camera)
    
def taking_photo ():
    print ("Smile!")
    time.sleep(0.1)   # allow the camera to warmup
    camera.resolution = (320, 240)
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    cv2.imshow("Image", image)
    rawCapture.truncate(0)

gpg = EasyGoPiGo3()
my_distance_sensor = gpg.init_distance_sensor()

curr_time = time.time()
curr_speed = 320

#gpg.set_speed(curr_speed)

time.sleep(1)
count = 0

taking_photo ()
while True:

    key = cv2.waitKey(1) & 0xFF
    
   # gpg.forward()
    
    #dist = my_distance_sensor.read_mm()

    if key == ord("t"):
        print ("here it comes...")
        threading.Thread(target=taking_photo).start()
    
    '''if dist < 100:
        gpg.turn_degrees(90) # rotate around
        print("Turning 90")
        count+=1
    else:
        count = 0

    if count>3:
        gpg.turn_degrees(180) # rotate around
        print("Tired of turning...")
        count = 0'''
               
    if (time.time() - curr_time) > 15 or key == ord("q"):     # turn off
        #gpg.stop()
        break

#gpg.stop()
