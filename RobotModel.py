from panda3d.bullet import *
from panda3d.core import *
from direct.task import Task

import time
import math

#--- Main class ---

class Robot (BulletVehicle):
    def __init__ (self, render, world):

        self.world = world
        
        # Chassis body
        shape = BulletBoxShape(Vec3(0.5,0.8,0.5))
        ts = TransformState.makePos(Point3(0, 0, 0.06))
        
        self.chassisNP = render.attachNewNode(BulletRigidBodyNode('Vehicle'))
        self.chassisNP.node().addShape(shape, ts)
        self.chassisNP.setPos(0, 5, 0)
        self.chassisNP.node().setMass(5)
        self.chassisNP.node().setDeactivationEnabled(False)
        self.chassisNP.setScale (0.5,0.9,0.5)

        self.robotModel = loader.loadModel("cube")       # Static Robot model
        self.robotModel.reparentTo (self.chassisNP) # Reparent the model to the node
        robot_tex = loader.loadTexture("textures/robot.jpeg")
        self.robotModel.setTexture(robot_tex, 1)

        self.world.attachRigidBody(self.chassisNP.node())

        # Vehicle
        super(Robot , self).__init__(world, self.chassisNP.node())
        self.setCoordinateSystem(ZUp)
        world.attachVehicle(self)

        # Wheel Right
        self.wheelR = loader.loadModel('models/wheel.egg')
        self.wheelR.reparentTo(render)
        self.addWheel(Point3(0.60, 0.75, 0.3), self.wheelR)

        # Wheel Left
        self.wheelL = loader.loadModel('models/wheel.egg')
        self.wheelL.reparentTo(render)
        self.addWheel(Point3(-0.60, 0.75, 0.3), self.wheelL)

        # Wheel back
        self.wheelB = loader.loadModel('models/wheel.egg')
        self.wheelB.reparentTo(render)
        self.addWheel(Point3(0, -0.75, 0.3), self.wheelB)

        engineForce = 0.0
        brakeForce = 0.0
        
    def addWheel(self, pos, np):
        wheel = self.createWheel()
        
        wheel.setNode(np.node())
        wheel.setChassisConnectionPointCs(pos)
        wheel.setFrontWheel(True)
         
        wheel.setWheelDirectionCs(Vec3(0, 0, -1))
        wheel.setWheelAxleCs(Vec3(1, 0, 0))
        wheel.setWheelRadius(0.33)
        wheel.setMaxSuspensionTravelCm(40.0)
         
        wheel.setSuspensionStiffness(40.0)
        wheel.setWheelsDampingRelaxation(2.3)
        wheel.setWheelsDampingCompression(4.4)
        wheel.setFrictionSlip(100.0)
        wheel.setRollInfluence(0.1)

    def setAngle(self, angle, speed = 300):
        if angle>0:                         # Turn right
                self.applyEngineForce(0, 0)
                self.applyEngineForce(speed/6, 1)
                self.setBrake(1, 2)
        else:                               # Turn left
            self.applyEngineForce(speed/6, 0)
            self.applyEngineForce(0, 1)
            self.setBrake(1, 2)

    def setEngineForce(self, engineForce):
        self.applyEngineForce(engineForce, 0)
        self.applyEngineForce(engineForce, 1)

    def getOffset(self):
        pl = self.wheelL.getPos(self.wheelB)
        pr = self.wheelR.getPos(self.wheelB)
        left_pos = math.atan2(pl[2], pl[1])*(180/math.pi)
        right_pos = math.atan2(pr[2], pr[1])*(180/math.pi)
        #print (left_pos, right_pos)
        return (left_pos, right_pos)



#--- Controllers ---

class ControllerInit:
    'Initial state'
    def __init__(self,gpg):
        self.gpg = gpg
        
    def start(self):
        pass
    
    def stop(self):
        pass
    
    def update(self):
        pass
    
class ControllerForward:
    def __init__(self, robot, speed = 300, collision = 150):
        self.speed = speed/60
        self.robot = robot
        self.start_time = 0
        self.flag = False

    def start(self):
        self.robot.setEngineForce(0)
        self.robot.setBrake(0, 2)
        self.start_time = time.time()
        self.flag = False

    def stop(self):
        if self.flag == True:
            self.robot.setBrake(5, 2)
            self.robot.setEngineForce(0)
            return True
        return False
    
    def update(self):
        if self.stop():
            return
        self.robot.setEngineForce(self.speed)

class ControllerTurn:
    def __init__(self, robot , speed = 300, angle = 90):
        self.start_time = 0
        self.robot = robot
        self.angle = angle
        self.flag = False   # not useful for now
        self.speed = speed
        self.t_rotation = abs(angle/32.7)        # for 90 degrees is 2,75 sec of rotation
    def start(self):
        self.robot.setEngineForce(0)
        self.start_time = time.time()

    def stop(self):
        res = self.robot.getOffset()
        """offset = max(abs(res[1]), abs(res[0]))
        turn = ((WHEEL_CIRCUMFERENCE*offset)/(WHEEL_BASE_CIRCUMFERENCE))/2
        return abs(turn)>=abs(self.angle) """
        if time.time() - self.start_time > self.t_rotation:
            return True
        return False
    
    def update(self):
        if self.stop():
            return
        self.robot.setAngle(self.angle, self.speed)

class ControllerSequence:
    def __init__(self, robot, commands = []):
        self.robot = robot
        self.commands = []
        self.commands = [x for x in commands]
        self.count = 0 # Number of a command counter
        
    def start(self):
        self.count = -1
        print ('start')

    def stop(self):
        return self.count >= len(self.commands)
    
    def update(self):
        if self.stop():
            return
        if self.count < 0 or self.commands[self.count].stop():
            self.count+=1
            if self.stop():
                return
            self.commands[self.count].start()
        self.commands[self.count].update()
        
    def next (self):
        self.commands[self.count].flag = True

