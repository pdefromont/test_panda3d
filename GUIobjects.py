from direct.gui.DirectGuiGlobals import FLAT, RAISED
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import *

from VoxelEngine import Voxel


class GUIparams:
    def __init__(self, base_object, font='vag'):
        # for frame
        self.frameColor = LVector4f(0.13, 0.13, 0.13, 1.0)
        self.borderWidth = LVector2f(0.15, 0.15)
        self.pad = LVector2f(0.5, 0.5)
        # self.test_scale = 0.06
        self.scale = 0.06

        # for text
        self.text_font = base_object.loader.loadFont('data/gui/fonts/' + font + '.ttf')
        self.text_font.set_bg((0, 0, 0, 0))
        self.text_font.set_outline((0, 0, 0, 0.8), 2, 0.5)
        self.text_fg = LVector4f(1., 1., 1.0, 1.0)
        self.text_shadow = LVector4f(0.0, 0.0, 0.0, 0.5)
        # self.text_scale = 0.045

    def text_params(self):
        r = dict()
        for e in self.__dict__:
            if 'text' in e:
                r[e] = self.__dict__[e]
        return r

    def __call__(self):
        return self.__dict__


class TextFrame(DirectScrolledFrame):
    def __init__(self, pos, params, size_x=0.9, size_y=0.9):
        DirectScrolledFrame.__init__(self,
                                     pos=pos,
                                     frameSize=LVector4f(0.0, size_x, 0.0, size_y),
                                     canvasSize=LVector4f(0.0, size_x - 0.05, 0.0, 0.0),
                                     frameColor=LVector4f(0.0, 0.0, 0.0, 0.2),
                                     scrollBarWidth=0.03,
                                     # verticalScroll_relief=None,
                                     verticalScroll_frameColor=LVector4f(0.0, 0.0, 0.0, 0.2),
                                     verticalScroll_thumb_frameColor=LVector4f(0.5, 0.5, 0.5, 0.8),
                                     verticalScroll_thumb_relief=FLAT,
                                     verticalScroll_incButton_frameColor=LVector4f(1.0, 1.0, 1.0, 0.8),
                                     verticalScroll_incButton_relief=FLAT,
                                     verticalScroll_decButton_frameColor=LVector4f(1.0, 1.0, 1.0, 0.8),
                                     verticalScroll_decButton_relief=FLAT,
                                     horizontalScroll_frameColor=LVector4f(0.0, 0.0, 0.0, 0.2),
                                     horizontalScroll_thumb_frameColor=LVector4f(0.5, 0.5, 0.5, 0.8),
                                     horizontalScroll_thumb_relief=FLAT,
                                     horizontalScroll_incButton_frameColor=LVector4f(1.0, 1.0, 1.0, 0.8),
                                     horizontalScroll_incButton_relief=FLAT,
                                     horizontalScroll_decButton_frameColor=LVector4f(1.0, 1.0, 1.0, 0.8),
                                     horizontalScroll_decButton_relief=FLAT
                                     )
        self.initialiseoptions(TextFrame)
        self.text_scale = 0.05
        self.params = params
        self.text = []
        self.text_height = 0

        # self.add_text('')

    def _cw(self):
        return self['canvasSize'].y

    def _ch(self):
        return self['canvasSize'].w

    def add_text(self, text):
        self.text.append(DirectLabel(
                                     parent=self.getCanvas(),
                                     pos=LVector3f(0.02, 0.0, self._ch()),
                                     text=text,
                                     **self.params.text_params(),
                                     text_align=TextNode.A_left,
                                     text_scale=self.text_scale,
                                     frameColor=LVector4f(0.0, 0.0, 0.0, 0.)
                                     ))
        # correcting the shadow
        self['text_shadow'] = LVector4f(0., 0., 0., 0.4)

        new_width = self.text[-1].getWidth()
        if new_width > self._cw():
            self['canvasSize'].y = new_width

        self.text_height += self.text[-1].getHeight()
        if self.text_height > self._ch():
            self['canvasSize'].w = self.text_height

        self.initialiseoptions(TextFrame)


class CheckButton(DirectCheckButton):
    def __init__(self, x, z, text, command, params, **kwargs):
        self.params = params
        DirectCheckButton.__init__(self, **self.params(),
                                   text=text,
                                   command=command,
                                   pos=LVector3f(x, 0, z),
                                   boxRelief=None,
                                   boxBorder=0.,
                                   boxImage=("data/gui/disable.png", "data/gui/enable.png", None),
                                   boxImageScale=0.7,
                                   relief=RAISED,
                                   pressEffect=0,
                                   **kwargs
                                   )
        # print('left corner ?', pos - LVector3f(self['width']/2, 0, self['height']/2))
        self.initialiseoptions(CheckButton)


