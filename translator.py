from Dexter import ControllerForward
from Dexter import ControllerTurn
from Dexter import ControllerSequence
from Dexter import Dexter
from easygopigo3 import EasyGoPiGo3

#from RobotModel import ControllerForward
#from RobotModel import ControllerTurn
#from RobotModel import ControllerSequence

#from panda3d.core import *
#from panda3d.bullet import *

import time


COLLISION_DIST = 150
SPEED = 300

while True:
    
    option = input ("Do you want to: A) Play simulation B) Control the robot. [a/b]? : ")
    if option in ['a', 'b']:
        break

if option == "a":

    import direct.directbase.DirectStart
    from RobotModel import Robot
    from main_simulation import Simulation

    sim = Simulation()
    sim.sColl = sim.initCollisionSphere(sim.robot.robotModel, True, Point3(0,COLLISION_DIST/30,1))
    base.cTrav.addCollider(sim.sColl[0], sim.collHandEvent)
    sim.accept('into-' + sim.sColl[1], sim.collide)
    robot = sim.robot

elif option == "b":
    import robotA
    gpg = EasyGoPiGo3()
    robot = Dexter(gpg)

# --- Your Code Goes Here ---

forward = ControllerForward(robot, 300, COLLISION_DIST)
turn90 = ControllerTurn(robot, 320, 90)

sequence = [forward, turn90, forward, turn90]

# --- End Your Code ---

if option == "a":
    sim.ctrl = ControllerSequence(robot, sequence)
    sim.ctrl.start()
    base.run()

elif option == "b":
    ctrl = ControllerSequence(robot, sequence)
    ctrl.start()
    while not ctrl.stop():
        ctrl.update()
        time.sleep(0.01)
    robot.shutdown()

    

