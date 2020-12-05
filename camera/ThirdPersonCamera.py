from camera.Camera import *


class ThirdPersonCamera(Camera):
    def __init__(self, name, position=None, up=None, center=None):
        super().__init__(name, position, up, center)
        self._zoom_speed = 0.5
        self._rotate_speed = 0.005
        self._horiz_spin = 0.0
        self._vert_spin = 0.0

    def get_rotate_speed(self):
        return self._rotate_speed

    def set_rotate_speed(self, speed):
        self._rotate_speed = speed

    def get_zoom_speed(self):
        return self._zoom_speed

    def get_horiz_spin(self):
        return self._horiz_spin

    def set_horiz_spin(self, value):
        self._horiz_spin = value

    def get_vert_spin(self):
        return self._vert_spin

    def set_vert_spin(self, value):
        self._vert_spin = value

    def set_zoom_speed(self, speed):
        self._zoom_speed = speed

    def move_toward(self, delta_time):
        forward = self.get_center() - self.get_position()
        self.set_position(
            (forward * delta_time * self._zoom_speed) + self.get_position())
        self.distance = glm.distance(self._position, self._center)
        

    def move_backward(self, delta_time):
        forward = self.get_center() - self.get_position()
        self.set_position(
            (-forward * delta_time * self._zoom_speed) + self.get_position())
        self.distance = glm.distance(self._position, self._center)
        

    def rotate_horizontal(self):
        xCam = math.sin(self._horiz_spin * self._rotate_speed) * self.distance
        zCam = math.cos(self._horiz_spin * self._rotate_speed) * self.distance
        self.set_position(glm.vec3(xCam, self._position[1], zCam))

    def rotate_vertical(self):
        yCam = math.sin(self._vert_spin * self._rotate_speed) * self.distance
        print(yCam)
        self.set_position(glm.vec3(self._position[0], -yCam, self._position[2]))
