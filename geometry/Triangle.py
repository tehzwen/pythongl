from geometry.Geometry import Geometry
from model.Model import *
from material.Material import *


class Triangle(Geometry):
    def __init__(self, name,  material=None, model=None):
        super().__init__()
        self._vertices = [
            -0.5, -0.5, 0,
            0.5, -0.5, 0,
            0,  0.5, 0
        ]
        self._indicies = [0, 1, 2]
        self._type = "triangle"
        self._name = name
        self.material = material if material else Material()
        self.model = model if model else Model()
