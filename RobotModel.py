from panda3d.bullet import *
from panda3d.core import *
from direct.task import Task
import direct.directbase.DirectStart


class Robot (BulletVehicle):
    def __init__ (self, render, world):
        # Chassis body
        shape = BulletBoxShape(Vec3(0.5,0.8,0.5))
        ts = TransformState.makePos(Point3(0, 0, 0.06))
        
        chassisNP = render.attachNewNode(BulletRigidBodyNode('Vehicle'))
        chassisNP.node().addShape(shape, ts)
        chassisNP.setPos(0, 0, 0)
        chassisNP.node().setMass(10.0)
        chassisNP.node().setDeactivationEnabled(False)
        chassisNP.setScale (0.5,0.9,0.5)
         
        world.attachRigidBody(chassisNP.node())

        robot = loader.loadModel("cube") # Static Robot model
        robot.reparentTo (chassisNP) # Reparent the model to the node
        robot_tex = loader.loadTexture("textures/robot.jpeg")
        robot.setTexture(robot_tex, 1)

        # Vehicle
        super(Robot , self).__init__(world, chassisNP.node())
        self.setCoordinateSystem(ZUp)
        world.attachVehicle(self)

        # Wheel Right
        wheelR = loader.loadModel('models/wheel.egg')
        wheelR.reparentTo(render)
        self.addWheel(Point3(0.60, 0.75, 0.3), wheelR)

        # Wheel Left
        wheelL = loader.loadModel('models/wheel.egg')
        wheelL.reparentTo(render)
        self.addWheel(Point3(-0.60, 0.75, 0.3), wheelL)

        # Wheel back
        wheelB = loader.loadModel('models/wheel.egg')
        wheelB.reparentTo(render)
        self.addWheel(Point3(0, -0.75, 0.3), wheelB)

        #self.addObstacle(Point3(0,9,0), Vec3(10, 1, 5), world) # Later
        #self.addObstacle(Point3(0,-9,0), Vec3(10, 1, 5), world)
        #self.addObstacle(Point3(-10,0,0), Vec3(1, 10, 5), world)
        #self.addObstacle(Point3(10,0,0), Vec3(1, 10, 5), world)
        engineForce = 0.0
        brakeForce = 0.0

    def addObstacle(self, pos, scale, world):
        shape = BulletBoxShape(scale) # To be changes later ar a sensor distance
        ghost = BulletGhostNode('Ghost')
        ghost.addShape(shape)
        self.ghostNP = render.attachNewNode(ghost)
        self.ghostNP.setPos(pos)
        self.ghostNP.setCollideMask(BitMask32(0x0f))
        world.attachGhost(ghost)
        
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

    def setAngle(self, angle, dt):
        if angle>0:                         # Turn right
                self.applyEngineForce(0, 0)
                self.applyEngineForce(20, 1)
                self.setBrake(1, 2)
        else:                               # Turn left
            self.applyEngineForce(20, 0)
            self.applyEngineForce(0, 1)
            self.setBrake(10, 2)

    def setEngineForce(self, engineForce):
        self.applyEngineForce(engineForce, 0)
        self.applyEngineForce(engineForce, 1)

    def getAngle(self):
        return self.steering # Change and actually get the value

    def checkGhost(self, task):
        if task.time < 0.5:
            ghost = self.ghostNP.node()
            print(ghost.getNumOverlappingNodes())
            for node in ghost.getOverlappingNodes():
               print (node)
            return task.cont


class ControllerForward:
    def __init__(self, robot, speed = 30):
        self.speed = speed
        self.robot = robot
        
    def start(self):
        print("start forward")

    def stop(self):
        return False
    
    def update(self):
        self.robot.setEngineForce(self.speed)
