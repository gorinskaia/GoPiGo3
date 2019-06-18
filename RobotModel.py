from panda3d.bullet import BulletWorld
from panda3d.core import *
from direct.task import Task
import direct.directbase.DirectStart
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletVehicle
from panda3d.bullet import ZUp

class Robot (BulletVehicle):
    def __init__ (self, render, world):
        # Chassis body
        shape = BulletBoxShape(Vec3(0.45, 0.98, 0.25))
        ts = TransformState.makePos(Point3(0, 0, 0.06))
        
        chassisNP = render.attachNewNode(BulletRigidBodyNode('Vehicle'))
        chassisNP.node().addShape(shape, ts)
        chassisNP.setPos(-1, 0, 0)
        #chassisNP.setScale(1.5,1.5,1.5)
        chassisNP.node().setMass(700.0)
        chassisNP.node().setDeactivationEnabled(False)
         
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
        self.addWheel(Point3(0.6, -0.95, 0.3), wheelR)

        # Wheel Left
        wheelL = loader.loadModel('models/wheel.egg')
        wheelL.reparentTo(render)

        self.addWheel(Point3(-0.60, -0.95, 0.3), wheelL)

        # Steering info
        steering = 0.0            # degree
        steeringClamp = 45.0      # degree
        steeringIncrement = 120.0 # degree per second
        
    def addWheel(self, pos, np):
        print('Adding a wheel')
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


    def getPosXYZ(self):
        # gettingPos
        position = self.getWheel(0).getNode()
        try:
            arrayOfStrings = str(position).split()
            z = arrayOfStrings[5]
            posXYZ = [float(arrayOfStrings[3]), float(arrayOfStrings[4]), float(z[:-1])]
            return (posXYZ)
        except IndexError:
            return ([0.0 , 0.0 , -200.0])   


    #function chor changin steering of front wheels
    def setAngle(self, left, dt):
        if(left):
            self.steering += dt * self.steeringIncrement
            self.steering = min(self.steering, self.steeringClamp)
        else:
            self.steering -= dt * self.steeringIncrement
            self.steering = max(self.steering, -self.steeringClamp)
        # Apply steering to front wheels
        self.setSteeringValue(self.steering, 0)
        self.setSteeringValue(self.steering, 1)

    #function that sets engine force of front wheels
    def setEngineForce(self, engineForce):
        self.applyEngineForce(engineForce, 0)
        self.applyEngineForce(engineForce, 1)

    #function that sets brake
    def setBrakeForce(self, brakeForce):
        self.setBrake(brakeForce, 2)
        self.setBrake(brakeForce, 3)


     #function that returns current steering of front wheels
    def getAngle(self):
        return self.steering




        # Apply steering to front wheels
        #vehicle.setSteeringValue(steering, 0)
        #vehicle.setSteeringValue(steering, 1)
         
        # Apply engine and brake to rear wheels
        #vehicle.applyEngineForce(engineForce, 0)
        #vehicle.applyEngineForce(engineForce, 3)
        #vehicle.setBrake(brakeForce, 2)
        #vehicle.setBrake(brakeForce, 3)



        #print(vehicle.getNumWheels())
        ###

"""def update(task):
    dt = globalClock.getDt()
    world.doPhysics(dt)
     
    vehicle.setSteeringValue(steering, 0)
    vehicle.applyEngineForce(engineForce, 0)

    return task.cont


taskMgr.add(update, 'update')

run()"""
