from geometry.Geometry import Geometry
from model.Model import *
from material.Material import *


class Cube(Geometry):
    def __init__(self, name,  material=None, model=None):
        super().__init__()
        self._vertices = [
            0.0, 0.0, 0.0,
            0.0, 0.5, 0.0,
            0.5, 0.5, 0.0,
            0.5, 0.0, 0.0,

            0.0, 0.0, 0.5,
            0.0, 0.5, 0.5,
            0.5, 0.5, 0.5,
            0.5, 0.0, 0.5,

            0.0, 0.5, 0.5,
            0.0, 0.5, 0.0,
            0.5, 0.5, 0.0,
            0.5, 0.5, 0.5,

            0.0, 0.0, 0.5,
            0.5, 0.0, 0.5,
            0.5, 0.0, 0.0,
            0.0, 0.0, 0.0,

            0.5, 0.0, 0.5,
            0.5, 0.0, 0.0,
            0.5, 0.5, 0.5,
            0.5, 0.5, 0.0,

            0.0, 0.0, 0.5,
            0.0, 0.0, 0.0,
            0.0, 0.5, 0.5,
            0.0, 0.5, 0.0
        ]
        self._indicies = [
            2, 0, 1, 3, 0, 2,
            5, 4, 6, 6, 4, 7,
            10, 9, 8, 10, 8, 11,
            13, 12, 14, 14, 12, 15,
            18, 16, 17, 18, 17, 19,
            22, 21, 20, 23, 21, 22,
        ]
        self._normals = [
            0.0, 0.0, -1.0,
            0.0, 0.0, -1.0,
            0.0, 0.0, -1.0,
            0.0, 0.0, -1.0,

            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,

            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,

            0.0, -1.0, 0.0,
            0.0, -1.0, 0.0,
            0.0, -1.0, 0.0,
            0.0, -1.0, 0.0,

            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,

            -1.0, 0.0, 0.0,
            -1.0, 0.0, 0.0,
            -1.0, 0.0, 0.0,
            -1.0, 0.0, 0.0
        ]
        self._texture_coords = [
            0.0, 0.0,
            1.0, 0.0,
            1.0, 1.0,
            0.0, 1.0,

            0.0, 0.0,
            1.0, 0.0,
            1.0, 1.0,
            0.0, 1.0,

            0.0, 0.0,
            1.0, 0.0,
            1.0, 1.0,
            0.0, 1.0,

            0.0, 0.0,
            1.0, 0.0,
            1.0, 1.0,
            0.0, 1.0,

            0.0, 0.0,
            1.0, 0.0,
            1.0, 1.0,
            0.0, 1.0,

            0.0, 0.0,
            1.0, 0.0,
            1.0, 1.0,
            0.0, 1.0
        ]
        self._type = "cube"
        self._name = name
        self.material = material if material else Material()
        self.model = model if model else Model()
