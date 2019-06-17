from direct.showbase.ShowBase import ShowBase
base = ShowBase()

from panda3d.core import NodePath, TextNode
from panda3d.core import *  # Contains most of Panda's modules
from direct.gui.DirectGui import *  # Imports Gui objects we use for putting text on the screen
import sys

class World(object):  # Our main class
    def __init__(self):
        
        self.title = OnscreenText(
            text="Panda3D: Tutorial 1 - Solar System",
            parent=base.a2dBottomRight, align=TextNode.A_right,
            style=1, fg=(1, 1, 1, 1), pos=(-0.1, 0.1), scale=.07)
        
        self.yearscale = 60  # Number of seconds a full rotation of Earth around the sun should take

        self.sizescale = 0.6  # relative size of planets
        self.orbitscale = 10  # relative size of orbits
      
        base.setBackgroundColor(0, 0, 0)   # Make the background color black (R=0, G=0, B=0)
        base.disableMouse()

        camera.setPos(0, 0, 45) # Set the camera position (x, y, z)
        camera.setHpr(0, -90, 0) # Set the camera orientation (heading, pitch, roll) in degrees

        # Number of seconds a day rotation of Earth should take.
        # It is scaled from its correct value for easier visability
        self.dayscale = self.yearscale / 365.0 * 5
        self.orbitscale = 10  # Orbit scale
        self.sizescale = 0.6  # Planet size scale

        
        self.loadPlanets()
        self.rotatePlanets()

    def loadPlanets(self):

         # This system of attaching NodePaths to each other is called the Scene Graph
        self.orbit_root_mercury = render.attachNewNode('orbit_root_mercury')
        self.orbit_root_venus = render.attachNewNode('orbit_root_venus')
        self.orbit_root_mars = render.attachNewNode('orbit_root_mars')
        self.orbit_root_earth = render.attachNewNode('orbit_root_earth')
        self.orbit_root_moon = (self.orbit_root_earth.attachNewNode('orbit_root_moon'))  # The moon orbits Earth, not the sun
        
            # When you load a file you leave the extension off so that it can choose the right version
            # The sky is different from the planet model because its polygons
            # (which are always one-sided in Panda) face inside the sphere instead of
            # outside (this is known as a model with reversed normals). 
        self.sky = loader.loadModel("models/solar_sky_sphere")
        self.sky.reparentTo(render)
        self.sky.setScale(40)
        self.sky_tex = loader.loadTexture("models/stars_1k_tex.jpg") # Setting texture
        self.sky.setTexture(self.sky_tex, 1) # The second argument must be one or the command will be ignored.

        self.sun = loader.loadModel("models/planet_sphere")
        self.sun.reparentTo(render)
        self.sun_tex = loader.loadTexture("models/sun_1k_tex.jpg")
        self.sun.setTexture(self.sun_tex, 1)
        self.sun.setScale(2 * self.sizescale)

        # Load mercury
        self.mercury = loader.loadModel("models/planet_sphere")
        self.mercury_tex = loader.loadTexture("models/mercury_1k_tex.jpg")
        self.mercury.setTexture(self.mercury_tex, 1)
        self.mercury.reparentTo(self.orbit_root_mercury)
        # Set the position of mercury. By default, all nodes are pre assigned the
        # position (0, 0, 0) when they are first loaded. We didn't reposition the
        # sun and sky because they are centered in the solar system. Mercury,
        # however, needs to be offset so we use .setPos to offset the
        # position of mercury in the X direction with respect to its orbit radius.
        # We will do this for the rest of the planets.
        self.mercury.setPos(0.38 * self.orbitscale, 0, 0)
        self.mercury.setScale(0.385 * self.sizescale)

        # Load Venus
        self.venus = loader.loadModel("models/planet_sphere")
        self.venus_tex = loader.loadTexture("models/venus_1k_tex.jpg")
        self.venus.setTexture(self.venus_tex, 1)
        self.venus.reparentTo(self.orbit_root_venus)
        self.venus.setPos(0.72 * self.orbitscale, 0, 0)
        self.venus.setScale(0.923 * self.sizescale)

        # Load Mars
        self.mars = loader.loadModel("models/planet_sphere")
        self.mars_tex = loader.loadTexture("models/mars_1k_tex.jpg")
        self.mars.setTexture(self.mars_tex, 1)
        self.mars.reparentTo(self.orbit_root_mars)
        self.mars.setPos(1.52 * self.orbitscale, 0, 0)
        self.mars.setScale(0.515 * self.sizescale)

        # Load Earth
        self.earth = loader.loadModel("models/planet_sphere")
        self.earth_tex = loader.loadTexture("models/earth_1k_tex.jpg")
        self.earth.setTexture(self.earth_tex, 1)
        self.earth.reparentTo(self.orbit_root_earth)
        self.earth.setScale(self.sizescale)
        self.earth.setPos(self.orbitscale, 0, 0)

        # The center of the moon's orbit is exactly the same distance away from
        # The sun as the Earth's distance from the sun
        self.orbit_root_moon.setPos(self.orbitscale, 0, 0)

        # Load the moon
        self.moon = loader.loadModel("models/planet_sphere")
        self.moon_tex = loader.loadTexture("models/moon_1k_tex.jpg")
        self.moon.setTexture(self.moon_tex, 1)
        self.moon.reparentTo(self.orbit_root_moon)
        self.moon.setScale(0.1 * self.sizescale)
        self.moon.setPos(0.1 * self.orbitscale, 0, 0)

    def rotatePlanets(self):
        self.day_period_sun = self.sun.hprInterval(20, (360, 0, 0))

        self.orbit_period_mercury = self.orbit_root_mercury.hprInterval(
            (0.241 * self.yearscale), (360, 0, 0))
        self.day_period_mercury = self.mercury.hprInterval(
            (59 * self.dayscale), (360, 0, 0))

        self.orbit_period_venus = self.orbit_root_venus.hprInterval(
            (0.615 * self.yearscale), (360, 0, 0))
        self.day_period_venus = self.venus.hprInterval(
            (243 * self.dayscale), (360, 0, 0))

        self.orbit_period_earth = self.orbit_root_earth.hprInterval(
            self.yearscale, (360, 0, 0))
        self.day_period_earth = self.earth.hprInterval(
            self.dayscale, (360, 0, 0))

        self.orbit_period_moon = self.orbit_root_moon.hprInterval(
            (.0749 * self.yearscale), (360, 0, 0))
        self.day_period_moon = self.moon.hprInterval(
            (.0749 * self.yearscale), (360, 0, 0))

        self.orbit_period_mars = self.orbit_root_mars.hprInterval(
            (1.881 * self.yearscale), (360, 0, 0))
        self.day_period_mars = self.mars.hprInterval(
            (1.03 * self.dayscale), (360, 0, 0))

        self.day_period_sun.loop()
        self.orbit_period_mercury.loop()
        self.day_period_mercury.loop()
        self.orbit_period_venus.loop()
        self.day_period_venus.loop()
        self.orbit_period_earth.loop()
        self.day_period_earth.loop()
        self.orbit_period_moon.loop()
        self.day_period_moon.loop()
        self.orbit_period_mars.loop()
        self.day_period_mars.loop()

w = World()


base.run()
