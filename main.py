import sys
from OpenGL import GL as gl
import glfw
import glm
import numpy as np
import math
import imgui
from imgui.integrations.glfw import GlfwRenderer
from geometry.Triangle import *
from material.Material import Material
from geometry.Cube import *
from geometry.Mesh import *
from geometry.Quad import *
from shader.Shader import *
from camera.ThirdPersonCamera import *
from scene.Manager import *
from lighting.Pointlight import *
from renderer.Renderer import *


# global manager
sm = Manager()
sm.set_dimensions(720, 640)


def main_loop(window):
    global sm

    width, height = sm.get_dimensions()
    # create projection matrix
    proj_matrix = glm.perspective(glm.radians(90), width/height, 0.1, 10000)

    renderer = Renderer()
    renderer.set_projection_matrix(proj_matrix)

    previous_time = 0.0
    current_time = 0.0

    while (
        glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS and
        not glfw.window_should_close(window)
    ):
        width, height = sm.get_dimensions()
        gl.glViewport(0, 0, width, height)
        current_time = glfw.get_time()
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        r, g, b, a = sm.get_background_color()
        gl.glClearColor(r, g, b, a)
        camera = sm.get_active_camera()
        camera.update()
        renderer.set_view_matrix(camera.view_matrix)

        delta = current_time - previous_time
        previous_time = current_time
        sm.update(delta)

        # link objects
        for key, object in sm.get_objects().items():
            if (isinstance(object, Geometry)):
                renderer.render_geometry(object, sm)
            else:
                renderer.render_mesh(object, sm)
        glfw.swap_buffers(window)
        glfw.poll_events()


def key_handler(window, key, scan_code, action, mods):
    global sm

    quad = sm.get_object("testPlane")

    if (key == glfw.KEY_A):
        quad.rotate(glm.vec3(1.0, 0.0, 0.0), 15)


def create_main_window():
    global sm
    if not glfw.init():
        sys.exit(1)

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 4)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    title = 'MyPy Engine'
    width, height = sm.get_dimensions()

    window = glfw.create_window(width, height, title, None, None)
    if not window:
        sys.exit(2)
    glfw.make_context_current(window)

    glfw.set_input_mode(window, glfw.STICKY_KEYS, True)
    glfw.set_key_callback(window, key_handler)
    glfw.set_cursor_pos_callback(window, sm.mouse_pos_handler)
    glfw.set_mouse_button_callback(window, sm.mouse_button_handler)
    glfw.set_scroll_callback(window, sm.mouse_scroll_handler)
    glfw.set_window_size_callback(window, window_resize_listener)

    return window


def window_resize_listener(window, width, height):
    global sm
    sm.set_dimensions(width, height)


if __name__ == '__main__':
    # imgui.create_context()
    window = create_main_window()

    # sm.debug_window = GlfwRenderer(window)

    # sm.input.handle_right_click_press = lambda: print("Here!")
    sm.input.handle_mouse_zoom_in = lambda: sm.get_active_camera().move_toward(sm.delta_time)
    sm.input.handle_mouse_zoom_out = lambda: sm.get_active_camera().move_backward(sm.delta_time)
    sm.set_background_color(glm.vec4(0.0, 0.0, 0.2, 1.0))

    my_light = Pointlight("light1")
    my_light.set_position(glm.vec3(0.0, 5.0, 0.0))
    my_light.set_strength(1)
    sm.add_point_light(my_light)

    # my_light = Pointlight("light2")
    # my_light.set_position(glm.vec3(250.0, 10.0, 25.0))
    # my_light.set_color(glm.vec3(0.5, 0.0, 0.0))
    # my_light.set_strength(2)
    # sm.add_point_light(my_light)

    # car = Mesh("car")
    # car.load_model(filename="car_new.obj")
    # car.scale(glm.vec3(0.5, 0.5, 0.5))
    # car.translate(glm.vec3(35, 0, 0.0))
    # sm.add_object(car)

    # test_cube = Cube("testCube", material=Material(
    #     ambient=glm.vec3(0.4, 0.4, 0.4), diffuse=glm.vec3(0.5, 0, 0)))
    # test_cube.shader.load_frag_source(file_name="basicShader.frag.glsl")
    # test_cube.shader.load_vert_source(file_name="basicShader.vert.glsl")
    # test_cube.shader.init()
    # test_cube.translate(glm.vec3(1.0, 10.0, 0.0))
    # test_cube.setup()
    # sm.add_object(test_cube)

    # my_cube = Cube("myCube")
    # my_cube.shader.load_frag_source(file_name="basicShader.frag.glsl")
    # my_cube.shader.load_vert_source(file_name="basicShader.vert.glsl")
    # my_cube.shader.init()
    # my_cube.set_diffuse_texture(filename="default.jpg")
    # my_cube.translate(glm.vec3(-10, 0.2, -10))
    # # my_cube.scale(glm.vec3(10, 3, 3))
    # my_cube.setup()
    # sm.add_object(my_cube)

    # my_cube2 = Cube("myCube2")
    # my_cube2.shader.load_frag_source(file_name="basicShader.frag.glsl")
    # my_cube2.shader.load_vert_source(file_name="basicShader.vert.glsl")
    # my_cube2.shader.init()
    # my_cube2.set_diffuse_texture(filename="default.jpg")
    # my_cube2.translate(glm.vec3(-10.0, 0.2, 0))
    # # my_cube.scale(glm.vec3(10, 3, 3))
    # my_cube2.setup()
    # sm.add_object(my_cube2)

    # my_cube3 = Cube("myCube3-ZAXIS")
    # my_cube3.shader.load_frag_source(file_name="basicShader.frag.glsl")
    # my_cube3.shader.load_vert_source(file_name="basicShader.vert.glsl")
    # my_cube3.shader.init()
    # my_cube3.set_diffuse_texture(filename="default.jpg")
    # my_cube3.translate(glm.vec3(0.0, 5.0, -10))
    # my_cube3.scale(glm.vec3(11, 1, 3))
    # my_cube3.setup()
    # sm.add_object(my_cube3)

    my_plane = Quad("testPlane", 40, 40, False, material=Material(
        ambient=glm.vec3(0.5, 0.5, 0.5), nVal=50, specular=glm.vec3(0.1, 0.1, 0.1)))
    my_plane.shader.load_frag_source(file_name="basicShader.frag.glsl")
    my_plane.shader.load_vert_source(file_name="basicShader.vert.glsl")
    my_plane.set_diffuse_texture(filename="default.jpg")
    my_plane.shader.init()
    my_plane.setup()
    my_plane.scale(glm.vec3(1, 5, 1))
    sm.add_object(my_plane)

    camera = ThirdPersonCamera("mainCam", position=glm.vec3(-5, 10.0, 5),
                               center=glm.vec3(0, 0, 0), up=glm.vec3(0.0, 1.0, 0.0))

    sm.add_camera(camera)
    sm.get_active_camera().set_zoom_speed(5.0)

    main_loop(window)
