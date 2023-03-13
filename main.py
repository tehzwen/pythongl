import sys
from OpenGL import *
import glfw
import glm
from geometry.Triangle import *
from material.Material import Material
from geometry.Cube import *
from geometry.Mesh import *
from geometry.Quad import *
from geometry.Sphere import *
from geometry.Line import *
from shader.Shader import *
from camera.ThirdPersonCamera import *
from scene.Manager import *
from scene.Axis import *
from lighting.Pointlight import *
from lighting.AreaLight import *
from lighting.DirectionalLight import *
from renderer.Renderer import *


# global manager
sm = Manager()
sm.set_dimensions(720, 640)


def main_loop(window):
    global sm

    width, height = sm.get_dimensions()
    # create projection matrix
    proj_matrix = glm.perspective(glm.radians(90), width/height, 0.1, 10000)
    glEnable(GL_MULTISAMPLE)

    renderer = Renderer()
    renderer.set_projection_matrix(proj_matrix)
    renderer.setup_hdr_buffer(sm)

    previous_time = 0.0
    current_time = 0.0

    while (
        glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS and
        not glfw.window_should_close(window)
    ):
        delta = current_time - previous_time
        previous_time = current_time
        sm.update(delta)
        current_time = glfw.get_time()
        
        # renderer.regular_render_scene(sm)
        renderer.render_scene_to_hdr(sm, exposure=1.0)

        glfw.swap_buffers(window)
        glfw.poll_events()


def key_handler(window, key, scan_code, action, mods):
    global sm

    # quad = sm.get_object("testPlane")

    # if (key == glfw.KEY_A):
    #     quad.rotate(glm.vec3(1.0, 0.0, 0.0), 15)
    # elif (key == glfw.KEY_W):
    #     # print(glfw.get_time())
    #     quad.alter_heights(lambda: 0.5 * np.random.randn()
    #                        * math.sin(glfw.get_time()))

    if (key == glfw.KEY_A):
        sm.axis.set_position(glm.vec3(5.0, 0.0, 0.0))


def create_main_window():
    global sm
    if not glfw.init():
        sys.exit(1)

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.SAMPLES, 4)

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
    sm.set_background_color(glm.vec4(0.0, 0.0, 0.0, 1.0))

    # car = Mesh("car")
    # car.load_model(filename="car_new.obj")
    # car.scale(glm.vec3(0.5, 0.5, 0.5))
    # car.translate(glm.vec3(35, 0, 0.0))
    # sm.add_object(car)

    # my_cube2 = Cube("myCube2")
    # my_cube2.shader.load_frag_source(file_name="basicShader.frag.glsl")
    # my_cube2.shader.load_vert_source(file_name="basicShader.vert.glsl")
    # my_cube2.shader.init()
    # my_cube2.set_diffuse_texture(filename="default.jpg")
    # my_cube2.translate(glm.vec3(-10.0, 0.2, 0))
    # # my_cube.scale(glm.vec3(10, 3, 3))
    # my_cube2.setup()
    # sm.add_object(my_cube2)

    my_light = Pointlight("light1", strength=15.0,
                          position=glm.vec3(30.0, 35.0, 0.0), color=glm.vec3(0.5, 0.0, 0.0))
    sm.add_point_light(my_light)

    my_dir_light = DirectionalLight("dirLight1", direction=glm.vec3(-1,-0.25,0), position=glm.vec3(200, 150, 0), strength=2)
    sm.add_directional_light(my_dir_light)
    my_sphere = Sphere("lightSphere", 10, 10, 10, material=Material(nVal=200), model=Model(position=glm.vec3(200, 150, 0)))
    my_sphere.shader.load_frag_source(file_name="lightObject")
    my_sphere.shader.load_vert_source(file_name="lightObject")
    my_sphere.shader.init()
    my_sphere.setup()
    # my_sphere.scale(glm.vec3(50, 1, 50))
    sm.add_object(my_sphere)


    scene_axis = Axis()
    for line in scene_axis.get_lines():
        sm.add_line(line)

    sm.axis = scene_axis

    my_plane = Quad("testPlane", 100, 50, smooth=True, dynamic=False, material=Material(
        ambient=glm.vec3(0.5, 0.5, 0.5), nVal=math.inf, specular=glm.vec3(0.1, 0.1, 0.1), diffuse=glm.vec3(0.3, 0.3, 0.3)))
    my_plane.shader.load_frag_source(file_name="basicShader")
    my_plane.shader.load_vert_source(file_name="basicShader")
    my_plane.shader.init()
    my_plane.setup()
    my_plane.set_diffuse_texture(filename="kekw.jpg")
    # my_plane.scale(glm.vec3(1, 1, 1))
    my_plane.translate(glm.vec3(0, -10, 0))
    sm.add_object(my_plane)

    camera = ThirdPersonCamera("mainCam", position=glm.vec3(-5, 10.0, 5),
                               center=glm.vec3(0, 0, 0), up=glm.vec3(0.0, 1.0, 0.0))

    sm.add_camera(camera)
    sm.get_active_camera().set_zoom_speed(5.0)

    main_loop(window)
