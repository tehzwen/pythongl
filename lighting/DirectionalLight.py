import glm
from lighting.Light import *


class DirectionalLight(Light):
    def __init__(self, name, direction=None):
        super().__init__(name)
        self._name = name
        self.direction = direction if direction else glm.vec3(0.0, 0.0, 0.0)
