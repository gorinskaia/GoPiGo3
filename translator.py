#from Dexter import ControllerForward
#from Dexter import ControllerTurn
#from Dexter import ControllerSequence
#from Dexter import Dexter
from RobotModel import ControllerForward
from RobotModel import ControllerTurn
from RobotModel import ControllerSequence

from panda3d.core import *
from panda3d.bullet import *


COLLISION_DIST = 100
SPEED = 300

"""def start():
    if ctrl = sim.ctrl:"""
    

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
    dexter = Dexter(gpg)

# --- Your Code Goes Here ---

forward = ControllerForward(robot, 300, COLLISION_DIST)
turn90 = ControllerTurn(robot, 300, 90)
sequence = [turn90, forward,turn90]

# --- End Your Code ---

if option == "a":

    sim.ctrl = ControllerSequence(robot, sequence)
    sim.ctrl.start()
    base.run()
    


elif option == "b":
    import robotA

    

