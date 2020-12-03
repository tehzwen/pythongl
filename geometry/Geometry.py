from OpenGL import GL as gl
import ctypes
from shader.Shader import *
from material.Material import *
from model.Model import *


class Geometry:
    def __init__(self, material=None, model=None):
        self._vertices = []
        self._indicies = []
        self._normals = []
        self._texture_coords = []
        self._name = ""
        self._parent = None
        self._type = None
        self._centroid = None
        self.vao = None
        self.shader = Shader()
        self.material = material if material else Material()
        self.model = model if model else Model()
        self.vertex_attrib = None
        self.normal_attrib = None
        self.index_buffer = None
        self.vertex_buffer = None
        self.normal_buffer = None

    def get_parent(self):
        return self._parent

    def set_parent(self, parent_name):
        self._parent = parent_name

    def get_name(self):
        return self._name

    def get_type(self):
        return self._type

    def get_vertices(self):
        return self._vertices

    def get_normals(self):
        return self._normals

    def get_texture_coords(self):
        return self._texture_coords

    def get_indices(self):
        return self._indicies

    def set_vertices(self, verts):
        self._vertices = verts

    def create_vao(self):
        self.vao = gl.glGenVertexArrays(1)

    def bind_vao(self):
        gl.glBindVertexArray(self.vao)

    def set_diffuse_texture(self, filename):
        self.material.set_diffuse_texture("./res/materials/" + filename)

    def link_material(self):
        self.shader.link_vec3("material.ambient",
                              self.material.ambient.to_list(), 1)
        self.shader.link_vec3("material.diffuse",
                              self.material.diffuse.to_list(), 1)
        self.shader.link_vec3("material.specular",
                              self.material.specular.to_list(), 1)
        self.shader.link_float("material.alpha", self.material.alpha)
        self.shader.link_float("material.shininess", self.material.n)

        if (self.material.diffuseTexture):
            gl.glActiveTexture(gl.GL_TEXTURE0 + self.material.diffuseTexture)
            self.shader.link_int("diffuseSamplerExists", 1)
            self.shader.link_int(
                "diffuseSampler", self.material.diffuseTexture)
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.material.diffuseTexture)

    def link_model(self):
        model_matrix = glm.mat4()
        model_matrix = glm.translate(model_matrix, self.model.get_position())
        model_matrix = glm.translate(model_matrix, self.get_centroid())
        model_matrix *= self.model.get_rotation()
        model_matrix = glm.scale(model_matrix, self.model.get_scale())
        model_matrix = glm.translate(model_matrix, -(self.get_centroid()))

        gl.glUniformMatrix4fv(gl.glGetUniformLocation(
            self.shader.program_id, "modelMatrix"), 1, False, model_matrix.to_list())

        self.model.set_matrix(model_matrix)

    def create_vertex_buffer(self):
        if not self.vao:
            self.create_vao()
            self.bind_vao()

        attr_id = 0  # No particular reason for 0,
        # but must match the layout location in the shader.

        self.vertex_buffer = gl.glGenBuffers(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vertex_buffer)

        array_type = (gl.GLfloat * len(self.get_vertices()))
        gl.glBufferData(gl.GL_ARRAY_BUFFER,
                        len(self.get_vertices()) *
                        ctypes.sizeof(ctypes.c_float),
                        array_type(*self.get_vertices()),
                        gl.GL_STATIC_DRAW)

        gl.glVertexAttribPointer(
            attr_id,            # attribute 0.
            3,                  # components per vertex attribute
            gl.GL_FLOAT,        # type
            False,              # to be normalized?
            0,                  # stride
            None                # array buffer offset
        )
        self.vertex_attrib = attr_id

    def create_normal_buffer(self):
        attr_id = 1

        self.normal_buffer = gl.glGenBuffers(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.normal_buffer)

        array_type = (gl.GLfloat * len(self.get_normals()))
        gl.glBufferData(gl.GL_ARRAY_BUFFER,
                        len(self.get_normals()) *
                        ctypes.sizeof(ctypes.c_float),
                        array_type(*self.get_normals()),
                        gl.GL_STATIC_DRAW)

        gl.glVertexAttribPointer(
            attr_id,            # attribute 0.
            3,                  # components per vertex attribute
            gl.GL_FLOAT,        # type
            False,              # to be normalized?
            0,                  # stride
            None                # array buffer offset
        )

        self.normal_attrib = attr_id

    def create_texture_buffer(self):
        attr_id = 2

        self.texture_buffer = gl.glGenBuffers(1)
        array_type = (gl.GLfloat * len(self.get_texture_coords()))
        gl.glBufferData(gl.GL_ARRAY_BUFFER,
                        len(self.get_texture_coords()) *
                        ctypes.sizeof(ctypes.c_float),
                        array_type(*self.get_texture_coords()),
                        gl.GL_STATIC_DRAW)

        gl.glVertexAttribPointer(
            attr_id,            # attribute 0.
            2,                  # components per vertex attribute
            gl.GL_FLOAT,        # type
            False,              # to be normalized?
            0,                  # stride
            None                # array buffer offset
        )

        self.texture_attrib = attr_id

    def enable_vertex_attrib(self):
        gl.glEnableVertexAttribArray(
            self.vertex_attrib)  # use currently bound VAO
        gl.glEnableVertexAttribArray(self.normal_attrib)
        gl.glEnableVertexAttribArray(self.texture_attrib)

    def create_index_buffer(self):
        index_buffer = gl.glGenBuffers(1)

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, index_buffer)

        array_type = (gl.GLuint * len(self.get_indices()))

        gl.glBufferData(
            gl.GL_ELEMENT_ARRAY_BUFFER,
            len(self.get_indices()) *
            ctypes.sizeof(ctypes.c_uint),
            array_type(*self.get_indices()),
            gl.GL_STATIC_DRAW
        )

        self.index_buffer = index_buffer

    def bind_index_buffer(self):
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.index_buffer)

    def setup(self):
        self.calculate_centroid()
        self.create_vertex_buffer()
        self.create_normal_buffer()
        self.create_texture_buffer()
        self.create_index_buffer()

    def bind(self):
        self.bind_vao()
        self.enable_vertex_attrib()

    def rotate(self, vector, angle):
        self.model.rotate(vector, angle)

    def scale(self, scale_vec):
        # print(scale_vec)
        self.model.scale(scale_vec)

    def translate(self, trans_vec):
        self.model.translate(trans_vec)

    def calculate_centroid(self):
        center = glm.vec3()
        for i in range(0, len(self._vertices), 3):
            center += glm.vec3(self._vertices[i],
                               self._vertices[i + 1], self._vertices[i + 2])

        center *= 1/(len(self._vertices)/3)
        self._centroid = center

    def get_centroid(self):
        return self._centroid

    def set_centroid(self, center):
        self._centroid = center
