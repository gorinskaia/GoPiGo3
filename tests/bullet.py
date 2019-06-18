from panda3d.bullet import BulletWorld
from panda3d.core import *
from direct.task import Task
import direct.directbase.DirectStart
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletVehicle

base.cam.setPos(0, -10, 0)
base.cam.lookAt(0, 0, 0)

world = BulletWorld()
world.setGravity(Vec3(0, 0, -9.81))

# Make a plane
shape = BulletPlaneShape(Vec3(0, 0, 1), 1)  # Collision shape
node = BulletRigidBodyNode('Ground')        # Create a rigid body
node.addShape(shape)                        # Add existing shape to it
np = render.attachNewNode(node)
np.setPos(0, 0, -2)
world.attachRigidBody(node)                 # Attach the rigid body node to the world


# Dynamic body
shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
ts = TransformState.makePos(Point3(0, 0, 0.5))

"""node = BulletRigidBodyNode('Box')
node.setMass(1.0)
node.addShape(shape)
np = render.attachNewNode(node)
np.setPos(0, 30, 0)
world.attachRigidBody(node)
"""

chassisNP = render.attachNewNode(BulletRigidBodyNode('Vehicle'))
chassisNP.node().addShape(shape, ts)
chassisNP.setPos(0, 0, 1)
chassisNP.node().setMass(800.0)
chassisNP.node().setDeactivationEnabled(False)
 
world.attachRigidBody(chassisNP.node())

robot = loader.loadModel("cube") # Static Robot model
robot.reparentTo (chassisNP) # Reparent the model to the node

robot_tex = loader.loadTexture("textures/robot.jpeg")
robot.setTexture(robot_tex, 1)


def update(task):
  dt = globalClock.getDt()
  world.doPhysics(dt)
  return task.cont


taskMgr.add(update, 'update')

run()
