from direct.showbase.ShowBase import ShowBase
from panda3d.core import *  # Contains most of Panda's modules
from direct.gui.DirectGui import *  # Imports Gui objects we use for putting

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
        self.robot.reparentTo(render) # Reparent the model to render.
        self.robot.setPos(0, 30, 0)

        self.robot_tex = loader.loadTexture("models/robot.jpeg")
        self.robot.setTexture(self.robot_tex, 1)
                    
app = Environment()
base.run()
