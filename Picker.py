import sys
from direct.showbase import DirectObject
from direct.showbase.ShowBase import NodePath
from panda3d.core import *


class Picker(DirectObject.DirectObject):
    def __init__(self, base_object, select, unselect):
        DirectObject.DirectObject.__init__(self)
        self._camNode = base_object.camNode
        self._render = base_object.render
        self._mwn = base_object.mouseWatcherNode

        self.picker = CollisionTraverser()
        self.queue = CollisionHandlerQueue()
        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = base_object.cam.attachNewNode(self.pickerNode)

        self.pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        self.picker.addCollider(self.pickerNP, self.queue)

        # this holds the object that has been picked
        self.selected = None
        self.overlined = None
        self.picked_pos = None
        self.picked_normal = None
        self.select_func = select
        self.unselect_func = unselect

        self._mouse_X = 0.
        self._mouse_Y = 0.

        self.accept('mouse1', self.left_click)
        # self.accept('mouse3', self.right_click)

        self.pickable_objects = dict()
        base_object.taskMgr.add(self.mouse_move, 'mouse_move')

    def make_pickable(self, obj):
        obj.set_tag('pickable', 'true')

    def get_selected_object(self):
        return self.selected

    def get_selected_pos(self):
        return self.picked_pos

    def get_selected_normal(self):
        return self.picked_normal

    def get_object(self):
        self.pickerRay.setFromLens(self._camNode, self._mwn.getMouse())
        self.picker.traverse(self._render)
        if self.queue.getNumEntries() > 0:
            self.queue.sortEntries()
            for element in self.queue.getEntries():
                shallow_element = element.getIntoNodePath()
                while not shallow_element.get_tag('pickable') == 'true':
                    shallow_element = shallow_element.get_parent()
                    if shallow_element == self._render:
                        return None
                self.picked_pos = element.getSurfacePoint(shallow_element)
                self.picked_normal = element.getSurfaceNormal(shallow_element)
                return shallow_element

    def _select(self, event_name):
        element = self.get_object()
        if element is None and self.selected is not None:
            self.unselect_func(self.selected)
            self.selected = None
        elif element is not None and element != self.selected:
            self.unselect_func(self.selected)
            self.selected = element
            self.select_func(event_name, self.selected, self.picked_pos, self.picked_normal)

    def _overline(self):
        element = self.get_object()
        if element is None and self.overlined is not None:
            self.overlined.hide_bounds()
            self.overlined = None
        elif element is not None and element != self.overlined:
            if self.overlined is not None:
                self.overlined.hide_bounds()
            self.overlined = element
            self.overlined.show_tight_bounds()

    def left_click(self):
        self._select('left_click')

    def _mouse_moved(self):
        mpos = self._mwn.getMouse()
        if mpos.getX() != self._mouse_X or mpos.getY() != self._mouse_Y:
            self._mouse_X = mpos.getX()
            self._mouse_Y = mpos.getY()
            return True
        return False

    def mouse_move(self, task):
        if self._mwn.hasMouse() and self._mouse_moved():
            self._overline()
        return task.cont
