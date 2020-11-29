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
from shader.Shader import *
from camera.Camera import *
from scene.Manager import *


def main_loop(window, manager):

    # create projection matrix
    proj_matrix = glm.perspective(glm.radians(60), 720/640, 0.1, 1000)
    camera = Camera(position=glm.vec3(0.0, 0.0, -2.5),
                    center=glm.vec3(0.0, 0.0, 0.0))

    while (
        glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS and
        not glfw.window_should_close(window)
    ):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        view_matrix = glm.lookAt(camera.position, camera.center, camera.up)

        for key, object in manager.get_objects().items():
            object.bind()
            object.link_material()
            object.link_model()
            object.shader.link_mat4("projectionMatrix", proj_matrix.to_list())
            object.shader.link_mat4("viewMatrix", view_matrix.to_list())

            gl.glDrawElements(gl.GL_TRIANGLES, len(
                object.get_indices()), gl.GL_UNSIGNED_INT, None)
        glfw.swap_buffers(window)
        glfw.poll_events()


def key_handler(window, key, scan_code, action, mods):
    if (key == glfw.KEY_A):
        print("LEFT")
    elif (key == glfw.KEY_D):
        print("RIGHT")


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
    my_manager = Manager()

    window = create_main_window()
    my_triangle = Triangle("testTriangle")
    my_triangle.shader.load_frag_source(file_name="basicShader.frag.glsl")
    my_triangle.shader.load_vert_source(file_name="basicShader.vert.glsl")
    my_triangle.shader.init()
    my_triangle.setup()
    my_manager.add_object(my_triangle)
    main_loop(window, my_manager)
