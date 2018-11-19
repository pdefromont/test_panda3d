from direct.showbase import DirectObject


class InputManager(DirectObject.DirectObject):
    # modes
    FREE_CAMERA = 0
    BUILD = 1

    def __init__(self, main_engine):
        super(InputManager, self).__init__()
        self.engine = main_engine
        self.cam_controls = self.engine.cam_control

    def set_mode(self, mode):
        if mode == InputManager.FREE_CAMERA:
            self.ignore_all()

            self.accept('arrow_up', self.cam_controls.axis_move, extraArgs=[0, 0.05])
            self.accept('arrow_down', self.cam_controls.axis_move, extraArgs=[0, -.05])
            self.accept('arrow_right', self.cam_controls.axis_move, extraArgs=[1, -.05])
            self.accept('arrow_left', self.cam_controls.axis_move, extraArgs=[1, 0.05])

            self.accept("wheel_up", self.cam_controls.set_radius, extraArgs=[-1])
            self.accept("wheel_down", self.cam_controls.set_radius, extraArgs=[1])

            self.accept("mouse3", self.cam_controls.start_spin)
            self.accept("mouse3-up", self.cam_controls.stop_spin)

            self.accept("mouse1", self.cam_controls.start_sliding)
            self.accept("mouse1-up", self.cam_controls.stop_sliding)
