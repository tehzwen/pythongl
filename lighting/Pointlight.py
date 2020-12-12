from lighting.Light import *

class Pointlight(Light):
    def __init__(self, name, linear=None, quadratic=None):
        super().__init__(name)
        self._name = name
        self._linear = linear if linear else 0.1
        self._quadratic = quadratic if quadratic else 0.001

    def get_linear(self):
        return self._linear

    def set_linear(self, val):
        self._linear = val
    
    def get_quadratic(self):
        return self._quadratic
    
    def set_quadratic(self, val):
        self._quadratic = val