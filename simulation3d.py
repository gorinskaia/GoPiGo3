from direct.showbase.ShowBase import ShowBase
from panda3d.core import *  # Contains most of Panda's modules
from direct.gui.DirectGui import *  # Imports Gui objects we use for putting
from direct.interval.IntervalGlobal import Sequence
from panda3d.ode import *
#from direct.directbase import DirectStart
#from direct.directtools.DirectGeometry import LineNodePath
import sys

base = ShowBase()


class Environment():
    def __init__(self):
        self.title = OnscreenText(
            text="Robot simulation",
            parent=base.a2dBottomRight, align=TextNode.A_right,
            style=1, fg=(1, 1, 1, 1), pos=(-0.1, -0.1), scale=.07)

        base.setBackgroundColor(1, 1, 1)
        base.disableMouse()
        
        world = OdeWorld()
        world.setGravity(0, 0, -9.81)
        
        self.robot = loader.loadModel("cube") # Static Robot model
        self.robot.reparentTo(render) # Reparent the model to render = load an object onto the scene.
        self.robot.setPos(0, 30, 0)

        self.wheelL = loader.loadModel("cube") # Static Robot model
        self.wheelL.setScale(0.4)
        self.wheelL.reparentTo(render) # Reparent the model to render = load an object onto the scene.
        self.wheelL.setPos(1, 30, 0)

        self.wheelR = loader.loadModel("cube") # Static Robot model
        self.wheelR.setScale(0.4)
        self.wheelR.reparentTo(render) # Reparent the model to render = load an object onto the scene.
        self.wheelR.setPos(-1, 30, 0)

        self.robot_tex = loader.loadTexture("textures/robot.jpeg")
        self.wheel_tex = loader.loadTexture("textures/wheel.jpg")
        self.robot.setTexture(self.robot_tex, 1)
        self.wheelL.setTexture(self.wheel_tex, 1)
        self.wheelR.setTexture(self.wheel_tex, 1)

        # Setup the body for the robot
        robotBody = OdeBody(world)
        M = OdeMass()
        M.setSphere(5000, 1.0)
        robotBody.setMass(M)
        robotBody.setPosition(self.robot.getPos(render))
        robotBody.setQuaternion(self.robot.getQuat(render))

        # Now, the body for the wheels
        wheelLBody = OdeBody(world)
        M = OdeMass()
        M.setSphere(5000, 1.0)
        wheelLBody.setMass(M)
        wheelLBody.setPosition(self.wheelL.getPos(render))
        wheelLBody.setQuaternion(self.wheelL.getQuat(render))

        wheelRBody = OdeBody(world)
        M = OdeMass()
        M.setSphere(5000, 1.0)
        wheelRBody.setMass(M)
        wheelRBody.setPosition(self.wheelR.getPos(render))
        wheelRBody.setQuaternion(self.wheelR.getQuat(render))
       
       
        # Create the joints
        self.robotJoint = OdeBallJoint(world)
        self.robotJoint.setAnchor(0, 0, 0)
        
        self.wheelLJoint = OdeBallJoint(world)
        self.wheelLJoint.attach(robotBody, wheelLBody)
        self.wheelLJoint.setAnchor(-5, 0, -5)

        self.wheelRJoint = OdeBallJoint(world)
        self.wheelRJoint.attach(robotBody, wheelRBody)
        self.wheelRJoint.setAnchor(-5, 0, -5)
        
        
        
        def simulationTask(task):
          # Step the simulation and set the new positions
          world.quickStep(globalClock.getDt())
          self.wheelL.setPosQuat(render, wheelLBody.getPosition(), Quat(wheelLBody.getQuaternion()))
          self.wheelR.setPosQuat(render, wheelRBody.getPosition(), Quat(wheelRBody.getQuaternion()))
          self.robot.setPosQuat(render, robotBody.getPosition(), Quat(robotBody.getQuaternion()))

          return task.cont
        taskMgr.doMethodLater(0.5, simulationTask, "Physics Simulation")

        robotBody.setForce(0, 5000000,  0)
        
        '''PosInterval1 = self.robot.posInterval(13, Point3(0, 30, -5), startPos=Point3(0, 30, 0))
        PosInterval2 = self.robot.posInterval(13, Point3(0, 30, 0), startPos=Point3(0, 30, -5))
        HprInterval1 = self.robot.hprInterval(3, Point3( 0,  0, 180), startHpr=Point3(0, 0, 0))
        HprInterval2 = self.robot.hprInterval(3, Point3(0, 0, -5), startHpr=Point3( 0, 0, 180))
 
        # Create and play the sequence that coordinates the intervals.
        self.Pace = Sequence(PosInterval1, HprInterval1, PosInterval2, HprInterval2, name="Pace")

        self.Pace.loop()'''

       # base.localAvatar.physControls.avatarControlForwardSpeed= +speed #sets speed - try this
        
app = Environment()
base.run()
