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
from geometry.Mesh import *
from shader.Shader import *
from camera.Camera import *
from scene.Manager import *
from lighting.Pointlight import *
from renderer.Renderer import *


# global manager
sm = Manager()


def main_loop(window):
    global sm

    # create projection matrix
    proj_matrix = glm.perspective(glm.radians(60), 720/640, 0.1, 1000)
    camera = Camera(position=glm.vec3(0.0, 0.0, -25),
                    center=glm.vec3(0.0, 0.0, 0.0))

    renderer = Renderer()
    renderer.set_projection_matrix(proj_matrix)

    while (
        glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS and
        not glfw.window_should_close(window)
    ):
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        view_matrix = glm.lookAt(camera.position, camera.center, camera.up)
        renderer.set_view_matrix(view_matrix)

        # link objects
        for key, object in sm.get_objects().items():
            if (isinstance(object, Geometry)):
                renderer.render_geometry(object, sm.get_point_lights())
            else:
                renderer.render_mesh(object, sm.get_point_lights())
        glfw.swap_buffers(window)
        glfw.poll_events()


def key_handler(window, key, scan_code, action, mods):
    # tempCube = sm.get_object("testCube")

    if (key == glfw.KEY_A):
        # tempCube.rotate(glm.vec3(1.0, 0.0, 0.0), 1)
        print("LEFT")
    elif (key == glfw.KEY_D):
        print("RIGHT")
        # tempCube.rotate(glm.vec3(-1.0, 0.0, 0.0), 1)


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

    earth = Mesh("earth")
    earth.load_model(filename="earth.obj")
    earth.scale(glm.vec3(0.5, 0.5, 0.5))
    earth.translate(glm.vec3(0.0, -18, 0.0))
    sm.add_object(earth)

    my_cube = Cube("testCube")
    my_cube.shader.load_frag_source(file_name="basicShader.frag.glsl")
    my_cube.shader.load_vert_source(file_name="basicShader.vert.glsl")
    my_cube.shader.init()
    my_cube.material.diffuseTexture = my_cube.material.load_texture(filename="poggers.png")
    my_cube.translate(glm.vec3(2.5, 0.0, 0.0))
    my_cube.scale(glm.vec3(10, 10, 10))
    my_cube.setup()
    sm.add_object(my_cube)

    # my_cube2 = Cube("testCubeTwo")
    # my_cube2.shader.load_frag_source(file_name="basicShader.frag.glsl")
    # my_cube2.shader.load_vert_source(file_name="basicShader.vert.glsl")
    # my_cube2.shader.init()
    # my_cube2.translate(glm.vec3(-1.5, 0.0, 0.0))
    # my_cube2.setup()
    # sm.add_object(my_cube2)


    # my_triangle = Triangle("testTriangle")
    # my_triangle.shader.load_frag_source(file_name="basicShader.frag.glsl")
    # my_triangle.shader.load_vert_source(file_name="basicShader.vert.glsl")
    # my_triangle.shader.init()
    # my_triangle.setup()
    # sm.add_object(my_triangle)

    main_loop(window)
