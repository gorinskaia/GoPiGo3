import time
from easygopigo3 import EasyGoPiGo3

print("Testing movement")

gpg = EasyGoPiGo3()
my_distance_sensor = gpg.init_distance_sensor()

curr_time = time.time()
curr_speed = 100

# Avoiding obstacles, movement

while True:
    gpg.set_speed(curr_speed)
    gpg.forward()
    dist = my_distance_sensor.read_mm()
    rand = random.randint(20,360)
    gpg.orbit(rand*random.choice([1,-1]), 20)   #random movement
    
    print("Distance Sensor Reading (mm): " + str(dist))
    if dist < 100:
        gpg.turn_degrees(90) # rotate around
        
    if time.time() - curr_time > 10     # turn off after 10 seconds
        gpg.stop()
        break

