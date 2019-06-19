from RobotModel import Robot
from RobotModel import ControllerForward
from RobotModel import ControllerTurn
from RobotModel import ControllerSequence

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

        self.setup()
        self.walls()
        self.robot = Robot(self.worldNP, self.world)    # Create a rosbot, pass this later as a parameter to the sequence
        
        taskMgr.add(self.update, 'updateWorld')
        #taskMgr.add(self.robot.checkGhost, 'checkGhost') # Later

        forward = ControllerForward(self.robot, 65)
        turn = ControllerTurn(self.robot, 90)
        sequence = [turn, forward, turn]
                
        self.ctrl = ControllerSequence(self.robot, sequence)
        self.ctrl.start()
        
        '''self.cTrav = CollisionTraverser()
        self.queue = CollisionHandlerQueue()'''


    def update(self, task):
        dt = globalClock.getDt()
        self.world.doPhysics(dt, 50, 0.008)
        
        if not self.ctrl.stop():
            self.ctrl.update()
        else:
            return

        '''self.cTrav.addCollider(self.robot.chassisNP, self.queue)
        self.cTrav.traverse(render)
        for entry in self.queue.getEntries():
            print(entry)'''
    

        return task.cont

    def setup(self):
        self.worldNP = render.attachNewNode('World')
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))

        shape = BulletPlaneShape(Vec3(0, 0, 1), 1)  # Collision shape: Plane
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

sim = Simulation()
base.run()




