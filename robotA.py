import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import threading
from easygopigo3 import EasyGoPiGo3


# Initializing

curr_time = time.time()
gpg = EasyGoPiGo3()
my_distance_sensor = gpg.init_distance_sensor()

# Robot Class

class Dexter:
    
    def __init__(self, speed = 300):
        self.speed = speed # Minimal distance between Dexter and obstacle
        
    def move(self):
        gpg.set_speed(self.speed)
        count = 0
        gpg.forward()
        dist = my_distance_sensor.read_mm()

        if dist < 100:
            gpg.turn_degrees(90) # rotate around
            count+=1
        else:
            count = 0
            
        if count>3:
            gpg.turn_degrees(180) # rotate around if stuck
            count = 0
        if count>5:
            gpg.stop() # For now

    def print_distance(self):
        dist = my_distance_sensor.read_mm()
        print("Distance Sensor Reading (mm): " + str(dist))

    def stop_time(self):
        if (time.time() - curr_time) > 10:     # turn off after 10 seconds
            return True
        
    def stop(self):
        gpg.stop()

    def move_square(self):
       
        for i in range(4):
          gpg.forward() # drive forward for length cm
          time.sleep(2)
          gpg.steer(100, -50)
          time.sleep(0.6)
          

    
# Camera Thread

def image_stream ():
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

# Main


print ('Start.')

threading.Thread(target=image_stream).start()

robot = Dexter(320)

"""while True:
    robot.move()
    robot.print_distance()
    if robot.stop_time() == True:
        robot.stop()
        break"""

robot.move_square()
robot.stop()
    
