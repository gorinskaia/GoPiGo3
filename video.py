import numpy as np
import cv2

#Capture Video from Camera

cap = cv2.VideoCapture(0)   #0 - for computer camera, or we can use a filename

"""Sometimes, cap may not have initialized the capture.
In that case, this code shows error. You can check whether it is initialized or not by the method cap.isOpened().
If it is True, OK. Otherwise open it using cap.open()."""

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read() #ret - value of pixels, frame - true if the capture is done

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  #Color conversion, cv2.cvtColor(input_image, flag), flag determines the type of conversion.

    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):   #Close on pressing 'q'
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()