import glm
from lighting.Light import *


class DirectionalLight(Light):
    def __init__(self, name, direction=glm.vec3(), position=glm.vec3(), strength=1.0, color=glm.vec3(1, 1, 1)):
        super().__init__(name)
        self._name = name
        self._direction = direction
        self._position = position
        self._strength = strength
        self._color = color

    def get_direction(self):
        return self._direction

    def set_direction(self, val):
        self._direction = val
