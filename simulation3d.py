from direct.showbase.ShowBase import ShowBase
from panda3d.core import *  # Contains most of Panda's modules
from direct.gui.DirectGui import *  # Imports Gui objects we use for putting
from direct.interval.IntervalGlobal import Sequence

base = ShowBase()
import sys

class Environment():
    def __init__(self):
        self.title = OnscreenText(
            text="Robot simulation",
            parent=base.a2dBottomRight, align=TextNode.A_right,
            style=1, fg=(1, 1, 1, 1), pos=(-0.1, -0.1), scale=.07)

        base.setBackgroundColor(1, 1, 1)
        base.disableMouse()
        
        self.robot = loader.loadModel("cube") # Static Robot model
        self.robot.reparentTo(render) # Reparent the model to render = load an object onto the scene.
        self.robot.setPos(0, 30, 0)

        self.robot_tex = loader.loadTexture("textures/robot.jpeg")
        self.robot.setTexture(self.robot_tex, 1)

        PosInterval1 = self.robot.posInterval(13, Point3(0, 30, -5), startPos=Point3(0,30, 5))
        PosInterval2 = self.robot.posInterval(13, Point3(0, 30, 5), startPos=Point3(0, 30, -5))
        HprInterval1 = self.robot.hprInterval(3, Point3( 0,  0, 180), startHpr=Point3(0, 0, 0))
        HprInterval2 = self.robot.hprInterval(3, Point3(0, 0, 0), startHpr=Point3( 0, 0, 180))
 
        # Create and play the sequence that coordinates the intervals.
        self.Pace = Sequence(PosInterval1, HprInterval1, PosInterval2, HprInterval2, name="Pace")

        self.Pace.loop()
        
app = Environment()
base.run()
