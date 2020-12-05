import contextlib
import sys
from OpenGL import GL as gl
import glfw
import glm
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
    proj_matrix = glm.perspective(glm.radians(90), width/height, 0.1, 1000)

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
        camera = sm.get_active_camera()
        view_matrix = glm.lookAt(
            camera.get_position(), camera.get_center(), camera.get_up())
        renderer.set_view_matrix(view_matrix)

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
    global sm

    cam = sm.get_active_camera()

    if (key == glfw.KEY_A):
        # cam.move_toward(sm.delta_time)
        cam.rotate_horizontal(0.5, sm.delta_time)
    elif (key == glfw.KEY_D):
        # cam.move_backward(sm.delta_time)
        cam.rotate_horizontal(glfw.get_time(), sm.delta_time)
    elif (key == glfw.KEY_Q):
        # sm.get_active_camera().set_target(glm.vec3(0, 0, 0), glm.vec3(0, 6, 0), 0.5, 0.05)
        # sm.get_active_camera().set_target(glm.vec3(0, 0, 0), sm.get_active_camera().get_center(), 0.5, 0.05)
        sm.get_active_camera().set_target(
            sm.get_active_camera().get_position(), glm.vec3(0, -6, 5), 0.5, 0.05)

    elif (key == glfw.KEY_1):
        sm.get_active_camera().rotate_around_horizontal(glfw.get_time(), 0.5, 20, False)


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
    r, g, b, a = sm.get_background_color()
    gl.glClearColor(r, g, b, a)
    glfw.set_window_size_callback(window, window_resize_listener)

    return window

def window_resize_listener(window, width, height):
    global sm
    sm.set_dimensions(width, height)

if __name__ == '__main__':

    # imgui.create_context()
    window = create_main_window()

    # sm.debug_window = GlfwRenderer(window)

    sm.input.handle_left_click_press = lambda: print("Here!")
    sm.input.handle_mouse_zoom_in = lambda: sm.get_active_camera().move_toward(sm.delta_time)
    sm.input.handle_mouse_zoom_out = lambda: sm.get_active_camera().move_backward(sm.delta_time)

    my_light = Pointlight("light1")
    my_light.set_position(glm.vec3(1.0, 10.0, 0.0))
    my_light.set_strength(100.0)
    sm.add_point_light(my_light)

    # earth = Mesh("earth")
    # earth.load_model(filename="earth.obj")
    # earth.scale(glm.vec3(0.5, 0.5, 0.5))
    # earth.translate(glm.vec3(0.25, -3.0, 0.0))
    # earth.calc_model_matrix()
    # sm.add_object(earth)

    # tree = Mesh("tree")
    # tree.load_model(filename="Lowpoly_tree_sample.obj")
    # tree.scale(glm.vec3(0.25, 0.25, 0.25))
    # tree.translate(glm.vec3(-4, -10, 0.0))
    # tree.calc_model_matrix()
    # sm.add_object(tree)

    test_cube = Cube("testCube", material=Material(
        ambient=glm.vec3(0.4, 0.4, 0.4), diffuse=glm.vec3(0.5, 0, 0)))
    test_cube.shader.load_frag_source(file_name="basicShader.frag.glsl")
    test_cube.shader.load_vert_source(file_name="basicShader.vert.glsl")
    test_cube.shader.init()
    test_cube.translate(glm.vec3(-8, -1.0, 0.0))
    test_cube.setup()
    sm.add_object(test_cube)

    my_cube = Cube("myCube")
    my_cube.shader.load_frag_source(file_name="basicShader.frag.glsl")
    my_cube.shader.load_vert_source(file_name="basicShader.vert.glsl")
    my_cube.shader.init()
    my_cube.set_diffuse_texture(filename="poggers.png")
    my_cube.translate(glm.vec3(9, -1.0, 0.0))
    my_cube.scale(glm.vec3(10, 3, 3))
    my_cube.setup()
    sm.add_object(my_cube)

    my_plane = Quad("testPlane", material=Material(
        ambient=glm.vec3(0.5, 0.5, 0.5)))
    my_plane.shader.load_frag_source(file_name="basicShader.frag.glsl")
    my_plane.shader.load_vert_source(file_name="basicShader.vert.glsl")
    my_plane.shader.init()
    # my_plane.set_diffuse_texture(filename="poggers.png")
    my_plane.translate(glm.vec3(0.0, -2.0, 0.0))
    my_plane.scale(glm.vec3(1000, 1, 1000))
    my_plane.setup()
    sm.add_object(my_plane)

    camera = ThirdPersonCamera("mainCam", position=glm.vec3(10, 2.0, -15),
                               center=test_cube.get_centroid(), up=glm.vec3(0.0, 1.0, 0.0))

    sm.add_camera(camera)
    sm.get_active_camera().set_zoom_speed(5.0)


    main_loop(window)
