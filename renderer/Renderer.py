from geometry.Geometry import Geometry
import glm
from OpenGL.GL import *
from lighting.Light import *
from lighting.AreaLight import CircularAreaLight
from geometry.Quad import *


class Renderer():
    def __init__(self, shader=None):
        self._shader = shader
        self._projection_matrix = glm.mat4()
        self._view_matrix = glm.mat4()
        self._normal_matrix = glm.mat4()
        self._hdr_buffer = None
        self._render_quad = None
        self._hdr_texture = None

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

    def setup_hdr_buffer(self, sm):

        # create a render quad for hdr
        self._render_quad = RenderQuad("myRenderQuad")
        self._render_quad.shader.load_frag_source(file_name="renderQuad")
        self._render_quad.shader.load_vert_source(file_name="renderQuad")
        self._render_quad.shader.init()
        self._render_quad.setup()

        self._hdr_buffer = glGenFramebuffers(1)
        # create floating point color buffer
        self._hdr_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self._hdr_texture)
        screen_width, screen_height = sm.get_dimensions()
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA16F, screen_width,
                     screen_height, 0, GL_RGBA, GL_FLOAT, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        rbo_depth = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, rbo_depth)
        glRenderbufferStorage(
            GL_RENDERBUFFER, GL_DEPTH_COMPONENT, screen_width, screen_height)

        glBindFramebuffer(GL_FRAMEBUFFER, self._hdr_buffer)
        glFramebufferTexture2D(
            GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self._hdr_texture, 0)
        glFramebufferRenderbuffer(
            GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, rbo_depth)

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def render_scene_to_hdr(self, sm, hdr=True, exposure=1.0):
        glBindFramebuffer(GL_FRAMEBUFFER, self._hdr_buffer)
        width, height = sm.get_dimensions()
        glViewport(0, 0, width, height)
        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        r, g, b, a = sm.get_background_color()
        glClearColor(r, g, b, a)
        camera = sm.get_active_camera()
        camera.update()
        self.set_view_matrix(camera.view_matrix)

        # render any lines
        for key, line in sm.get_lines().items():
            self.render_line(line, sm)

        # render objects
        for key, object in sm.get_objects().items():
            if (isinstance(object, Geometry)):
                self.render_geometry(object, sm)
            else:
                self.render_mesh(object, sm)

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self._render_quad.shader.bind()
        self.set_shader(self._render_quad.shader)

        self._shader.link_int("hdr", hdr)
        self._shader.link_float("exposure", exposure)
        glActiveTexture(GL_TEXTURE0 + self._hdr_texture)
        self._shader.link_int("diffuseSampler", self._hdr_texture)
        glBindTexture(GL_TEXTURE_2D, self._hdr_texture)
        self._render_quad.bind()
        self._render_quad.render()
        self._render_quad.unbind_vao()


    def regular_render_scene(self, sm):
        width, height = sm.get_dimensions()
        glViewport(0, 0, width, height)
        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        r, g, b, a = sm.get_background_color()
        glClearColor(r, g, b, a)
        camera = sm.get_active_camera()
        camera.update()
        self.set_view_matrix(camera.view_matrix)

        # render any lines
        for key, line in sm.get_lines().items():
            self.render_line(line, sm)

        # render objects
        for key, object in sm.get_objects().items():
            if (isinstance(object, Geometry)):
                self.render_geometry(object, sm)
            else:
                self.render_mesh(object, sm)

    def render_line(self, line, sm):
        line.shader.bind()
        line.bind()
        line.link_material()
        line.link_model()
        self.set_shader(line.shader)
        self.link_matrices(line.model.get_matrix())
        glDrawArrays(GL_LINES, 0, 2)
        line.unbind_vao()

    def render_geometry(self, geo, sm):
        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)  # enables wireframe
        # glEnable(GL_CULL_FACE)
        geo.shader.bind()
        geo.bind()
        geo.link_material()
        geo.link_model()
        self.set_shader(geo.shader)
        self.link_matrices(geo.model.get_matrix())
        self.render_point_lights(sm.get_point_lights())
        self.render_area_lights(sm.get_area_lights())
        self.render_directional_lights(sm.get_directional_lights())
        self.link_camera(sm.get_active_camera())
        geo.render()

    def render_mesh(self, mesh, sm):
        lights = sm.get_point_lights()
        area_lights = sm.get_area_lights()
        for child in mesh.get_children():
            self.set_shader(child.shader)
            child.shader.bind()
            child.bind()
            child.link_material()
            child.link_model()
            self.link_matrices(child.model.get_matrix())
            self.render_point_lights(lights)
            self.render_area_lights(area_lights)
            self.render_directional_lights(sm.get_directional_lights())
            self.link_camera(sm.get_active_camera())
            child.render()

    def link_matrices(self, model_matrix):
        self._shader.link_mat4(
            "projectionMatrix", self._projection_matrix.to_list())
        self._shader.link_mat4("viewMatrix", self._view_matrix.to_list())
        self._normal_matrix = model_matrix
        self._normal_matrix = glm.transpose(self._normal_matrix)
        self._shader.link_mat4("normalMatrix", self._normal_matrix.to_list())

    def link_camera(self, camera):
        self._shader.link_vec3(
            "cameraPosition", camera.get_position().to_list(), 1)

    def render_area_lights(self, lights):
        count = 0
        for key, light in sorted(lights.items()):
            # check what type of area light we're dealing with here
            if (isinstance(light, CircularAreaLight)):
                self._shader.link_vec3(
                    "circularAreaLights[" + str(count) + "].position", light.get_position().to_list(), 1)
                self._shader.link_vec3(
                    "circularAreaLights[" + str(count) + "].color", light.get_color().to_list(), 1)
                self._shader.link_float(
                    "circularAreaLights[" + str(count) + "].strength", light.get_strength())
                self._shader.link_float(
                    "circularAreaLights[" + str(count) + "].linear", light.get_linear())
                self._shader.link_float(
                    "circularAreaLights[" + str(count) + "].quadratic", light.get_quadratic())
                self._shader.link_float(
                    "circularAreaLights[" + str(count) + "].radius", light.get_radius())
                count += 1

        self._shader.link_int("numAreaLights", count)

    def render_directional_lights(self, lights):
        count = 0
        for key, light in sorted(lights.items()):
            self._shader.link_vec3(
                "dirLights[" + str(count) + "].position", light.get_position().to_list(), 1)
            self._shader.link_vec3(
                "dirLights[" + str(count) + "].color", light.get_color().to_list(), 1)
            self._shader.link_vec3(
                "dirLights[" + str(count) + "].direction", light.get_direction().to_list(), 1)
            self._shader.link_float(
                "dirLights[" + str(count) + "].strength", light.get_strength())
            count += 1

        self._shader.link_int("numDirectionalLights", count)

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
