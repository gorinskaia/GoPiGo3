from RobotModel3D import Robot

import sys
import math
import datetime
from images import Image_Processing

from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from panda3d.bullet import *
from direct.task import Task


class Simulation(ShowBase):
    
    def __init__(self):
        import direct.directbase.DirectStart

        base.cTrav = CollisionTraverser()
        #base.disableMouse()
        
        self.collHandEvent = CollisionHandlerEvent()
        self.collHandEvent.addInPattern('into-%in')

        self.robot = Robot (worldNP, world, self)
        self.sColl = self.initCollisionSphere(self.robot.robotModel, True, Point3(0,0,0))

        # Camera setting

        my_cam1 = Camera('cam1')
        self.my_camera1 = render.attachNewNode(my_cam1)
        self.my_camera1.setName('camera1')
        self.my_camera1.setPos(0, -0, 1)
        self.my_camera1.reparentTo(self.robot.chassisNP)

        my_cam2 = Camera('cam2')
        self.my_camera2 = render.attachNewNode(my_cam2)
        self.my_camera2.setName('camera2')
        self.my_camera2.setPos(0, 0, 70)
        self.my_camera2.lookAt(0,0,0)

        dr = base.camNode.getDisplayRegion(0)
        dr.setActive(0) 
        window = dr.getWindow()

        w, h = self.robot.CAMX*2, self.robot.CAMY
        props = WindowProperties() 
        props.setSize(w, h) 
        window.requestProperties(props)
        
        self.dr1 = window.makeDisplayRegion(0, 0.5, 0, 1)
        self.dr1.setSort(dr.getSort())
        self.dr2 = window.makeDisplayRegion(0.5, 1, 0, 1)
        self.dr2.setSort(dr.getSort())

        self.dr1.setCamera(self.my_camera1)
        self.dr2.setCamera(self.my_camera2)
        
        # Light
        alight = AmbientLight('ambientLight')
        alight.setColor(Vec4(0.9, 0.9, 0.9, 1))
        alightNP = render.attachNewNode(alight)
        alightNP.setPos(0,0,5)

        dlight = DirectionalLight('directionalLight')
        dlight.setColor(Vec4(0.9, 0.9, 0.9, 1))
        dlightNP = render.attachNewNode(dlight)
        dlightNP.setPos(0,0, 5)

        render.clearLight()
        render.setLight(alightNP)
        render.setLight(dlightNP)
            
        self.setup()
        
        self.walls(Point3(0,18,0), Point3(20, 0.1, 5), Point3(1, 0.05, 2.5), Point3(-1,-9,0), BulletBoxShape(Vec3(10, 0.01, 5)))
        self.walls(Point3(0,-18,0), Point3(20, 0.1, 5), Point3(1, 0.05, 2.5), Point3(-1,-9,0), BulletBoxShape(Vec3(10, 0.01, 5)))
        self.walls(Point3(-18,0,0), Point3(0.1, 20, 5), Point3(0.05, 1, 2.5), Point3(-10,-1,0), BulletBoxShape(Vec3(0.01, 10, 5)))
        self.walls(Point3(18,0,0), Point3(0.1, 20, 5), Point3(0.05, 1, 2.5), Point3(-10,-1,0), BulletBoxShape(Vec3(0.01, 10, 5)))
 
        taskMgr.add(self.update, 'updateWorld')

        self.distance = 1000

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
        #print('Collision distance', collEntry.getIntoNode().getName())
        self.distance = float(collEntry.getIntoNode().getName())
        self.ctrl.commands[self.ctrl.count].flag = True
        
    def initCollisionWall(self, obj, show, dist, center):
        collWallStr = 'CollisionWall' + "_" + obj.getName()
        cNode = CollisionNode(collWallStr)
        cNode.addSolid(CollisionBox(center, dist))
        cNodepath = obj.attachNewNode(cNode)
        if show:
            cNodepath.show()
        return (cNodepath, collWallStr)
        
    def initCollisionSphere(self, obj, show, center, num=0):
        collSphereStr = str(center[1]*30)
        #print (collSphereStr)
        cNode = CollisionNode(collSphereStr)
        cNode.addSolid(CollisionSphere (center, 0.2))
        cNodepath = obj.attachNewNode(cNode)
        if show:
            cNodepath.show()
        return (cNodepath, collSphereStr)


    def walls (self, pos, scale, wall1, wall2, shape):
        tex = loader.loadTexture("textures/text_photo.jpg")
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

    def take_screenshot(self, CAMX, CAMY):
        screen = self.dr1.getScreenshot()
        file_name = 'results/res.jpg'
        screen.write(file_name)
        img = Image_Processing(file_name, CAMX, CAMY)
        return img.coord()

worldNP = render.attachNewNode('World')
world = BulletWorld()
world.setGravity(Vec3(0, 0, -9.81))
    




