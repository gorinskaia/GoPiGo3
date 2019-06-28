# --- Global libraries --- 
import time
from Controller import ControllerInit
from Controller import ControllerForward
from Controller import ControllerTurn
from Controller import ControllerSequence
import numpy

# --- Global variables --- 
COLLISION_DIST = 120
SPEED = 300

# --- Choose an option between 3D Simulation and Real World Action
'''while True:
    option = input ("Do you want to: A) Play simulation B) Control the robot. [a/b]? : ")
    if option in ['a', 'b']:
        break
'''
option = "a"
#option = "b"

if option == "a":

    # --- Import local libraries ---
    from panda3d.core import *
    from panda3d.bullet import *
    import direct.directbase.DirectStart
    from RobotModel3D import Robot
    from main_simulation3d import Simulation

    sim = Simulation()

    for i in numpy.arange(0, COLLISION_DIST/30, 0.5):
        sim.sColl = sim.initCollisionSphere(sim.robot.robotModel, True, Point3(0,(COLLISION_DIST/30)-i,1))
        base.cTrav.addCollider(sim.sColl[0], sim.collHandEvent)
        sim.accept('into-' + sim.sColl[1], sim.collide)
    
    robot = sim.robot

elif option == "b":
    
    # --- Import local libraries --- 
    from easygopigo3 import EasyGoPiGo3
    import main_robotA
    
    gpg = EasyGoPiGo3()
    robot = Dexter(gpg)

# --------------------------
# --- Your Sequence Goes Here ---

forward = ControllerForward(robot, 300, COLLISION_DIST)
turn90 = ControllerTurn(robot, 500, 90)
turn90_ = ControllerTurn(robot, 350, -50)

sequence = [turn90, forward, turn90_, forward, turn90, forward, turn90_, forward, turn90]

# --- End Your Code ---
# --------------------------

# --- Run ---
if option == "a":
    sim.ctrl = ControllerSequence(sequence)
    sim.ctrl.start()
    base.run()
    robot.shutdown()

elif option == "b":
    ctrl = ControllerSequence(sequence)
    ctrl.start()
    while not ctrl.stop():
        ctrl.update()
        time.sleep(0.01)
    robot.shutdown()
