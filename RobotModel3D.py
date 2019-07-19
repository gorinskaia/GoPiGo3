from panda3d.bullet import *
from panda3d.core import *
from direct.task import Task

import time
import math

#--- Main class ---

class Robot (BulletVehicle):
    def __init__ (self, render, world, sim):
        self.sim = sim
        self.world = world
        WHEEL_BASE_WIDTH         = 0.0065
        WHEEL_DIAMETER           = 0.66
        self.WHEEL_BASE_CIRCUMFERENCE = WHEEL_BASE_WIDTH * math.pi
        self.WHEEL_CIRCUMFERENCE      = WHEEL_DIAMETER   * math.pi
        self.CAMX = 320
        self.CAMY = 240

        self.total_distl = 0
        self.total_distr = 0
        self.last_posl = 0
        self.last_posr = 0
        self.x1l, self.y1l  = (0, 0)
        self.x1r, self.y1r  = (0, 0)

        # Chassis body
        shape = BulletBoxShape(Vec3(0.5,0.8,0.5))
        ts = TransformState.makePos(Point3(0, 0, 0.06))
        
        self.chassisNP = render.attachNewNode(BulletRigidBodyNode('Vehicle'))
        self.chassisNP.node().addShape(shape, ts)
        self.chassisNP.setPos(0, 0, 0)
        self.chassisNP.node().setMass(1)
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

        self.count = 1

        
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

    def set_speed(self, left_speed, right_speed):
        if left_speed == 0 and right_speed == 0:
            self.setBrake(100, 2)
            self.setBrake(50, 0)
            self.setBrake(50, 1)
            self.applyEngineForce(0, 0)
            self.applyEngineForce(0, 1)
        else:        
            self.setBrake(0.23, 2)
            self.applyEngineForce(left_speed/20, 1)
            self.applyEngineForce(right_speed/20, 0)
            
    def shutdown(self):
        self.set_speed(0,0)
            
    def reset(self):

        self.sim.distance = 1000
        self.set_speed(0,0)
        self.total_distl = 0
        self.total_distr = 0
        
        self.last_posl = self.wheelL.getPos()
        self.last_posr = self.wheelR.getPos()
        self.x1l, self.y1l  = (self.last_posl[0], self.last_posl[1])
        self.x1r, self.y1r  = (self.last_posr[0], self.last_posr[1])

    def get_offset(self):
        self.curr_posl = self.wheelL.getPos()
        self.curr_posr = self.wheelR.getPos()
        x2l, y2l  = (self.curr_posl[0], self.curr_posl[1])
        x2r, y2r  = (self.curr_posr[0], self.curr_posr[1])

        self.total_distl += math.sqrt(pow((x2l- self.x1l), 2) + pow((y2l- self.y1l), 2))
        self.total_distr += math.sqrt(pow((x2r- self.x1r), 2) + pow((y2r- self.y1r), 2))

        self.x1l, self.y1l  = (x2l, y2l)
        self.x1r, self.y1r  = (x2r, y2r)
        res = (self.total_distl, self.total_distr)
        return res
            
    def get_dist(self):
        return self.sim.distance

    def get_speed(self):
        return self.current_speed_km_hour

    def condition(self, ctrl):
        if ctrl.flag == False:
            self.sim.distance = 1000
        return ctrl.flag # Collision detections
        
    def odometry(self):
        cl = 1
        cr = 1
        coeff = 0
        
        left_steps, right_steps = self.get_offset()
        
        if left_steps>0 and right_steps>0:
            cl = self.WHEEL_CIRCUMFERENCE / left_steps
            cr = self.WHEEL_CIRCUMFERENCE / right_steps
            coeff = abs(cl-cr)
            if cr<cl:
                cl = 1
                cr = 1+coeff
            else:
                cr = 1
                cl = 1+coeff
        if cl>1 or cr>1:
            cl = 1
            cr = 1
        return cl, cr

    def get_image(self): 
        return self.sim.take_screenshot(self.CAMX, self.CAMY)
