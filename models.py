from direct.showbase.ShowBase import Geom, GeomNode, GeomVertexData, GeomVertexFormat, GeomVertexWriter, GeomLines, NodePath
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import LVector3f, LVector4f, TextNode, TransparencyAttrib


class SkyDome:
    def __init__(self, engine):
        self.model = engine.render.attach_new_node(engine.loader.load_model('models/test.egg').node())
        # self.model.set_pos(engine.cam.get_pos())
        # self.model.reparent_to(engine.cam, sort=1, current_thread=None)
        self.model.set_pos(0, 0, 0)
        self.model.set_scale(20)

        self.model.set_depth_write(0)
        self.model.set_depth_test(0)
        # self.model.set_bin('fixed', -100)

    def set_color(self, color):
        self.model.set_color(color)

    def set_color_scale(self, color):
        self.model.set_color_scale(color)

    def set_luminosity(self, l):
        self.model.set_color_scale((l, l, l, 1.0))


class Grid(GeomNode):
    def __init__(self, x_extend=None, y_extend=None, x_size=1, y_size=1, z=-0.01, tickness=2., name='Grid',
                 x_color=None,
                 y_color=None):
        GeomNode.__init__(self, name)
        if x_color is None:
            x_color = LVector4f(1.0, 1.0, 1.0, 1.0)

        if y_color is None:
            y_color = LVector4f(1.0, 1.0, 1.0, 1.0)

        if x_extend is None:
            x_extend = [0, 10]
        if y_extend is None:
            y_extend = [0, 10]

        self.vertexData = GeomVertexData("Chunk", GeomVertexFormat.getV3c4(), Geom.UHStatic)
        self.vertex = GeomVertexWriter(self.vertexData, 'vertex')
        self.color = GeomVertexWriter(self.vertexData, 'color')

        self.mesh = Geom(self.vertexData)
        self.lines = GeomLines(Geom.UHStatic)

        nb_lines_x = int((x_extend[1] - x_extend[0]) / x_size)
        nb_lines_y = int((y_extend[1] - y_extend[0]) / y_size)

        vertex_nb = 0
        for ix in range(nb_lines_x):
            for iy in range(nb_lines_y):
                x = x_extend[0] + ix * x_size
                y = y_extend[0] + iy * y_size

                self.vertex.addData3f(x, y, z)
                self.color.addData4f(x_color)

                self.vertex.addData3f(x + x_size, y, z)
                self.color.addData4f(x_color)

                self.vertex.addData3f(x, y, z)
                self.color.addData4f(y_color)

                self.vertex.addData3f(x, y + y_size, z)
                self.color.addData4f(y_color)

                self.lines.add_vertices(vertex_nb, vertex_nb + 1, vertex_nb + 2, vertex_nb + 3)
                vertex_nb += 4

        self.lines.closePrimitive()
        self.mesh.addPrimitive(self.lines)
        self.addGeom(self.mesh)

        NodePath(self).setRenderModeThickness(tickness)
        NodePath(self).setLightOff()
        NodePath(self).setColorOff()
        NodePath(self).setTransparency(TransparencyAttrib.MAlpha)
        # NodePath(self).set_bin('fixed', 8)


class DevEnv:
    def __init__(self, engine):
        self.basis = CartesianBasis(tickness=5, shade=0.3)
        engine.render.attachNewNode(self.basis)

        for n, p in zip(['x', 'y', 'z'], [LVector3f(1, 0, 0), LVector3f(0, 1, 0), LVector3f(0, 0, 1)]):
            text = TextNode(n)
            text.set_text(n)
            np = engine.render.attachNewNode(text)
            np.set_scale(0.4)
            np.set_color(LVector4f(p, 1) + LVector4f(0.2, 0.2, 0.2, 1))
            np.setPos(p * 1.5)
            np.setBillboardPointEye()

        self.grid = Grid(x_extend=[-10, 10], y_extend=[-10, 10], x_color=(0.4, .4, 0.3, 0.5), y_color=(0.4, .4, 0.3, 0.5), tickness=3)
        engine.render.attach_new_node(self.grid)

        self.dome = SkyDome(engine)


class CartesianBasis(GeomNode):
    def __init__(self, length=1., tickness=3., shade=0.2):
        GeomNode.__init__(self, "Basis")
        self.vertexData = GeomVertexData("Basis", GeomVertexFormat.getV3c4(), Geom.UHStatic)
        self.vertex = GeomVertexWriter(self.vertexData, 'vertex')
        self.color = GeomVertexWriter(self.vertexData, 'color')
        self.mesh = Geom(self.vertexData)
        self.lines = GeomLines(Geom.UHStatic)

        self.vertex.addData3f(0.0, 0.0, 0.0)
        self.color.addData4f(1.0, shade, shade, 1.0)
        self.vertex.addData3f(length, 0.0, 0.0)
        self.color.addData4f(1.0, shade, shade, 1.0)
        self.lines.add_vertices(0, 1)

        self.vertex.addData3f(0.0, 0.0, 0.0)
        self.color.addData4f(shade, 1.0, shade, 1.0)
        self.vertex.addData3f(0.0, length, 0.0)
        self.color.addData4f(shade, 1.0, shade, 1.0)
        self.lines.add_vertices(2, 3)

        self.vertex.addData3f(0.0, 0.0, 0.0)
        self.color.addData4f(shade, shade, 1.0, 1.0)
        self.vertex.addData3f(0.0, 0.0, length)
        self.color.addData4f(shade, shade, 1.0, 1.0)
        self.lines.add_vertices(4, 5)

        self.lines.closePrimitive()
        self.mesh.addPrimitive(self.lines)
        self.addGeom(self.mesh)

        NodePath(self).setRenderModeThickness(tickness)
        NodePath(self).setLightOff()
        NodePath(self).setColorOff()
        # NodePath(self).set_bin('fixed', 9)
