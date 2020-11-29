import glm
from lighting.Light import *

class Pointlight(Light):
    def __init__(self, name):
        super().__init__(name)
        self._name = name