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
        self.chassisNP.setPos(0, -5, 0)
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

    def forward(self, engineForce):
        self.applyEngineForce(engineForce/100, 0)
        self.applyEngineForce(engineForce/100, 1)

    def reset(self):
        self.forward(0)
        self.setBrake(0, 2)
        
    def condition(self, ctrl):
        return ctrl.flag

    def angle_reached(self, ctrl):
        if time.time() - ctrl.start_time > ctrl.t_rotation:
            return True
        return False
