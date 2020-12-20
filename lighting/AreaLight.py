from lighting.Light import *

class CircularAreaLight(Light):
    def __init__(self, name, radius=1.0, linear=None, quadratic=None, strength=None, position=None):
        super().__init__(name)
        self._radius = radius
        self._linear = linear if linear else 0.1
        self._quadratic = quadratic if quadratic else 0.001
        self._strength = strength if strength else 1.0
        self._position = position if position else glm.vec3()

    def get_linear(self):
        return self._linear

    def set_linear(self, val):
        self._linear = val

    def get_quadratic(self):
        return self._quadratic

    def set_quadratic(self, val):
        self._quadratic = val

    def get_radius(self):
        return self._radius

    def set_radius(self, val):
        self._radius = val
