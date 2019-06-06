import time
import random
from easygopigo3 import EasyGoPiGo3

print("Testing movement")

gpg = EasyGoPiGo3()
my_distance_sensor = gpg.init_distance_sensor()

curr_time = time.time()
curr_speed = 290

gpg.set_speed(curr_speed)

time.sleep(1)
count = 0

while True:
    gpg.forward()
    dist = my_distance_sensor.read_mm()

    if dist < 120 and dist > 99:
        gpg.turn_degrees(45) # rotate around
        print("Turning 45")
        count+=1
    elif dist < 100:
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
    
gpg.stop()
