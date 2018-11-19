import time

import numpy as num
from direct.showbase import DirectObject
from panda3d.core import *

TO_RAD = 0.017453293
TO_DEG = 57.295779513


class RTSCameraControl(DirectObject.DirectObject):
    def __init__(self, game_engine):
        DirectObject.DirectObject.__init__(self)

        self.game_engine = game_engine
        game_engine.disableMouse()  # disable common mouse behavior

        self.camera = game_engine.camera
        self.mwn = game_engine.mouseWatcherNode
        self.target = NodePath('target')

        # u follows the line of sight
        self._left_arm = LVector3f(0, 0, 0)
        self._straight = LVector3f(0, 0, 0)

        # sliding
        self.slide_velocity = 5.0
        self._is_sliding = False

        # spinning
        self.spin_velocity = 50.0
        self._is_spinning = False

        # mouse
        self._mx = 0.0
        self._my = 0.0

        self.set_pos(LVector3f(10, 10, 10))
        self.look_at(LVector3f(0, 0, 0))

        self.game_engine.taskMgr.add(self.cam_move_task, 'cam_move_task')

    def spin(self, deg_angle=0.1):
        self.camera.wrt_reparent_to(self.target)  # Preserve absolute position
        self.target.set_h(self.target.get_h() + deg_angle)  # Rotates environ around pivot
        self.camera.wrt_reparent_to(self.game_engine.render)

        self._update_vectors()

    def _update_vectors(self):
        theta = TO_RAD * self.camera.get_h()
        self._left_arm = LVector3f(-num.cos(theta), -num.sin(theta), 0)
        self._straight = LVector3f(-num.sin(theta), num.cos(theta), 0)

    # def p(self):
    #     angle = self.camera.get_h()
    #     self.camera.wrt_reparent_to(self.target)  # Preserve absolute position
    #     self.target.set_h(-angle)
    #     self.target.set_p(self.target.get_p() + 1)  # Rotates environ around pivot
    #     self.target.set_h(0.0)
    #     self.camera.wrtReparentTo(self.base_object.render)
    #     # self.camera.set_h(angle)
    #
    #     print('p =', self.camera.get_p())

    def look_at(self, *pos):
        self.target.setPos(LVector3f(*pos))
        self.camera.lookAt(LVector3f(*pos))
        self._update_vectors()

    def set_pos(self, *pos):
        self.camera.setPos(LVector3f(*pos))

    def set_fov(self, fov):
        self.game_engine.camLens.setFov(fov)

    def axis_move(self, axis=0, vel=1):
        dis = self._straight * vel if axis == 0 else self._left_arm * vel
        self.target.set_pos(self.target.get_pos() + dis)
        self.camera.set_pos(self.camera.get_pos() + dis)

    def move(self, vel_axis_0, vel_axis_1):
        dis = self._straight * vel_axis_0 + self._left_arm * vel_axis_1
        self.target.set_pos(self.target.get_pos() + dis)
        self.camera.set_pos(self.camera.get_pos() + dis)

    def get_radius(self):
        return self.camera.get_pos(self.target).length()

    def set_radius(self, add=1):
        self.camera.set_pos(self.target, self.camera.get_pos(self.target) * (1 + add / self.get_radius()))

    # def _config_input(self):
    #     self.ignore_all()
    #
    #     self.accept('arrow_up', self.axis_move, extraArgs=[0, 0.05])
    #     self.accept('arrow_down', self.axis_move, extraArgs=[0, -.05])
    #     self.accept('arrow_right', self.axis_move, extraArgs=[1, -.05])
    #     self.accept('arrow_left', self.axis_move, extraArgs=[1, 0.05])
    #
    #     self.accept("wheel_up", self.set_radius, extraArgs=[-1])
    #     self.accept("wheel_down", self.set_radius, extraArgs=[1])
    #
    #     self.accept("mouse3", self.start_spin)
    #     self.accept("mouse3-up", self.stop_spin)
    #
    #     self.accept("mouse1", self.start_sliding)
    #     self.accept("mouse1-up", self.stop_sliding)

    def start_sliding(self):
        self._is_sliding = True
        if self.mwn.hasMouse():
            self._mx = self.mwn.getMouse().getX()
            self._my = self.mwn.getMouse().getY()

    def stop_sliding(self):
        self._is_sliding = False
        self._mx = 0.0
        self._my = 0.0

    def start_spin(self):
        self._is_spinning = True
        if self.mwn.hasMouse():
            self._mx = self.mwn.getMouse().getX()

    def stop_spin(self):
        self._is_spinning = False

    def cam_move_task(self, task):
        if self.mwn.hasMouse():
            mpos = self.mwn.getMouse()
            if self._is_spinning:
                self.spin(deg_angle=self.spin_velocity * (self._mx - mpos.getX()))
                self._mx = mpos.getX()
            if self._is_sliding:
                self.move(vel_axis_0=-self.slide_velocity * (mpos.getY() - self._my),
                          vel_axis_1=self.slide_velocity * (mpos.getX() - self._mx))
                self._mx = mpos.getX()
                self._my = mpos.getY()
        return task.cont
