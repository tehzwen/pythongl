import math
from camera.Camera import *


class ThirdPersonCamera(Camera):
    def __init__(self, name, position=None, up=None, center=None):
        super().__init__(name, position, up, center)
        self._zoom_speed = 0.5
        self._rotate_speed = 0.005
        self._translate_speed = 0.01
        self.rate_x = 0
        self.rate_y = 0
        self.translation = glm.vec3()

    def get_rotate_speed(self):
        return self._rotate_speed

    def set_rotate_speed(self, speed):
        self._rotate_speed = speed

    def get_zoom_speed(self):
        return self._zoom_speed

    def set_zoom_speed(self, speed):
        self._zoom_speed = speed

    def move_toward(self, delta_time):
        forward = self.get_center() - self.get_position()
        self.set_position(
            (forward * delta_time * self._zoom_speed) + self.get_position())
        self.distance = glm.distance(self._position, self._center)

    def translate(self, trans_vec):
        trans_vec *= self._translate_speed
        self.set_center(self.get_center() + trans_vec)
        self.set_position(self.get_position() + trans_vec)
        self.distance = glm.distance(self._position, self._center)
        self.translation += trans_vec

    def move_backward(self, delta_time):
        forward = self.get_center() - self.get_position()
        self.set_position(
            (-forward * delta_time * self._zoom_speed) + self.get_position())
        self.distance = glm.distance(self._position, self._center)

    def rotate_horizontal(self):
        xCam = math.sin(self.rate_x * self._rotate_speed) * self.distance
        zCam = math.cos(self.rate_x * self._rotate_speed) * self.distance
        self.set_position(glm.vec3(
            xCam + self.translation[0], self._position[1], zCam + self.translation[2]))

    def rotate_vertical(self, delta_y):
        if (self.rate_y + delta_y > 0.0 and self.rate_y + delta_y < 180):
            self.rate_y += delta_y
            yVal = math.sin(self.rate_y * self._rotate_speed)
            yCam = yVal * self.distance
            self.set_position(
                glm.vec3(self._position[0], yCam + self.translation[1], self._position[2]))