class ImageButton(DirectButton):
    def __init__(self, x, z, params, image, command=None, **kwargs):
        DirectButton.__init__(self,
                              **params(),
                              text='',
                              command=command,
                              pos=LVector3f(x, 0, z),
                              relief=RAISED,
                              pressEffect=0,
                              image=image,
                              **kwargs
                              )

        self.setTransparency(TransparencyAttrib.MAlpha)
        self.initialiseoptions(ImageButton)

    def enable(self):
        self['image_color'] = LVector4f(1.0, 1.0, 1.0, 1.0)

    def disable(self):
        self['image_color'] = LVector4f(1.0, 1.0, 1.0, 0.2)


class Button(DirectButton):
    DEFAULT = 0
    COLORED = 1
    GREY = 2

    def __init__(self, x, z, object, text='', command=None, style=0, **kwargs):
        self._gui_params = object._gui_params
        maps = object._world.loader.loadModel('data/gui/button/button_maps.egg')
        DirectButton.__init__(self,
                              # image='data/gui/button/up.png',
                              # image=(maps.find('**/up'),
                              #       maps.find('**/down'),
                              #       maps.find('**/down'),
                              #       maps.find('**/disabled')),
                              # **self._gui_params(),
                              text=text,
                              text_scale=0.06,
                              command=command,
                              # command=lambda: print("youy"),
                              pos=LVector3f(x, 0, z),
                              relief=None,
                              # relief=RAISED,
                              # pressEffect=0,
                              **kwargs
                              )
        if style == self.COLORED:
            self['frameColor'] = LVector4f(0.25, 0.53, 0.13, 1.)
            self['text_shadow'] = LVector4f(0., 0., 0., 1.)
        elif style == self.GREY:
            self['frameColor'] = LVector4f(0.27, 0.27, 0.27, 1.)
            self['text_shadow'] = LVector4f(0., 0., 0., 1.)

        # compute bounds
        self.initialiseoptions(Button)
        bounds = self.bounds
        center = (0.5 * (bounds[1] + bounds[0]),
                  1.0,
                  0.5 * (bounds[3] + bounds[2]))
        size = (bounds[1] - bounds[0],
                1.0,
                bounds[3] - bounds[2])
        X = object._world.win.getXSize()
        Y = object._world.win.getYSize()
        # need aspect ratio ?
        scale = (size[0] * 0.5 * X / 240,
                 1.0,
                 size[2] * 0.5 * Y / 240,)

        # setting images
        images = [maps.find('**/up'),
                  maps.find('**/down'),
                  maps.find('**/down'),
                  maps.find('**/disabled')
                  ]
        for im in images:
            im.set_pos(center)
            im.set_texture_scale(scale)

        # self["image_pos"] = LPoint3f(0.5, 1.0, 0.5)
        self["image"] = tuple(images)
        self.setImage()
        # self["image_scale"] = (3.0, 1.0, 0.2)

        self.resetFrameSize()
        self.initialiseoptions(Button)
        # self.frameInitialiseFunc()
        # self.resetFrameSize()

        print(self.bounds, self.getCenter(), self['image_pos'])

    def disable(self):
        self["state"] = DGG.DISABLED
        self.initialiseoptions(Button)

    def enable(self):
        self["state"] = DGG.ACCEPT
        self.initialiseoptions(Button)


#
# class GUItext:
#     def __init__(self):
#         self.frameColor = LVector4f(0.0, 0.0, 0.0, 0.0)
#         self.borderWidth = LVector2f(0.05, 0.05)
#         self.pad = LVector2f(0.2, 0.2)
#         self.text_fg = LVector4f(1.0, 1.0, 1.0, 1.0)
#         self.text_bg = LVector4f(1.0, 1.0, 1.0, 0.0)
#         self.scale = 0.045
#
#     def __call__(self):
#         return self.__dict__


