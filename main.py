# --- Global libraries --- 
import time
from Controller import ControllerInit
from Controller import ControllerForward
from Controller import ControllerTurn
from Controller import ControllerSequence
from Controller import ControllerFollow
from Controller import ControllerLearn
from Controller import ControllerForwardSmart

from panda3d.core import *
from panda3d.bullet import *

import numpy
import threading

class Option:
    def __init__(self, option):
        self.option = option

    def setup(self):
        if self.option == "a":
            # --- Import local libraries ---
            import direct.directbase.DirectStart
            from RobotModel3D import Robot
            from main_simulation3d import Simulation

            self.sim = Simulation()
            j=1 # For the number of a collision sphere
            for i in numpy.arange(0, COLLISION_DIST/30, 0.5):
                self.sim.sColl = self.sim.initCollisionSphere(self.sim.robot.robotModel, False, Point3(0,(COLLISION_DIST/30)-i+1,1),j)
                base.cTrav.addCollider(self.sim.sColl[0], self.sim.collHandEvent)
                self.sim.accept('into-' + self.sim.sColl[1], self.sim.collide)
                j+=1
            self.robot = self.sim.robot
            
            return self.robot

        else:
            # --- Import local libraries --- 
            from easygopigo3 import EasyGoPiGo3
            from RobotDexter import Dexter
            gpg = EasyGoPiGo3()
            self.robot = Dexter(gpg)
            return self.robot
            
    def run(self, sequence):
        self.sequence = sequence
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

        
# --- Global variables ---

COLLISION_DIST = 100
SPEED = 290

# --- Choose an option between 3D Simulation and Real World Action
while True:
    option = input ("Do you want to: A) Play simulation B) Control the robot. [a/b]? : ")
    if option in ['a', 'b']:
        break

opt_robot = Option(option)
robot = opt_robot.setup()

forward = ControllerForward(robot, SPEED, COLLISION_DIST)
turn = ControllerTurn(robot, SPEED, 25)
turn_ = ControllerTurn(robot, SPEED, -90)
follow = ControllerFollow(robot, SPEED, COLLISION_DIST)

learn = ControllerLearn(robot, "NN", SPEED)
forward_smart = ControllerForwardSmart (robot, learn, SPEED)

#sequence = [forward, turn_, forward, turn, forward, turn]
#sequence = [forward_smart]
sequence = [follow]

opt_robot.run(sequence)

robot.shutdown()
