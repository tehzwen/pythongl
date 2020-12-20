import glm
import math
import glfw
from scene.Input import *


class Manager():
    def __init__(self):
        self._objects = {}
        self._lines = {}
        self._point_lights = {}
        self._area_lights = {}
        self._directional_lights = {}
        self._cameras = {}
        self._active_camera = None
        self._background_color = glm.vec4(0.0, 0.0, 0.0, 1.0)
        self.debug_window = None
        self.input = Input()
        self.delta_time = None
        self.changed = False
        self.dimensions = {
            "width": 0,
            "height": 0
        }
        self.axis = None

    def get_background_color(self):
        return self._background_color

    def set_background_color(self, bg):
        self._background_color = bg

    def set_dimensions(self, width, height):
        self.dimensions["width"] = width
        self.dimensions["height"] = height

    def get_dimensions(self):
        return (self.dimensions["width"], self.dimensions["height"])

    def add_line(self, line):
        if (line.get_name() not in self._lines):
            self._lines[line.get_name()] = line
        else:
            raise Exception(
                "Line with this name already exists in the scene, names must be unique")

    def get_lines(self):
        return self._lines

    def get_line(self, name):
        if (name in self._lines):
            return self._lines[name]
        else:
            raise Exception("No line with this name")

    def add_object(self, object):
        if (object.get_name() not in self._objects):
            self._objects[object.get_name()] = object
        else:
            raise Exception(
                "Object with this name already exists in the scene, names must be unique")

    def get_objects(self):
        return self._objects

    def get_object(self, name):
        if (name in self._objects):
            return self._objects[name]
        else:
            raise Exception("No object with this name")

    def add_point_light(self, light):
        if (light.get_name() not in self._point_lights):
            self._point_lights[light.get_name()] = light
        else:
            raise Exception(
                "Pointlight with this name already exists in the scene, names must be unique")

    def get_point_lights(self):
        return self._point_lights

    def get_point_light(self, name):
        if (name in self._point_lights):
            return self._point_lights[name]
        else:
            raise Exception("No Pointlight with this name")

    def add_area_light(self, light):
        if (light.get_name() not in self._area_lights):
            self._area_lights[light.get_name()] = light
        else:
            raise Exception(
                "Pointlight with this name already exists in the scene, names must be unique")

    def get_area_lights(self):
        return self._area_lights

    def get_area_light(self, name):
        if (name in self._area_lights):
            return self._area_lights[name]
        else:
            raise Exception("No Pointlight with this name")

    def add_directional_light(self, light):
        if (light.get_name() not in self._directional_lights):
            self._directional_lights[light.get_name()] = light
        else:
            raise Exception(
                "DirectionalLight with this name already exists in the scene, names must be unique")

    def get_directional_lights(self):
        return self._directional_lights

    def get_directional_light(self, name):
        if (name in self._directional_lights):
            return self._directional_lights[name]
        else:
            raise Exception("No DirectionalLight with this name")

    def add_camera(self, cam):
        if (cam.get_name() not in self._cameras):
            self._cameras[cam.get_name()] = cam
            if (not self._active_camera):
                self._active_camera = cam.get_name()

    def get_camera(self, name):
        if (name in self._cameras):
            return self._cameras[name]

    def get_active_camera(self):
        return self._cameras[self._active_camera]

    def set_active_camera(self, name):
        if (name in self._cameras):
            self._active_camera = name

    def mouse_pos_handler(self, window, x_pos, y_pos):
        if (x_pos != self.input.x):
            self.input.set_x(x_pos)
        else:
            self.input.delta_x = 0
        if (y_pos != self.input.y):
            self.input.set_y(y_pos)
        else:
            self.input.delta_y = 0

    def mouse_button_handler(self, window, button, action, mods):
        if (button == glfw.MOUSE_BUTTON_RIGHT):
            if (action == glfw.PRESS):
                self.input.handle_right_click_press()
                self.input.mouse_right_down = True
            elif (action == glfw.RELEASE):
                self.input.mouse_right_down = False
        if (button == glfw.MOUSE_BUTTON_LEFT):
            if (action == glfw.PRESS):
                self.input.handle_left_click_press()
                self.input.mouse_left_down = True
            elif (action == glfw.RELEASE):
                self.input.mouse_left_down = False

    def mouse_scroll_handler(self, window, x_offset, y_offset):
        if (y_offset == 1.0):
            self.input.handle_mouse_zoom_in()
        elif (y_offset == -1.0):
            self.input.handle_mouse_zoom_out()

    def update(self, delta_time):
        self.delta_time = delta_time
        cam = self.get_active_camera()

        self.axis.set_position(cam.get_center())

        # check if camera is looking or moving
        if (cam.state["moving"]):
            cam.lerp_camera_position(delta_time)
        if (cam.state["looking"]):
            cam.lerp_camera_center(delta_time)

        if (self.input.mouse_right_down):
            if (self.input.delta_x > 1.0 or self.input.delta_x < -1.0):
                cam.rate_x += self.input.delta_x
                cam.rotate_horizontal()

            if (self.input.delta_y > 1.0 or self.input.delta_y < -1.0):
                cam.rotate_vertical(-self.input.delta_y)

        if (self.input.mouse_left_down):
            forward = cam.get_center() - cam.get_position()
            right = glm.cross(forward, cam.get_up())

            out_vec = glm.vec3(0, 0, 0)
            if (self.input.delta_x < -1.0):
                out_vec -= right
            elif (self.input.delta_x > 1.0):
                out_vec += right

            if (self.input.delta_y > 1.0):
                out_vec += glm.vec3(-forward[0], 0.0, -forward[2])
            elif (self.input.delta_y < -1.0):
                out_vec += glm.vec3(forward[0], 0.0, forward[2])

            cam.translate(out_vec)
