from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import Sequence, Func, Wait
from panda3d.core import *
 
class World(DirectObject):
 
    def __init__( self ):
        # Initialize the traverser.
        base.cTrav = CollisionTraverser()
 
        # Initialize the handler.
        self.collHandEvent = CollisionHandlerEvent()
        self.collHandEvent.addInPattern('into-%in')
 
        # Make a variable to store the unique collision string count.
        self.collCount = 0
 
        # Load a model. Reparent it to the camera so we can move it.
        s = loader.loadModel('models/frowney')	
        s.reparentTo(camera)
        s.setPos(0, 25, 0)
 
        # Setup a collision solid for this model.
        sColl = self.initCollisionSphere(s, True)
 
        # Add this object to the traverser.
        base.cTrav.addCollider(sColl[0], self.collHandEvent)
 
        # Accept the events sent by the collisions.
        self.accept('into-' + sColl[1], self.collide)
 
        # Load another model.
        t = loader.loadModel('models/wheel')
        t.reparentTo(render)
        t.setPos(5, 25, 0)
 
        # Setup a collision solid for this model.
        tColl = self.initCollisionSphere(t, True)
 
        # Add this object to the traverser.
        base.cTrav.addCollider(tColl[0], self.collHandEvent)


    def collide(self, collEntry):
        print("WERT: object has collided into another object 1")

    def initCollisionSphere(self, obj, show=False):
        # Get the size of the object for the collision sphere.
        bounds = obj.getChild(0).getBounds()
        center = bounds.getCenter()
        radius = bounds.getRadius() * 1.1
 
        # Create a collision sphere and name it something understandable.
        collSphereStr = 'CollisionHull' + str(self.collCount) + "_" + obj.getName()
        self.collCount += 1
        cNode = CollisionNode(collSphereStr)
        cNode.addSolid(CollisionSphere(center, radius))
 
        cNodepath = obj.attachNewNode(cNode) # boundaries
 
 
        # Return a tuple with the collision node and its corrsponding string so
        # that the bitmask can be set.
        return (cNodepath, collSphereStr)
 
ShowBase()
# Run the world. Move around with the mouse to create collisions.
w = World()
run()
