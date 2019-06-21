from RobotModel import Robot
from RobotModel import ControllerForward
from RobotModel import ControllerTurn
from RobotModel import ControllerSequence
from RobotModel import ControllerInit

import sys
import math

from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from panda3d.bullet import *
from direct.task import Task

COLLISION_DIST = 100
SPEED = 300

class Simulation(ShowBase):
    
    def __init__(self):

        import direct.directbase.DirectStart

        base.cTrav = CollisionTraverser()
        self.collHandEvent = CollisionHandlerEvent()
        self.collHandEvent.addInPattern('into-%in')

        self.collCount = 0  # unique collision string count.
        
        self.robot = Robot (worldNP, world)
        
        base.setFrameRateMeter(True)
        base.cam.setPos(0, 0, 35)
        base.cam.lookAt(0, 0, 0)
        
        self.setup()
        self.walls()
 
        taskMgr.add(self.update, 'updateWorld')

        

        #forward = ControllerForward(robot, 300, COLLISION_DIST)
        #turn90 = ControllerTurn(robot, 300, 90)
        #turn45 = ControllerTurn(robot, SPEED, -45)
        #turn180 = ControllerTurn(robot, 300, -90)
        #sequence = [turn90, forward, turn180, turn45, forward]
        #self.sequence = [turn90, forward,turn90]
        self.sequence = []  
        #self.ctrl = ControllerInit(robot)
        #self.ctrl.start()

    def update(self, task):
        dt = globalClock.getDt()
        world.doPhysics(dt, 50, 0.008)
    
        if not self.ctrl.stop():
            self.ctrl.update()

        else:
            return
        
        return task.cont

    def setup(self):
        shape = BulletPlaneShape(Vec3(0, 0, 1), 1)  # Collision shape: Plane
        node = BulletRigidBodyNode('Ground')        # Create a rigid body
        node.addShape(shape)                        # Add existing shape to it
        np = render.attachNewNode(node)
        np.setPos(0, 0, -1.5)
        world.attachRigidBody(node)            # Attach the rigid body node to the world

    
        # Setup a collision solid for this model.
        sColl = self.initCollisionSphere(self.robot.robotModel, True, Point3(0,COLLISION_DIST/30,1))
        base.cTrav.addCollider(sColl[0], self.collHandEvent)
        self.accept('into-' + sColl[1], self.collide)

    def collide(self, collEntry):
        print ('collide')
        self.ctrl.next()
        

    def initCollisionWall(self, obj, show, dist, center):

        collWallStr = 'CollisionWall' + str(self.collCount) + "_" + obj.getName()
        cNode = CollisionNode(collWallStr)
        cNode.addSolid(CollisionBox(center, dist))
        cNodepath = obj.attachNewNode(cNode) # boundaries
        if show:
            cNodepath.show()
        return (cNodepath, collWallStr)
        
    def initCollisionSphere(self, obj, show, center):
        
        collSphereStr = 'CollisionRobot' + str(self.collCount) + "_" + obj.getName()
        self.collCount += 1
        cNode = CollisionNode(collSphereStr)
        cNode.addSolid(CollisionSphere (center, 0.5))
        cNodepath = obj.attachNewNode(cNode) # boundaries
        if show:
            cNodepath.show()
        return (cNodepath, collSphereStr)


    def walls (self):
        shape = BulletBoxShape(Vec3(10, 0.1, 5))
        tex = loader.loadTexture("textures/wall.jpg")
        
        node = BulletRigidBodyNode('Box')
        node.setMass(0)
        node.addShape(shape)
        np = render.attachNewNode(node)
        np.setPos(0,9,0)
        world.attachRigidBody(node)
        self.box1 = loader.loadModel("cube")
        self.box1.setScale(10, 0.1, 5)
        self.box1.reparentTo(np)
        self.box1.setTexture(tex, 1)

        tColl = self.initCollisionWall( self.box1, True, Point3(1, 0.05, 2.5), Point3(-1,-9,0))  # Setup a collision solid for this model.
        base.cTrav.addCollider(tColl[0], self.collHandEvent) # Add this object to the traverser.

        node = BulletRigidBodyNode('Box')
        node.setMass(0)
        node.addShape(shape)
        np = render.attachNewNode(node)
        np.setPos(0,-9,0)
        world.attachRigidBody(node)
        self.box1 = loader.loadModel("cube")
        self.box1.setScale(10, 0.1, 5)
        self.box1.reparentTo(np)
        self.box1.setTexture(tex, 1)

        tColl = self.initCollisionWall( self.box1, True, Point3(1, 0.05, 2.5), Point3(-1,-9,0))
        base.cTrav.addCollider(tColl[0], self.collHandEvent)

        shape = BulletBoxShape(Vec3(0.1, 10, 5))

        node = BulletRigidBodyNode('Box')
        node.setMass(0)
        node.addShape(shape)
        np = render.attachNewNode(node)
        np.setPos(-10,0,0)
        world.attachRigidBody(node)
        self.box1 = loader.loadModel("cube")
        self.box1.setScale(0.1, 10, 5)
        self.box1.reparentTo(np)
        self.box1.setTexture(tex, 1)
                
        tColl = self.initCollisionWall( self.box1, True, Point3(0.05, 1, 2.5), Point3(-10,-1,0))
        base.cTrav.addCollider(tColl[0], self.collHandEvent)

        node = BulletRigidBodyNode('Box')
        node.setMass(0)
        node.addShape(shape)
        np = render.attachNewNode(node)
        np.setPos(10,0,0)
        world.attachRigidBody(node)
        self.box1 = loader.loadModel("cube")
        self.box1.setScale(0.1, 10, 5)
        self.box1.reparentTo(np)
        self.box1.setTexture(tex, 1)
       
        tColl = self.initCollisionWall( self.box1, True, Point3(0.05, 1, 2.5), Point3(-10,-1,0))
        base.cTrav.addCollider(tColl[0], self.collHandEvent)

worldNP = render.attachNewNode('World')
world = BulletWorld()
world.setGravity(Vec3(0, 0, -9.81))
    




