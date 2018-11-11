from direct.showbase import DirectObject
from panda3d.core import *


class KeyEvent(DirectObject.DirectObject):
    def __init__(self, base_object):
        DirectObject.DirectObject.__init__(self)
        self.camera = base_object.rts_camera
        self.picker = base_object.picker
        self.mwn = base_object.mouseWatcherNode

        self.velocity = 1.0

        self.accept('space', self.space_press)
        self.accept('a', self.a_press)
        # self.accept('arrow_up-repeat', self.up_arrow)
        # self.accept('arrow_down-repeat', self.down_arrow)
        # self.accept('arrow_right-repeat', self.right_arrow)
        # self.accept('arrow_left-repeat', self.left_arrow)

        # forward_speed = 5.0  # units per second
        # backward_speed = 2.0
        # forward_button = KeyboardButton.ascii_key('arrow_up')

        # base_object.taskMgr.add(self.move_task, 'event_move')

    # def move_task(self, task):
    #     is_down = self.mwn.is_button_down
    #     print(is_down)
    #     if is_down(KeyboardButton.ascii_key('arrow_up')):
    #         print('up !')

    def a_press(self):
        self.camera.use_pan_zone(None)

    def space_press(self):
        selected_object = self.picker.get_selected_object()
        if selected_object is not None:
            self.camera.set_target(selected_object.getPos())

    def right_arrow(self):
        self.camera.move(dx=self.velocity)

    def left_arrow(self):
        self.camera.move(dx=- self.velocity)

    def up_arrow(self):
        self.camera.move(dy=self.velocity)

    def down_arrow(self):
        self.camera.move(dy=-self.velocity)
