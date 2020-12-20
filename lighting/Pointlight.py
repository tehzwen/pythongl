import glm
from enum import Enum
from lighting.Light import *


class LightType(Enum):
    normal = 1
    square = 2
    circular = 3


class Pointlight(Light):
    def __init__(self, name, linear=None, quadratic=None, strength=None, position=None, color=glm.vec3(1, 1, 1)):
        super().__init__(name)
        self._name = name
        self._linear = linear if linear else 0.1
        self._quadratic = quadratic if quadratic else 0.001
        self._strength = strength if strength else 1.0
        self._position = position if position else glm.vec3()
        self._color = color

    def get_linear(self):
        return self._linear

    def set_linear(self, val):
        self._linear = val

    def get_quadratic(self):
        return self._quadratic

    def set_quadratic(self, val):
        self._quadratic = val
