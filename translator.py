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

while True:
    
    option = input ("Do you want to: A) Play simulation B) Control the robot. [a/b]? : ")
    if option in ['a', 'b']:
        break

if option == "a":

    import direct.directbase.DirectStart
    from RobotModel import Robot
    from main_simulation import Simulation

    sim = Simulation()


    forward = ControllerForward(robot, 300, COLLISION_DIST)
    turn90 = ControllerTurn(robot, 300, 90)
    sim.sequence = [turn90, forward,turn90]
    
    sim.ctrl = ControllerSequence(robot, self.sequence)
    sim.ctrl.start()

    base.run()

elif option == "b":
    import robotA
    
#class Translator:
    
    
"""gpg = EasyGoPiGo3()
dexter = Dexter(gpg)

forward = ControllerForward(dexter, 350, 150)
turn90 = ControllerTurn(dexter,350,90)

sequenceSquare = [forward, turn90, forward, turn90, forward, turn90, forward]

robot = ControllerSequence(dexter, sequenceSquare)

robot.start()"""


