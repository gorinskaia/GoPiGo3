from RobotModel import Robot

import sys

from direct.showbase.ShowBase import ShowBase

from panda3d.core import *
from panda3d.bullet import *
from direct.task import Task


class Simulation(ShowBase):
    
    def __init__(self):
        base.setFrameRateMeter(True)
        base.cam.setPos(0, 0, 35)
        base.cam.lookAt(0, 0, 0)
        taskMgr.add(self.update, 'updateWorld')
        self.setup()
        self.walls()
        self.robot = Robot(self.worldNP, self.world)    # Create a robot, pass this later as a parameter to the sequence

    def update(self, task):
        dt = globalClock.getDt()
        self.processInput(dt, 'goStraight', 4)
        self.world.doPhysics(dt, 50, 0.008)
        return task.cont

    def setup(self):
        self.worldNP = render.attachNewNode('World')
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))

        # Make a plane
        shape = BulletPlaneShape(Vec3(0, 0, 1), 1)  # Collision shape
        node = BulletRigidBodyNode('Ground')        # Create a rigid body
        node.addShape(shape)                        # Add existing shape to it
        np = render.attachNewNode(node)
        np.setPos(0, 0, -1.5)
        self.world.attachRigidBody(node)            # Attach the rigid body node to the world


    def walls (self):

        shape = BulletBoxShape(Vec3(10, 0.1, 5))
        tex = loader.loadTexture("textures/wall.jpg")
        
        node = BulletRigidBodyNode('Box')
        node.setMass(0)
        node.addShape(shape)
        np = render.attachNewNode(node)
        np.setPos(0,9,0)
        self.world.attachRigidBody(node)
        self.box1 = loader.loadModel("cube")
        self.box1.setScale(10, 0.1, 5)
        self.box1.reparentTo(np)
        self.box1.setTexture(tex, 1)

        node = BulletRigidBodyNode('Box')
        node.setMass(0)
        node.addShape(shape)
        np = render.attachNewNode(node)
        np.setPos(0,-9,0)
        self.world.attachRigidBody(node)
        self.box1 = loader.loadModel("cube")
        self.box1.setScale(10, 0.1, 5)
        self.box1.reparentTo(np)
        self.box1.setTexture(tex, 1)

        shape = BulletBoxShape(Vec3(0.1, 10, 5))

        node = BulletRigidBodyNode('Box')
        node.setMass(0)
        node.addShape(shape)
        np = render.attachNewNode(node)
        np.setPos(-10,0,0)
        self.world.attachRigidBody(node)
        self.box1 = loader.loadModel("cube")
        self.box1.setScale(0.1, 10, 5)
        self.box1.reparentTo(np)
        self.box1.setTexture(tex, 1)

        node = BulletRigidBodyNode('Box')
        node.setMass(0)
        node.addShape(shape)
        np = render.attachNewNode(node)
        np.setPos(10,0,0)
        self.world.attachRigidBody(node)
        self.box1 = loader.loadModel("cube")
        self.box1.setScale(0.1, 10, 5)
        self.box1.reparentTo(np)
        self.box1.setTexture(tex, 1)

        
        
    def processInput(self, dt, command, value=0):
        engineForce = 0.0
        brakeForce = 0.0

        if command == 'goStraight':
            self.robot.setEngineForce(value)
            
        if command == 'stop':
            setBrakeForce(self, value)
            
        if command == 'turn':               #Change set angle to create an actual angle. Maybe with position, check the original robot formula.
                vehicle.setAngle(True, dt)
                

    def cleanup(self):
        self.world = None
        self.worldNP.removeNode()


sim = Simulation()
base.run()
