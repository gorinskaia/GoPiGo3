# --- Global libraries --- 
import time
from Controller import ControllerInit
from Controller import ControllerForward
from Controller import ControllerTurn
from Controller import ControllerSequence
from panda3d.core import *
from panda3d.bullet import *
import numpy
import threading

class Proxy:
    def __init__(self, option):
        self.option = option

    def setup(self):
        if self.option == "a":

            # --- Import local libraries ---
            import direct.directbase.DirectStart
            from RobotModel3D import Robot
            from main_simulation3d import Simulation

            self.sim = Simulation()

            for i in numpy.arange(0, COLLISION_DIST/30, 0.5):
                self.sim.sColl = self.sim.initCollisionSphere(self.sim.robot.robotModel, True, Point3(0,(COLLISION_DIST/30)-i,1))
                base.cTrav.addCollider(self.sim.sColl[0], self.sim.collHandEvent)
                self.sim.accept('into-' + self.sim.sColl[1], self.sim.collide)
            self.robot = self.sim.robot
            return self.robot

        else:
            
            # --- Import local libraries --- 
            from easygopigo3 import EasyGoPiGo3
            from RobotDexter import Dexter
            import main_robotA
            gpg = EasyGoPiGo3()
            self.robot = Dexter(gpg)
            return self.robot
            
    def run(self, sequence):

        self.sequence = sequence
        threading.Thread(target=self.get_degrees, daemon=True).start()
        
        if self.option == "a":
            self.sim.ctrl = ControllerSequence(self.sequence)
            self.sim.ctrl.start()
            base.run()
        else:
            ctrl = ControllerSequence(self.sequence)
            ctrl.start()
            while not ctrl.stop():
                ctrl.update()
                time.sleep(0.01)

    def shutdown(self):
        self.robot.shutdown()
        
    def get_speed(self):
        print (self.robot.get_speed())
        return self.robot.get_speed()

    def get_dist(self):
        if self.option == "a":
            print('Sorry, no input data (simulation)')
        else:
            print (self.robot.get_dist())
            return self.robot.get_dist()

    def get_degrees(self):
        res = self.robot.get_offset()
        offset = max(abs(res[1]), abs(res[0])) 
        turn = ((self.robot.WHEEL_CIRCUMFERENCE*offset)/(self.robot.WHEEL_BASE_CIRCUMFERENCE))/2
        print ('Degrees: ', turn)
        return turn
        
        
# --- Global variables ---

COLLISION_DIST = 120
SPEED = 300

# --- Choose an option between 3D Simulation and Real World Action
while True:
    option = input ("Do you want to: A) Play simulation B) Control the robot. [a/b]? : ")
    if option in ['a', 'b']:
        break

proxy = Proxy(option)
robot = proxy.setup()

forward = ControllerForward(robot, 300, COLLISION_DIST)
turn90 = ControllerTurn(robot, 400, 90)
turn_ = ControllerTurn(robot, 350, -45)

sequence = [turn_, forward, turn_, forward]

proxy.run(sequence)
proxy.shutdown()
