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
from geometry.Quad import *
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

    renderer = Renderer()
    renderer.set_projection_matrix(proj_matrix)

    previous_time = 0.0
    current_time = 0.0

    while (
        glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS and
        not glfw.window_should_close(window)
    ):
        current_time = glfw.get_time()
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        camera = sm.get_active_camera()
        view_matrix = glm.lookAt(
            camera.get_position(), camera.get_center(), camera.get_up())
        renderer.set_view_matrix(view_matrix)

        # xCam = math.sin(glfw.get_time() * 0.5) * 20
        # zCam = math.cos(glfw.get_time() * 0.5) * 20

        # camera.set_position(glm.vec3(xCam, camera.get_position()[1], zCam))
        delta = current_time - previous_time
        previous_time = current_time
        sm.update(delta)

        # link objects
        for key, object in sm.get_objects().items():
            if (isinstance(object, Geometry)):
                renderer.render_geometry(object, sm.get_point_lights())
            else:
                renderer.render_mesh(object, sm.get_point_lights())
        glfw.swap_buffers(window)
        glfw.poll_events()


def key_handler(window, key, scan_code, action, mods):

    if (key == glfw.KEY_A):
        tempCube.rotate(glm.vec3(1.0, 0.0, 0.0), 1)
        print("LEFT")
    elif (key == glfw.KEY_D):
        print("RIGHT")
        tempCube.rotate(glm.vec3(-1.0, 0.0, 0.0), 1)
    elif (key == glfw.KEY_Q):
        sm.switch_cameras("secondCam", 0.005)


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
    my_light.set_position(glm.vec3(1.0, 10.0, 0.0))
    my_light.set_strength(100.0)
    sm.add_point_light(my_light)

    earth = Mesh("earth")
    earth.load_model(filename="Medieval-House.obj")
    earth.scale(glm.vec3(0.5, 0.5, 0.5))
    earth.translate(glm.vec3(0.25, -3.0, 0.0))
    earth.calc_model_matrix()
    sm.add_object(earth)

    tree = Mesh("tree")
    tree.load_model(filename="Lowpoly_tree_sample.obj")
    tree.scale(glm.vec3(0.25, 0.25, 0.25))
    tree.translate(glm.vec3(-4, -10, 0.0))
    tree.calc_model_matrix()
    sm.add_object(tree)

    my_cube = Cube("testCube")
    my_cube.shader.load_frag_source(file_name="basicShader.frag.glsl")
    my_cube.shader.load_vert_source(file_name="basicShader.vert.glsl")
    my_cube.shader.init()
    my_cube.set_diffuse_texture(filename="poggers.png")
    my_cube.translate(glm.vec3(9, -1.0, 0.0))
    my_cube.scale(glm.vec3(10, 3, 3))
    my_cube.setup()
    sm.add_object(my_cube)

    my_plane = Quad("testPlane", material=Material(ambient=glm.vec3(0.5, 0.5, 0.5)))
    my_plane.shader.load_frag_source(file_name="basicShader.frag.glsl")
    my_plane.shader.load_vert_source(file_name="basicShader.vert.glsl")
    my_plane.shader.init()
    # my_plane.set_diffuse_texture(filename="poggers.png")
    my_plane.translate(glm.vec3(0.0, -2.0, 0.0))
    my_plane.scale(glm.vec3(100, 1, 100))
    my_plane.setup()
    sm.add_object(my_plane)

    camera = Camera("mainCam", position=glm.vec3(10, 2.0, -15),
                    center=earth.get_worldspace_centroid(), up=glm.vec3(0.0, 1.0, 0.0))

    cameraTwo = Camera("secondCam", position=glm.vec3(3, 6.0, 15),
                       center=my_cube.model.get_position(), up=glm.vec3(0.0, 1.0, 0.0))

    sm.add_camera(camera)
    sm.add_camera(cameraTwo)

    main_loop(window)
