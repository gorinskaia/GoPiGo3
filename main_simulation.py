from RobotModel import Robot

import sys
import _thread as thread

from direct.showbase.ShowBase import ShowBase

from panda3d.core import *
from panda3d.bullet import *

from direct.task import Task


class Simulation(ShowBase):
    
    def __init__(self):
        #base.setBackgroundColor(0.1, 0.1, 0.8)
        base.setFrameRateMeter(True)
        base.cam.setPos(0, 0, 50)
        base.cam.lookAt(0, 0, 0)
        taskMgr.add(self.update, 'updateWorld')
        self.setup()


    def update(self, task):
        dt = globalClock.getDt()
        
        #self.robot.setAngle(90, dt)
        
        self.processInput(dt)
        self.world.doPhysics(dt, 10, 0.008)

        return task.cont

    def setup(self):
        self.worldNP = render.attachNewNode('World')
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))

        self.robot = Robot(self.worldNP, self.world)

        # Make a plane
        shape = BulletPlaneShape(Vec3(0, 0, 1), 1)  # Collision shape
        node = BulletRigidBodyNode('Ground')        # Create a rigid body
        node.addShape(shape)                        # Add existing shape to it
        np = render.attachNewNode(node)
        np.setPos(0, 0, -1.5)
        self.world.attachRigidBody(node)            # Attach the rigid body node to the world"""

    def processInput(self, dt):
        engineForce = 10.0
        brakeForce = 0.0

        self.robot.applyEngineForce(0, 0)
        self.robot.applyEngineForce(engineForce, 1)
        
        #self.robot.setAngle(True, dt)

        """ if inputState.isSet('forward'):
                engineForce = 1000.0
                brakeForce = 0.0

            if inputState.isSet('backward'):
                engineForce = -1000.0
                brakeForce = 0.0

            if inputState.isSet('reverse'):
                engineForce = 0.0
                brakeForce = 100.0

            if inputState.isSet('left'):
                vehicle.setAngle(True, dt)

            if inputState.isSet('right'):
                vehicle.setAngle(False, dt)"""

    def cleanup(self):
        self.world = None
        self.worldNP.removeNode()


sim = Simulation()
base.run()
