import contextlib
from material.Material import Material
import sys
from OpenGL import GL as gl
import time
import glfw
import ctypes
import glm
import math
from geometry.Triangle import *
from geometry.Cube import *
from shader.Shader import *
from camera.Camera import *
from scene.Manager import *
from lighting.Pointlight import *


# global manager
sm = Manager()


def main_loop(window):
    global sm

    # create projection matrix
    proj_matrix = glm.perspective(glm.radians(60), 720/640, 0.1, 1000)
    camera = Camera(position=glm.vec3(0.0, 0.0, -2.5),
                    center=glm.vec3(0.0, 0.0, 0.0))

    

    while (
        glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS and
        not glfw.window_should_close(window)
    ):
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        view_matrix = glm.lookAt(camera.position, camera.center, camera.up)

        # link objects
        for key, object in sm.get_objects().items():
            object.bind()
            object.link_material()
            object.link_model()
            object.shader.link_mat4("projectionMatrix", proj_matrix.to_list())
            object.shader.link_mat4("viewMatrix", view_matrix.to_list())
            normal_matrix = -object.model.get_matrix()
            mormal_matrix = glm.transpose(normal_matrix)
            object.shader.link_mat4("normalMatrix", normal_matrix.to_list())

            # link lights
            count = 0
            for key, light in sorted(sm.get_point_lights().items()):
                object.shader.link_vec3("pointLights[" + str(count) + "].position", light.get_position().to_list(), 1)
                object.shader.link_vec3("pointLights[" + str(count) + "].color", light.get_color().to_list(), 1)
                object.shader.link_float("pointLights[" + str(count) + "].strength", light.get_strength())
                count += 1

            object.shader.link_int("numPointLights", count)

            gl.glDrawElements(gl.GL_TRIANGLES, len(
                object.get_indices()), gl.GL_UNSIGNED_INT, None)
        glfw.swap_buffers(window)
        glfw.poll_events()


def key_handler(window, key, scan_code, action, mods):
    tempCube = sm.get_object("testCube")

    if (key == glfw.KEY_A):
        tempCube.rotate(glm.vec3(1.0, 0.0, 0.0), 1)
    elif (key == glfw.KEY_D):
        tempCube.rotate(glm.vec3(-1.0, 0.0, 0.0), 1)


def create_main_window():
    if not glfw.init():
        sys.exit(1)

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 4)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    title = 'MyPy Engine'
    window = glfw.create_window(720, 640, title, None, None)
    if not window:
        sys.exit(2)
    glfw.make_context_current(window)

    glfw.set_input_mode(window, glfw.STICKY_KEYS, True)
    glfw.set_key_callback(window, key_handler)
    gl.glClearColor(0, 0, 0.4, 1.0)

    return window


if __name__ == '__main__':

    window = create_main_window()
    my_light = Pointlight("light1")
    my_light.set_position(glm.vec3(1.0, 5.0, 0.0))
    sm.add_point_light(my_light)

    my_cube = Cube("testCube")
    my_cube.shader.load_frag_source(file_name="basicShader.frag.glsl")
    my_cube.shader.load_vert_source(file_name="basicShader.vert.glsl")
    my_cube.shader.init()
    my_cube.setup()

    sm.add_object(my_cube)
    main_loop(window)
