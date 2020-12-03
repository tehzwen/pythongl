from geometry.Geometry import *
from model.Model import *
from material.Material import *


class Quad(Geometry):
    def __init__(self, name,  material=None, model=None):
        super().__init__()
        self._vertices = [
            0.0, 0.5, 0.5,
            0.0, 0.5, 0.0,
            0.5, 0.5, 0.0,
            0.5, 0.5, 0.5,
        ]
        self._indicies = [
            0, 2, 1, 2, 0, 3,
        ]
        self._normals = [
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
        ]
        self._texture_coords = [
            0.0, 0.0,
            5.0, 0.0,
            5.0, 5.0,
            0.0, 5.0,
        ]
        self._type = "quad"
        self._name = name
        self.material = material if material else Material()
        self.model = model if model else Model()
