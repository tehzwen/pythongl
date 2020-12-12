from geometry.Geometry import *
from model.Model import *
from material.Material import *


class Quad(Geometry):
    def __init__(self, name, size, segments, material=None, model=None):
        super().__init__()
        self.create_segmented(size, segments)
        self._type = "quad"
        self._name = name
        self.material = material if material else Material()
        self.model = model if model else Model()

    def create_segmented(self, size, segments):
        vertices = []
        indices = []
        normals = []
        uvs = []
        current_index = 0



        step = size/segments
        x = step
        z = step
        print(step)

        while(x != size):
            while(z != size):
                # 0
                vertices += [z, 0, x]
                # 1
                vertices += [z + step, 0, x]
                # 2
                vertices += [z, 0, x + step]
                # 3
                vertices += [z, 0, x + step]
                # 4
                vertices += [z + step, 0, x]
                # 5
                vertices += [z + step, 0, x + step]

                indices += [
                    0 + current_index,
                    2 + current_index,
                    1 + current_index,
                    3 + current_index,
                    4 + current_index,
                    5 + current_index,
                ]

                current_index += 6
                normals += [
                    0.0, 1.0, 0.0,
                    0.0, 1.0, 0.0,
                    0.0, 1.0, 0.0,
                    0.0, 1.0, 0.0,
                    0.0, 1.0, 0.0,
                    0.0, 1.0, 0.0
                ]

                uvs += [
                    z, x,
                    z + step, x,
                    z, x + step,
                    z, x + step,
                    z + step, x,
                    z + step, x + step
                ]
                z += step
            x += step

        self._vertices = vertices
        self._normals = normals
        self._texture_coords = uvs
        self._indicies = indices

        print(len(self._indicies))
        print(len(self._vertices))

