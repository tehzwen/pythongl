import random
import glm
import math
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

        # helper function to calculate the normals
        def calculate_normal(a, b, c):
            return glm.cross(b - a, c - a).to_list()

        random_range = 1.0
        vertices = []
        indices = []
        normals = []
        heights = []

        uvs = []
        current_index = 0

        step = size/segments
        x = -(size)
        z = -(size)

        grid_num = int((size * 2)/step)

        row = 0
        while(x < size):
            col = 0

            while(z < size):
                temp_heights = []
                temp_vertices = []

                if (row == 0):
                    # check for first initial square
                    if (col == 0):
                        for i in range(4):
                            val = random.uniform(-random_range, random_range)
                            temp_heights.append(val)
                        # 0
                        # vertices += [z, temp_heights[0], x]
                        temp_vertices.append(z)
                        temp_vertices.append(temp_heights[0])
                        temp_vertices.append(x)
                        # 1
                        # vertices += [z + step,
                        #              temp_heights[1], x]

                        temp_vertices.append(z + step)
                        temp_vertices.append(temp_heights[1])
                        temp_vertices.append(x)
                        # 2
                        # vertices += [z, temp_heights[2], x + step]

                        temp_vertices.append(z)
                        temp_vertices.append(temp_heights[2])
                        temp_vertices.append(x + step)
                        # 3
                        # vertices += [z, temp_heights[2], x + step]
                        temp_vertices.append(z)
                        temp_vertices.append(temp_heights[2])
                        temp_vertices.append(x + step)

                        # 4
                        # vertices += [z + step,
                        #              temp_heights[1], x]

                        temp_vertices.append(z + step)
                        temp_vertices.append(temp_heights[1])
                        temp_vertices.append(x)
                        # # 5
                        # vertices += [z + step,
                        #              temp_heights[3], x + step]

                        temp_vertices.append(z + step)
                        temp_vertices.append(temp_heights[3])
                        temp_vertices.append(x + step)

                    # not at the end of a row
                    else:
                        height_2 = random.uniform(-random_range, random_range)
                        height_3 = random.uniform(-random_range, random_range)

                        temp_heights.append(heights[col - 1][1])
                        temp_heights.append(height_2)
                        temp_heights.append(heights[col - 1][3])
                        temp_heights.append(height_3)

                        # 0
                        # vertices += [z, heights[col - 1][1], x]
                        temp_vertices.append(z)
                        temp_vertices.append(heights[col - 1][1])
                        temp_vertices.append(x)
                        # 1
                        # vertices += [z + step, height_2, x]
                        temp_vertices.append(z + step)
                        temp_vertices.append(height_2)
                        temp_vertices.append(x)
                        # 2
                        # vertices += [z, heights[col - 1][3], x + step]
                        temp_vertices.append(z)
                        temp_vertices.append(heights[col - 1][3])
                        temp_vertices.append(x + step)
                        # 3
                        # vertices += [z, heights[col - 1][3], x + step]
                        temp_vertices.append(z)
                        temp_vertices.append(heights[col - 1][3])
                        temp_vertices.append(x + step)
                        # 4
                        # vertices += [z + step, height_2, x]
                        temp_vertices.append(z + step)
                        temp_vertices.append(height_2)
                        temp_vertices.append(x)
                        # 5
                        # vertices += [z + step, height_3, x + step]
                        temp_vertices.append(z + step)
                        temp_vertices.append(height_3)
                        temp_vertices.append(x + step)

                else:

                    # check for first col

                    if (col == 0):
                        height_2 = random.uniform(-random_range, random_range)
                        height_3 = random.uniform(-random_range, random_range)

                        temp_heights.append(
                            heights[(row * grid_num) - grid_num][2])
                        temp_heights.append(
                            heights[(row * grid_num) - grid_num][3])
                        temp_heights.append(height_2)
                        temp_heights.append(height_3)

                        # 0
                        # vertices += [z,
                        #              heights[(row * grid_num) - grid_num][2], x]

                        temp_vertices.append(z)
                        temp_vertices.append(
                            heights[(row * grid_num) - grid_num][2])
                        temp_vertices.append(x)
                        # 1
                        # vertices += [z + step,
                        #              heights[(row * grid_num) - grid_num][3], x]

                        temp_vertices.append(z + step)
                        temp_vertices.append(
                            heights[(row * grid_num) - grid_num][3])
                        temp_vertices.append(x)
                        # 2
                        # vertices += [z, height_2, x + step]

                        temp_vertices.append(z)
                        temp_vertices.append(height_2)
                        temp_vertices.append(x + step)
                        # 3
                        # vertices += [z, height_2, x + step]

                        temp_vertices.append(z)
                        temp_vertices.append(height_2)
                        temp_vertices.append(x + step)
                        # 4
                        # vertices += [z + step,
                        #              heights[(row * grid_num) - grid_num][3], x]

                        temp_vertices.append(z + step)
                        temp_vertices.append(
                            heights[(row * grid_num) - grid_num][3])
                        temp_vertices.append(x)
                        # 5
                        # vertices += [z + step, height_3, x + step]

                        temp_vertices.append(z + step)
                        temp_vertices.append(height_3)
                        temp_vertices.append(x + step)

                    else:
                        height_3 = random.uniform(-random_range, random_range)

                        temp_heights.append(
                            heights[(row * grid_num) + col - 1][1])
                        temp_heights.append(
                            heights[((row * grid_num) - grid_num) + col][3])
                        temp_heights.append(
                            heights[(row * grid_num) + col - 1][3])
                        temp_heights.append(height_3)

                        # 0
                        # vertices += [z,
                        #              heights[(row * grid_num) + col - 1][1], x]

                        temp_vertices.append(z)
                        temp_vertices.append(
                            heights[(row * grid_num) + col - 1][1])
                        temp_vertices.append(x)
                        # 1
                        # vertices += [z + step,
                        #              heights[((row * grid_num) - grid_num) + col][3], x]

                        temp_vertices.append(z + step)
                        temp_vertices.append(
                            heights[((row * grid_num) - grid_num) + col][3])
                        temp_vertices.append(x)
                        # 2
                        # vertices += [z,
                        #              heights[(row * grid_num) + col - 1][3], x + step]

                        temp_vertices.append(z)
                        temp_vertices.append(
                            heights[(row * grid_num) + col - 1][3])
                        temp_vertices.append(x + step)
                        # 3
                        # vertices += [z,
                        #              heights[(row * grid_num) + col - 1][3], x + step]

                        temp_vertices.append(z)
                        temp_vertices.append(
                            heights[(row * grid_num) + col - 1][3])
                        temp_vertices.append(x + step)
                        # 4
                        # vertices += [z + step,
                        #              heights[((row * grid_num) - grid_num) + col][3], x]

                        temp_vertices.append(z + step)
                        temp_vertices.append(
                            heights[((row * grid_num) - grid_num) + col][3])
                        temp_vertices.append(x)
                        # 5
                        # vertices += [z + step, height_3, x + step]

                        temp_vertices.append(z + step)
                        temp_vertices.append(height_3)
                        temp_vertices.append(x + step)

                indices += [
                    0 + current_index,
                    2 + current_index,
                    1 + current_index,
                    3 + current_index,
                    4 + current_index,
                    5 + current_index,
                ]

                current_index += 6

                # print(len(temp_vertices))

                for i in range(0, len(temp_vertices), 9):
                    normal_calc = calculate_normal(
                        glm.vec3(
                            temp_vertices[i], temp_vertices[i + 1], temp_vertices[i + 2]),
                        glm.vec3(
                            temp_vertices[i + 6], temp_vertices[i + 7], temp_vertices[i + 8]),
                        glm.vec3(
                            temp_vertices[i + 3], temp_vertices[i + 4], temp_vertices[i + 5])
                    )
                    normals += normal_calc
                    normals += normal_calc
                    normals += normal_calc

                uvs += [
                    z, x,
                    z + step, x,
                    z, x + step,
                    z, x + step,
                    z + step, x,
                    z + step, x + step
                ]
                z += step
                vertices += temp_vertices
                heights.append(temp_heights)
                col += 1

            row += 1
            z = -(size)
            x += step

        self._vertices = vertices
        self._normals = normals
        self._texture_coords = uvs
        self._indicies = indices
