from geometry.Geometry import Geometry
from model.Model import *
from material.Material import *


class Line(Geometry):
    def __init__(self, name, point_1, point_2, material=None, model=None):
        super().__init__()
        self._vertices = [
            point_1[0],
            point_1[1],
            point_1[2],
            point_2[0],
            point_2[1],
            point_2[2],
        ]
        self._type = "line"
        self._name = name
        self.material = material if material else Material()
        self.model = model if model else Model()


    def setup(self):
        self.create_vao()
        self.bind_vao()
        self.calculate_centroid()
        self.create_vertex_buffer()
        self.unbind_vao()