import glm
import ctypes
from OpenGL import GL as gl


class Renderer():
    def __init__(self, shader=None):
        self._shader = shader
        self._projection_matrix = glm.mat4()
        self._view_matrix = glm.mat4()
        self._normal_matrix = glm.mat4()

    def get_shader(self):
        return self._shader

    def set_shader(self, shader):
        self._shader = shader

    def get_projection_matrix(self):
        return self._projection_matrix

    def set_projection_matrix(self, mat):
        self._projection_matrix = mat

    def get_view_matrix(self):
        return self._view_matrix

    def set_view_matrix(self, mat):
        self._view_matrix = mat

    def render_geometry(self, geo, sm):
        # gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE); # enables wireframe
        lights = sm.get_point_lights()
        geo.shader.bind()
        geo.bind()
        geo.link_material()
        geo.link_model()
        self.set_shader(geo.shader)
        self.link_matrices(geo.model.get_matrix())
        self.render_point_lights(lights)
        self.link_camera(sm.get_active_camera())
        gl.glDrawElements(gl.GL_TRIANGLES, len(
            geo.get_indices()), gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))
        geo.unbind_vao()

    def render_mesh(self, mesh, sm):
        lights = sm.get_point_lights()
        for child in mesh.get_children():
            self.set_shader(child.shader)
            child.shader.bind()
            child.bind()
            child.link_material()
            child.link_model()
            self.link_matrices(child.model.get_matrix())
            self.render_point_lights(lights)
            self.link_camera(sm.get_active_camera())
            gl.glDrawElements(gl.GL_TRIANGLES, len(
                child.get_indices()), gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))
            child.unbind_vao()

    def link_matrices(self, model_matrix):
        self._shader.link_mat4(
            "projectionMatrix", self._projection_matrix.to_list())
        self._shader.link_mat4("viewMatrix", self._view_matrix.to_list())
        self._normal_matrix = model_matrix
        self._normal_matrix = glm.transpose(self._normal_matrix)
        self._shader.link_mat4("normalMatrix", self._normal_matrix.to_list())

    def link_camera(self, camera):
        self._shader.link_vec3("cameraPosition", camera.get_position().to_list(), 1)

    def render_point_lights(self, lights):
        count = 0
        for key, light in sorted(lights.items()):
            self._shader.link_vec3(
                "pointLights[" + str(count) + "].position", light.get_position().to_list(), 1)
            self._shader.link_vec3(
                "pointLights[" + str(count) + "].color", light.get_color().to_list(), 1)
            self._shader.link_float(
                "pointLights[" + str(count) + "].strength", light.get_strength())
            self._shader.link_float(
                "pointLights[" + str(count) + "].linear", light.get_linear())
            self._shader.link_float(
                "pointLights[" + str(count) + "].quadratic", light.get_quadratic())
            count += 1

        self._shader.link_int("numPointLights", count)
