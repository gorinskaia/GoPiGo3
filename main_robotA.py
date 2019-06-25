import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import threading
from Controller import ControllerForward
from Controller import ControllerTurn
from Controller import ControllerSequence
from RobotDexter import Dexter
from easygopigo3 import EasyGoPiGo3

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

threading.Thread(target=image_stream).start()
