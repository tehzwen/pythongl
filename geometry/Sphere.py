import numpy as np
import math
import glm

from numpy.lib.function_base import angle
from geometry.Geometry import Geometry
from model.Model import *
from material.Material import *


class Sphere(Geometry):
    def __init__(self, name, horiz_segments, vert_segments, radius, material=None, model=None):
        super().__init__()

        self._type = "sphere"
        self.generate_self(horiz_segments, vert_segments, radius)
        self._name = name
        self.material = material if material else Material()
        self.model = model if model else Model()

    def generate_flat_norms(self):

        def calculate_normal(a, b, c):
            return glm.cross(b-a, c-a)

        numpy_norms = np.zeros((len(self._vertices)))
        for i in range(0, len(self._indicies), 3):
            # print(self._indicies[i], self._indicies[i + 1], self._indicies[i + 2])
            # print(self._vertices[self._indicies[i]], self._vertices[self._indicies[i] + 1], self._vertices[self._indicies[i] + 2])
            # print(self._vertices[self._indicies[i + 1]], self._vertices[self._indicies[i + 1] + 1], self._vertices[self._indicies[i + 1] + 2])
            # print(self._vertices[self._indicies[i + 2]], self._vertices[self._indicies[i + 2] + 1], self._vertices[self._indicies[i + 2] + 2])

            normal_calc = calculate_normal(
                glm.vec3(self._vertices[self._indicies[i]],
                         self._vertices[self._indicies[i] + 1], self._vertices[self._indicies[i] + 2]),
                glm.vec3(self._vertices[self._indicies[i + 1]],
                         self._vertices[self._indicies[i + 1] + 1], self._vertices[self._indicies[i + 1] + 2]),
                glm.vec3(self._vertices[self._indicies[i + 2]],
                         self._vertices[self._indicies[i + 2] + 1], self._vertices[self._indicies[i + 2] + 2])
            )

            numpy_norms[self._indicies[i]] = normal_calc[0]
            numpy_norms[self._indicies[i] + 1] = normal_calc[1]
            numpy_norms[self._indicies[i] + 2] = normal_calc[2]

            numpy_norms[self._indicies[i + 1]] = normal_calc[0]
            numpy_norms[self._indicies[i + 1] + 1] = normal_calc[1]
            numpy_norms[self._indicies[i + 1] + 2] = normal_calc[2]

            numpy_norms[self._indicies[i + 2]] = normal_calc[0]
            numpy_norms[self._indicies[i + 2] + 1] = normal_calc[1]
            numpy_norms[self._indicies[i + 2] + 2] = normal_calc[2]

        self._normals = numpy_norms

    def generate_self(self, horiz_segments, vert_segments, radius):
        sector_count = vert_segments
        stack_count = horiz_segments

        x = 0
        y = 0
        z = 0
        xy = 0
        length_inv = 1.0 / radius
        nx = 1.0 / radius
        ny = 1.0 / radius
        nz = 1.0 / radius

        k1 = 0
        k2 = 0

        sector_step = 2 * math.pi / sector_count
        stack_step = math.pi / stack_count
        sector_angle = 0.0
        stack_angle = 0.0

        i = 0
        j = 0

        for i in range(stack_count + 1):
            stack_angle = math.pi / 2 - i * stack_step
            xy = radius * math.cos(stack_angle)
            z = radius * math.sin(stack_angle)

            k1 = i * (sector_count + 1)
            k2 = k1 + sector_count + 1

            for j in range(sector_count + 1):
                sector_angle = j * sector_step

                x = xy * math.cos(sector_angle)
                y = xy * math.sin(sector_angle)
                self._vertices += [x, y, z]

                nx = x * length_inv
                ny = y * length_inv
                nz = z * length_inv

                self._normals += [nx, ny, nz]

                s = j / sector_count
                t = i / stack_count
                self._texture_coords += [s, t]

                if (i != 0):
                    self._indicies += [k1, k2, k1 + 1]

                if (i != (stack_count - 1)):
                    self._indicies += [k1 + 1, k2, k2 + 1]

                k1 += 1
                k2 += 1

        print(len(self._indicies))
        print(len(self._vertices))

        # self.generate_flat_norms()
