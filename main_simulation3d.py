from RobotModel3D import Robot

import sys
import math

from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from panda3d.bullet import *
from direct.task import Task

class Simulation(ShowBase):
    
    def __init__(self):
        import direct.directbase.DirectStart

        base.cTrav = CollisionTraverser()
        self.collHandEvent = CollisionHandlerEvent()
        self.collHandEvent.addInPattern('into-%in')

        self.robot = Robot (worldNP, world)
        self.sColl = self.initCollisionSphere(self.robot.robotModel, True, Point3(0,0,0))
  
        base.setFrameRateMeter(True)
        base.cam.setPos(0, 0, 35)
        base.cam.lookAt(0, 0, 0)
        
        self.setup()
        self.walls(Point3(0,9,0), Point3(10, 0.1, 5), Point3(1, 0.05, 2.5), Point3(-1,-9,0), BulletBoxShape(Vec3(10, 0.1, 5)))
        self.walls(Point3(0,-9,0), Point3(10, 0.1, 5), Point3(1, 0.05, 2.5), Point3(-1,-9,0), BulletBoxShape(Vec3(10, 0.1, 5)))
        self.walls(Point3(-10,0,0), Point3(0.1, 10, 5), Point3(0.05, 1, 2.5), Point3(-10,-1,0), BulletBoxShape(Vec3(0.1, 10, 5)))
        self.walls(Point3(10,0,0), Point3(0.1, 10, 5), Point3(0.05, 1, 2.5), Point3(-10,-1,0), BulletBoxShape(Vec3(0.1, 10, 5)))
 
        taskMgr.add(self.update, 'updateWorld')

    def update(self, task):
        dt = globalClock.getDt()
        world.doPhysics(dt, 50, 0.008)
        if not self.ctrl.stop():
            self.ctrl.update()
        else:
            return
        return task.cont

    def setup(self):
        shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
        node = BulletRigidBodyNode('Ground')
        node.addShape(shape)   
        np = render.attachNewNode(node)
        np.setPos(0, 0, -1.5)
        world.attachRigidBody(node) 

    def collide(self, collEntry):
        print('collide')
        self.ctrl.commands[self.ctrl.count].flag = True
        
    def initCollisionWall(self, obj, show, dist, center):
        collWallStr = 'CollisionWall' + "_" + obj.getName()
        cNode = CollisionNode(collWallStr)
        cNode.addSolid(CollisionBox(center, dist))
        cNodepath = obj.attachNewNode(cNode)
        if show:
            cNodepath.show()
        return (cNodepath, collWallStr)
        
    def initCollisionSphere(self, obj, show, center):
        collSphereStr = 'CollisionRobot' + "_" + obj.getName()
        cNode = CollisionNode(collSphereStr)
        cNode.addSolid(CollisionSphere (center, 0.2))
        cNodepath = obj.attachNewNode(cNode) 
        if show:
            cNodepath.show()
        return (cNodepath, collSphereStr)


    def walls (self, pos, scale, wall1, wall2, shape):
        tex = loader.loadTexture("textures/wall.jpg")
        
        node = BulletRigidBodyNode('Box')
        node.setMass(0)
        node.addShape(shape)
        np = render.attachNewNode(node)
        np.setPos(pos)
        world.attachRigidBody(node)
        self.box1 = loader.loadModel("cube")
        self.box1.setScale(scale)
        self.box1.reparentTo(np)
        self.box1.setTexture(tex, 1)

        tColl = self.initCollisionWall( self.box1, False, wall1, wall2) 
        base.cTrav.addCollider(tColl[0], self.collHandEvent) 


worldNP = render.attachNewNode('World')
world = BulletWorld()
world.setGravity(Vec3(0, 0, -9.81))
    