class ColorSpectrum(object):

    def __init__(self, app, click_handler, **kwargs):

        self._app = app
        self._frame = DirectFrame(**kwargs)
        self._marker = DirectFrame(parent=self._frame,
                                   frameColor=(0., 0., 0., 1.),
                                   frameSize=(-.06, .06, -.06, .06),
                                   pos=(-.89, 0., -.89))
        self._marker_center = DirectFrame(parent=self._marker,
                                          frameColor=(.5, .5, .5, 1.),
                                          frameSize=(-.02, .02, -.02, .02))

        texture_filename = self._frame['image']
        self._palette_img = img = PNMImage(Filename.fromOsSpecific(texture_filename))
        width = img.getReadXSize()
        height = img.getReadYSize()
        self._palette_size = (width, height)
        self._frame['state'] = DGG.NORMAL
        self._frame.bind(DGG.B1PRESS, command=click_handler)

    def getColorUnderMouse(self, update_marker=False):

        if not self._app.mouseWatcherNode.hasMouse():
            return

        x, y = self._app.mouseWatcherNode.getMouse()
        win_w, win_h = self._app.win.getSize()
        width, height = self._palette_size

        if win_w < win_h:
            y *= 1. * win_h / win_w
        else:
            x *= 1. * win_w / win_h

        screen = self._app.aspect2d
        x -= self._frame.getX(screen)
        y -= self._frame.getZ(screen)
        img_scale = self._frame['image_scale']
        sx = self._frame.getSx(screen) * img_scale[0]
        sy = self._frame.getSz(screen) * img_scale[2]
        marker_x = max(-.89, min(.89, x / sx))
        marker_y = max(-.89, min(.89, y / sy))
        x = (.5 + x / (2. * sx)) * width
        y = (.5 + y / -(2. * sy)) * height

        if 0 <= x < width and 0 <= y < height:

            r, g, b = color = self._palette_img.getXel(int(x), int(y))

            if update_marker:
                self._marker_center['frameColor'] = (r, g, b, 1.)
                self._marker.setPos(marker_x, 0., marker_y)

            return color

    def setMarkerCoord(self, coord):

        x, y = coord
        marker_x = max(-.89, min(.89, x))
        marker_y = max(-.89, min(.89, y))
        self._marker.setPos(marker_x, 0., marker_y)

    def getMarkerCoord(self):

        marker_x, y, marker_y = self._marker.getPos()

        return (marker_x, marker_y)

    def setMarkerColor(self, color):

        r, g, b = color
        self._marker_center['frameColor'] = (r, g, b, 1.)


class ColorSwatch(object):
    def __init__(self, parent, color=None):
        self._frame = DirectFrame(parent=parent,
                                  relief=DGG.SUNKEN,
                                  borderWidth=(.05, .05),
                                  frameColor=(.3, .3, .3, 1.),
                                  frameSize=(-.4, .4, -.3, .3),
                                  scale=(.5, 1., .5))
        self._swatch = DirectFrame(parent=self._frame,
                                   frameColor=color if color else (.5, .5, .5, 1.),
                                   frameSize=(-.35, .35, -.25, .25))
        self._color = color

    def setColor(self, color=None):
        self._swatch['frameColor'] = color if color else (.5, .5, .5, 1.)
        self._color = color

    def getColor(self):
        return self._color

    def setPos(self, *pos):
        self._frame.setPos(*pos)


class ColorData(object):

    def __init__(self, color=None, brightness=None, spectrum_coord=None):

        self._color = color if color else Vec3(.5, .5, .5)
        self._brightness = .5 if brightness is None else brightness
        self._coord = spectrum_coord if spectrum_coord else (-1., -1.)

    def copy(self):

        color_data = ColorData(self._color, self._brightness, self._coord)

        return color_data

    def setColor(self, color):

        self._color = color

    def getColor(self):

        return self._color

    def setBrightness(self, brightness):

        self._brightness = brightness

    def getBrightness(self):

        return self._brightness

    def getColorShade(self):

        if self._brightness < .5:
            color = self._color
        else:
            color = Vec3(1., 1., 1.) - self._color

        color = color * 2. * (self._brightness - .5)
        color += self._color
        r, g, b = color

        return VBase4(r, g, b, 1.)

    def setCoord(self, coord):

        self._coord = coord

    def getCoord(self):

        return self._coord


