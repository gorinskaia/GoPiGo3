import time
from easygopigo3 import EasyGoPiGo3
gpg = EasyGoPiGo3()
curr_time = time.time()

class Dexter:

    'Robot class'
    
    
    def __init__(self, speed = 300):
        self.speed = speed # Minimal distance between Dexter and obstacle
        
    def move(self):
        my_distance_sensor = gpg.init_distance_sensor() 
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
        my_distance_sensor = gpg.init_distance_sensor()
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
          
