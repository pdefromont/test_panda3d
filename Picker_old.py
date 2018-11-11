from pandac.PandaModules import *
from direct.showbase import DirectObject


class Picker(DirectObject.DirectObject):
    def __init__(self, engine):
        super(Picker, self).__init__()
        #setup collision stuff

        self.engine = engine
        self.mpos = self.engine.mouseWatcherNode

        self.picker = CollisionTraverser()
        self.queue = CollisionHandlerQueue()
        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = self.engine.camera.attachNewNode(self.pickerNode)

        self.pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.pickerRay = CollisionRay()

        self.pickerNode.addSolid(self.pickerRay)
        self.picker.addCollider(self.pickerNode, self.queue)

        self.picked_obj = None

        # self.accept('mouse1', self.printMe)
        #this function is meant to flag an object as being somthing we can pick

    def set_pickable(self, obj):
        obj.setTag('pickable', True)

    #this function finds the closest object to the camera that has been hit by our ray
    def getObjectHit(self): #mpos is the position of the mouse on the screen
        self.picked_obj = None
        self.pickerRay.setFromLens(self.engine.camNode, self.mpos.getX(), self.mpos.getY())
        self.picker.traverse(self.engine.render)
        if self.queue.getNumEntries() > 0:
            self.queue.sortEntries()
            self.picked_obj = self.queue.getEntry(0).getIntoNodePath()
            parent = self.picked_obj.getParent()

            self.picked_obj = None
            while parent != self.engine.render:
                if parent.getTag('pickable'):
                    print(self.picked_obj)
                    self.picked_obj = parent
                    return parent
            else:
                parent = parent.getParent()
        return None