class ColorPicker:

    def __init__(self, app, picker_command, params, **kwargs):
        if 'frameSize' not in kwargs:
            kwargs['frameSize'] = (-.8, .8, -1., 1.)

        self._gui_params = params
        self._app = app
        self._frame = DirectFrame(**kwargs,
                                  frameColor=self._gui_params.frameColor)

        spectrum_filename = 'data/gui/color_spectrum.png'
        self._spectrum = ColorSpectrum(app,
                                       self.__handle_color_selection,
                                       parent=self._frame,
                                       relief=DGG.SUNKEN,
                                       borderWidth=(.05, .05),
                                       # **self._gui_params(),
                                       image=spectrum_filename,
                                       image_scale=(.95, 1., .95),
                                       frameColor=self._gui_params.frameColor,
                                       frameSize=(-1., 1., -1., 1.0),
                                       pos=(-.15, 0., .3),
                                       scale=(.5, 1., .5),
                                       )
        self._selected_color = ColorData()
        self._spectrum.setMarkerCoord(self._selected_color.getCoord())
        self._spectrum.setMarkerColor(self._selected_color.getColor())

        def update_brightness():
            self._selected_color.setBrightness(self._slider['value'])
            self._swatch_selected.setColor(self._selected_color.getColorShade())

        brightness_filename = 'data/gui/brightness.png'
        brightness = self._selected_color.getBrightness()
        self._slider = DirectSlider(parent=self._frame,
                                    orientation=DGG.VERTICAL,
                                    relief=None,
                                    borderWidth=(.05, .05),
                                    image=brightness_filename,
                                    image_scale=(.05, 1., .95),
                                    frameColor=(.3, .3, .3, 1.),
                                    frameSize=(-.4, .4, -1., 1.),
                                    thumb_frameSize=(-.2, .2, -.1, .1),
                                    command=update_brightness,
                                    value=brightness,
                                    pos=(.55, 0., .3),
                                    scale=(.5, 1., .5))

        self._swatch_selected = ColorSwatch(self._frame)
        self._swatch_selected.setPos(-.45, 0., -.4)
        self._swatch_current = ColorSwatch(self._frame)
        self._swatch_current.setPos(.15, 0., -.4)

        self._task = app.taskMgr.add(self.__show_color_under_mouse, 'show_color')
        self._drag_start = Point2()  # used when dragging the color picker frame
        self._drag_offset = Vec2()  # used when dragging the color picker frame

        def on_ok():
            # self.destroy()
            picker_command(self._selected_color)

        self._btn_ok = DirectButton(parent=self._frame,
                                    borderWidth=(.02, .02),
                                    frameSize=(-.6, .6, -.15, .15),
                                    command=on_ok,
                                    text='select color',
                                    frameColor=LVector4f(0.25, 0.53, 0.13, 1.),
                                    text_fg=self._gui_params.text_fg,
                                    text_shadow=LVector4f(0., 0., 0., 1.),
                                    text_pos=(0., -.03),
                                    text_scale=(.12, .12),
                                    text_font=kwargs['text_font'] if 'text_font' in kwargs else None,
                                    pos=(-.1, 0., -.75))

    def get_selected_color(self):
        return self._selected_color.getColorShade()

    def __handle_color_selection(self, *args):

        color = self._spectrum.getColorUnderMouse(update_marker=True)

        if color:
            coord = self._spectrum.getMarkerCoord()
            self._selected_color.setCoord(coord)
            self._selected_color.setColor(color)
            self._swatch_selected.setColor(self._selected_color.getColorShade())

    def __show_color_under_mouse(self, task):

        color = self._spectrum.getColorUnderMouse()

        if color:
            r, g, b = color
            self._swatch_current.setColor(VBase4(r, g, b, 1.))

        return task.cont






#
# class BasicObjectRepresentation(DirectFrame):
#     def __init__(self, pos):
#         DirectFrame.__init__(self,
#                              pos=pos,
#                              frameSize=LVector4f(0., 0.5, 0, 0.5),
#                              frameColor=LVector4f(0.13, 0.13, 0.13, 1.))
#         self.initialiseoptions(BasicObjectRepresentation)
#
#         self._text_params = GUItext()
#         self.text = DirectLabel(**self._text_params(),
#                                 parent=self,
#                                 text='nothing to display',
#                                 text_align=TextNode.A_left,
#                                 textMayChange=1)
#
#     def show_object(self, obj):
#         if isinstance(obj, Voxel):
#             text = 'voxel of : ' + obj.name + \
#                    '\nlocated in ' + str(obj.relative_pos) + \
#                    '\nin structure : ' + str(obj.structure is not None)
#             self.text['text'] = text
#         else:
#             can_be_shown = getattr(obj, "__str__", None)
#             if callable(can_be_shown):
#                 self.text['text'] = obj.__str__()
#             else:
#                 self.text['text'] = 'nothing to display'