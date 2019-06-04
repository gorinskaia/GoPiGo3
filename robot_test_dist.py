import time
from easygopigo3 import EasyGoPiGo3

print("Testing movement")

gpg = EasyGoPiGo3()
my_distance_sensor = gpg.init_distance_sensor()


while True:
    dist = my_distance_sensor.read_mm()
    print("Distance Sensor Reading (mm): " + str(dist))
    if dist < 100:
         print("STOP: " + str(dist))


