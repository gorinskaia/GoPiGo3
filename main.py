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
            #import main_robotA #Camera thread continious
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

COLLISION_DIST = 120
SPEED = 300

# --- Choose an option between 3D Simulation and Real World Action
while True:
    option = input ("Do you want to: A) Play simulation B) Control the robot. [a/b]? : ")
    if option in ['a', 'b']:
        break

opt_robot = Option(option)
robot = opt_robot.setup()

forward = ControllerForward(robot, 300, COLLISION_DIST)
turn = ControllerTurn(robot, 300, 90)
turn_ = ControllerTurn(robot, 300, -90)

sequence = [turn_, forward, turn]

'''thread = threading.Thread(target=robot.get_image, daemon = True)
thread.start()
image = thread.join()'''


opt_robot.run(sequence)
robot.shutdown()
