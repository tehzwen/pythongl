import glm
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

    def render_geometry(self, geo, lights):
        geo.shader.bind()
        geo.bind()
        geo.link_material()
        geo.link_model()
        self.set_shader(geo.shader)
        self.link_matrices(geo.model.get_matrix())
        self.render_lights(lights)
        gl.glDrawElements(gl.GL_TRIANGLE_STRIP, len(
                    geo.get_indices()), gl.GL_UNSIGNED_INT, None)
    
    def render_mesh(self, mesh, lights):
        for child in mesh.get_children():
            self.set_shader(child.shader)
            child.shader.bind()
            child.bind()
            child.link_material()
            child.link_model()
            self.link_matrices(child.model.get_matrix())
            self.render_lights(lights)
            gl.glDrawElements(gl.GL_TRIANGLES, len(
                child.get_indices()), gl.GL_UNSIGNED_INT, None)

    def link_matrices(self, model_matrix):
        self._shader.link_mat4(
            "projectionMatrix", self._projection_matrix.to_list())
        self._shader.link_mat4("viewMatrix", self._view_matrix.to_list())
        self._normal_matrix = model_matrix
        self._normal_matrix = glm.transpose(self._normal_matrix)
        self._shader.link_mat4("normalMatrix", self._normal_matrix.to_list())

    def render_lights(self, lights):
        count = 0
        for key, light in sorted(lights.items()):
            self._shader.link_vec3(
                "pointLights[" + str(count) + "].position", light.get_position().to_list(), 1)
            self._shader.link_vec3(
                "pointLights[" + str(count) + "].color", light.get_color().to_list(), 1)
            self._shader.link_float(
                "pointLights[" + str(count) + "].strength", light.get_strength())
            count += 1

        self._shader.link_int("numPointLights", count)
