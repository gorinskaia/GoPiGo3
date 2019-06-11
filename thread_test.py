import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import threading
from easygopigo3 import EasyGoPiGo3
    
def taking_photo ():
    camera = PiCamera()
    camera.resolution = (320, 240)
    camera.framerate = 30
    rawCapture = PiRGBArray(camera, size=(320, 240))

    display_window = cv2.namedWindow("Image")
    time.sleep(0.1)

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        cv2.imshow("Image", image)
        key = cv2.waitKey(1)
        rawCapture.truncate(0)

        if key == ord("q"):
            camera.close()
            cv2.destroyAllWindows()
            break


gpg = EasyGoPiGo3()
my_distance_sensor = gpg.init_distance_sensor()

curr_time = time.time()
curr_speed = 290

gpg.set_speed(curr_speed)
count = 0

print ("Hello!")

threading.Thread(target=taking_photo).start()

while True:
    gpg.forward()
    dist = my_distance_sensor.read_mm()

    if dist < 100:
        gpg.turn_degrees(90) # rotate around
        print("Turning 90")
        count+=1
    else:
        print("Distance Sensor Reading (mm): " + str(dist))
        count = 0

    if count>3:
        gpg.turn_degrees(180) # rotate around
        print("Tired of turning...")
        count = 0
               
    if (time.time() - curr_time) > 20:     # turn off after 10 seconds
        gpg.stop()
        break
