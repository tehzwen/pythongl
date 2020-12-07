import glm
import math
from mymath.Utilities import *


class Camera():
    def __init__(self, name, position=None, up=None, center=None):
        self._name = name
        self._position = position if position else glm.vec3()
        self._up = up if up else glm.vec3(0.0, 1.0, 0.0)
        self._center = center if center else glm.vec3()
        self._input = {"move": False, "x": 0.0, "y": 0.0}
        self.state = {"moving": False,
                      "looking": False,
                      "target_position": None,
                      "target_center": None,
                      "move_speed": 0,
                      "look_speed": 0}
        self.distance = glm.distance(self._position, self._center)
        self.view_matrix = glm.mat4()

    def get_position(self):
        return self._position

    def get_up(self):
        return self._up

    def get_center(self):
        return self._center

    def set_position(self, position):
        self._position = position

    def set_up(self, up):
        self._up = up

    def set_center(self, center):
        self._center = center

    def get_name(self):
        return self._name

    def set_target(self, target_position, target_center, move_speed, look_speed):
        self.state["moving"] = True
        self.state["looking"] = True
        self.state["target_position"] = target_position
        self.state["target_center"] = target_center
        self.state["move_speed"] = move_speed
        self.state["look_speed"] = look_speed

    def lerp_camera_position(self, delta_time):
        done, position = lerp_to_vec3(
            self.get_position(), self.state["target_position"], self.state["move_speed"], delta_time)
        self._position = position
        if (done):
            self.state["moving"] = False
            self.state["target_position"] = None

    def lerp_camera_center(self, delta_time):
        done, center = lerp_to_vec3(
            self.get_center(), self.state["target_center"], self.state["look_speed"], delta_time)
        self._center = center
        if (done):
            self.state["looking"] = False
            self.state["target_center"] = None

    def rotate_around_horizontal(self, time, speed, distance, reverse):
        xCam = math.sin(time * speed) * distance
        zCam = math.cos(time * speed) * distance

        if (reverse):
            self.set_position(glm.vec3(-xCam, self._position[1], -zCam))
        else:
            self.set_position(glm.vec3(-xCam, self._position[1], zCam))

    def update(self):
        self.view_matrix = glm.lookAt(
            self.get_position(), self.get_center(), self.get_up())
