import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import threading
from Dexter import ControllerForward
from Dexter import Dexter
#from viewer import Viewer

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

gpg = EasyGoPiGo3()
robot = Dexter(gpg)
robotA = ControllerForward(Dexter, 320, 80)

while not robotA.stop():
    robotA.update()

