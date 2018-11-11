from direct.gui.DirectButton import DirectButton, LVector3f, DirectFrame, TextNode
from direct.gui.DirectCheckButton import DirectCheckButton
from direct.gui.DirectGuiGlobals import FLAT, SUNKEN, RAISED, RIDGE, GROOVE
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectScrolledFrame import DirectScrolledFrame
from panda3d.core import LVector4f, LVector2f, LVector3i

from GUIobjects import TextFrame, CheckButton, GUIparams, ColorPicker, Button, ImageButton, DGG
from VoxelEngine import Voxel, VoxelWorld, VoxelNode
from utils import normalized_rgb_to_hex


class GameGui:
    def __init__(self, world):
        self._gui_params = GUIparams(world)
        # self._text_params = GUItext()
        self._world = world

        self.text_frame = TextFrame(pos=LVector3f(-1.34, 0.0, 0.1), params=self._gui_params)
        # self.object_pres = BasicObjectRepresentation(pos=LVector3f(-1.33, 0, -1))

        # DirectButton(**self._gui_params(), text="change mode", command=self)
        cb = CheckButton(1., 0.9, text='use keyboard', command=self.use_keyboard, params=self._gui_params)
        bb = CheckButton(1., 0.7, text='set build mode', command=self.set_build_mode, params=self._gui_params)
        b = Button(0.0,  0.0, object=self, text='cliquez ici')
        # b.disable()
        # b1 = Button(LVector3f(1., 0, 0.6), text='colored', style=Button.COLORED)
        # b2 = Button(LVector3f(1., 0, 0.5), text='gray', style=Button.GREY)

        self.click = self._world.loader.load_sfx('data/sound/gui/click1.mp3')

    def click_sound(self):
        self.click.play()

    def write(self, text):
        self.text_frame.add_text(text)

    def select(self, obj):
        # self.object_pres.show_object(obj)
        pass

    def use_keyboard(self, use):
        self.click_sound()
        if use:
            self._world.rts_camera.use_keyboard()
            self.write('using keyboard')
        else:
            self._world.rts_camera.use_mousse()
            self.write('using mouse')

    def set_build_mode(self, use):
        self.click_sound()
        if use:
            self._world.voxel_world.set_mode(VoxelWorld.EDIT_MODE)
            self.write('setting mode to : build')
        else:
            self._world.voxel_world.set_mode(VoxelWorld.SELECT_MODE)
            self.write('setting mode to : select')


class ItemBuilderGui:
    ADD_MODE = 0
    DELETE_MODE = 1
    PICK_MODE = 2

    def __init__(self, world):
        self._gui_params = GUIparams(world)
        self._world = world

        self.text_frame = TextFrame(pos=LVector3f(-1.34, 0.0, 0.1), params=self._gui_params)

        font = self._world.loader.loadFont('data/gui/fonts/vag.ttf')

        self.color_picker = ColorPicker(self._world,
                                        self.select_color,
                                        pos=(- .95, 0., -0.55),
                                        scale=(.4, 1., .4),
                                        text_font=font,
                                        params=self._gui_params)

        cb = CheckButton(1., 0.9, text='use keyboard', command=self.use_keyboard, params=self._gui_params)
        rest = Button(.9, 0.7, text='reset', command=self.reset, params=self._gui_params)
        self.edit_button = ImageButton(x=1., z=0.5, params=self._gui_params, image='data/gui/pencil.png',
                                  command=self.set_mode, extraArgs=(self.ADD_MODE,))
        self.delete_button = ImageButton(x=1., z=0.3, params=self._gui_params, image='data/gui/rubber.png',
                                    command=self.set_mode, extraArgs=(self.DELETE_MODE,))
        self.picker_button = ImageButton(x=1., z=0.1, params=self._gui_params, image='data/gui/color_picker.png',
                                    command=self.set_mode, extraArgs=(self.PICK_MODE,))

        self.set_mode(self.ADD_MODE)

    def manage_event_return(self, retour):
        if isinstance(retour, str):
            self.write(retour)
        elif isinstance(retour, Voxel):
            self._world.item.set_current_voxel_type(normalized_rgb_to_hex(retour.color))

    def set_mode(self, mode):
        if mode == self.ADD_MODE:
            self._world.item.event_mode = VoxelNode.ADD_ONLY_MODE
            self.edit_button.enable()
            self.delete_button.disable()
            self.picker_button.disable()
        elif mode == self.DELETE_MODE:
            self._world.item.event_mode = VoxelNode.REMOVE_ONLY_MODE
            self.delete_button.enable()
            self.edit_button.disable()
            self.picker_button.disable()
        elif mode == self.PICK_MODE:
            self._world.item.event_mode = VoxelNode.PICK_ONLY_MODE
            self.picker_button.enable()
            self.delete_button.disable()
            self.edit_button.disable()

    def write(self, text):
        self.text_frame.add_text(text)

    def reset(self):
        self.write('clear mesh')
        self._world.item.clear_all()
        self._world.item.add_voxel(LVector3i(0, 0, 0), cube_name='#ffffff')

    def select_color(self, id=None):
        color = self.color_picker.get_selected_color()
        self.write(normalized_rgb_to_hex(color))
        self._world.item.set_current_voxel_type(normalized_rgb_to_hex(color))

    def use_keyboard(self, use):
        if use:
            self._world.rts_camera.use_keyboard()
            self.write('using keyboard')
        else:
            self._world.rts_camera.use_mousse()
            self.write('using mouse')
