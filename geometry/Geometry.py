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
        self._name = ""
        self.vao = None
        self.shader = Shader()
        self._type = None
        self.material = material if material else Material()
        self.model = model if model else Model()
        self._centroid = None

    def get_name(self):
        return self._name

    def get_type(self):
        return self._type

    def get_vertices(self):
        return self._vertices

    def get_normals(self):
        return self._normals

    def get_indices(self):
        return self._indicies

    def set_vertices(self, verts):
        self._vertices = verts

    def create_vao(self):
        self.vao = gl.glGenVertexArrays(1)

    def bind_vao(self):
        gl.glBindVertexArray(self.vao)

    def link_material(self):
        gl.glUniform3fv(gl.glGetUniformLocation(
            self.shader.program_id, "diffuseValue"), 1, self.material.diffuse.to_list())

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

        vertex_buffer = gl.glGenBuffers(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vertex_buffer)

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

        normal_buffer = gl.glGenBuffers(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, normal_buffer)

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

    def enable_vertex_attrib(self):
        gl.glEnableVertexAttribArray(
            self.vertex_attrib)  # use currently bound VAO
        gl.glEnableVertexAttribArray(self.normal_attrib)

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
        self.create_index_buffer()

    def bind(self):
        self.shader.bind()
        self.bind_index_buffer()
        self.enable_vertex_attrib()

    def rotate(self, vector, angle):
        self.model.rotate(vector, angle)

    def scale(self, scale_vec):
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
