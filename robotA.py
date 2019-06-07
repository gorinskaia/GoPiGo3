import time
from easygopigo3 import EasyGoPiGo3
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (352, 272)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(352, 272))

# allow the camera to warmup
time.sleep(0.1)

gpg = EasyGoPiGo3()
my_distance_sensor = gpg.init_distance_sensor()

curr_time = time.time()
curr_speed = 320

gpg.set_speed(curr_speed)

time.sleep(1)
count = 0

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    key = cv2.waitKey(1) & 0xFF
    
    image = frame.array
    cv2.imshow("Frame", image)

    rawCapture.truncate(0)  # clear the stream in preparation for the next frame
    gpg.forward()
    dist = my_distance_sensor.read_mm()

    if dist < 100:
        gpg.turn_degrees(90) # rotate around
        print("Turning 90")
        count+=1
    else:
        count = 0

    if count>3:
        gpg.turn_degrees(180) # rotate around
        print("Tired of turning...")
        count = 0
               
    if (time.time() - curr_time) > 15 or key == ord("q"):     # turn off
        gpg.stop()
        break

gpg.stop()
