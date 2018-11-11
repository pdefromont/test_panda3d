from direct.showbase.ShowBase import ShowBase, ClockObject, AntialiasAttrib, TransparencyAttrib, NodePath
from Picker import Picker
from camera import RTSCameraControl
from models import CartesianBasis, Grid, DevEnv
from utils import hex_to_normalized_rgb


class Game(ShowBase):
    """
    The main class of the game. Reads configuration from the params.ini file.
    """
    def __init__(self):
        ShowBase.__init__(self)
        self.clock = ClockObject()

        self.env = DevEnv(self)
        self.cam_control = RTSCameraControl(self)
        self.cam_control.look_at(0, 0, 0)
        self.cam_control.set_fov(80)

        self.picker = Picker(self, self.select, self.unselect)

        self.model = self.render.attach_new_node(self.loader.load_model("models/sphere.bam").node())
        self.model.set_color(0.5, 0.7, 0.6, 0.5)
        self.model.setTransparency(TransparencyAttrib.MAlpha)
        self.model.set_pos(2, 0, 0)
        self.picker.make_pickable(self.model)

        for j in range(-100, 100):
            a = self.render.attach_new_node(self.loader.load_model("models/wall_straight_new.egg").node())
            a.set_pos(0, j, 0)
            if j == 4:
                a.set_texture(self.loader.load_texture('models/tex/test.png'), 1)

        self.setBackgroundColor(hex_to_normalized_rgb('#99ffcc'))
        self.render.setShaderAuto()
        self.setFrameRateMeter(True)
        self.render.setAntialias(AntialiasAttrib.MAuto)

    def select(self, event_name, obj, pos=None, norm=None):
        if obj is not None:
            obj.set_color_scale(1.2, 1.2, 1.2, 1.0)

    def unselect(self, obj, **kwargs):
        if obj is not None:
            obj.set_color_scale(1.0, 1.0, 1.0, 1.0)

    def get_time(self):
        return self.clock.get_real_time()


g = Game()
g.run()
