import noise
import glm
import math
import numpy as np
from geometry.Geometry import *
from model.Model import *
from material.Material import *


class Quad(Geometry):
    def __init__(self, name, size, segments, smooth=False, material=None, model=None):
        super().__init__()
        self.create_segmented(size, segments, smooth)
        self._type = "quad"
        self._name = name
        self.material = material if material else Material()
        self.model = model if model else Model()

    def create_segmented(self, size, segments, smooth):


        vert_dictionary = {}

        # helper function to calculate the normals
        def calculate_normal(a, b, c):
            return glm.cross(b-a, c-a)

        def get_random(z, x):
            # return random.uniform(-random_range, random_range)
            # return 0.1 * np.random.randn()
            # return math.sin(z) * math.sin(x)
            scale = 60
            octaves = 6
            lacunarity = 6 #level of detail for each octave
            persistence = 10 #adjusts amplitude

            # if (z > (0 - (size/4)) and z < (0 + (size/4))):
            #     octaves = 1
            #     scale = 10


            val = noise.pnoise2(z/scale, x/scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=size*2, repeaty=size*2, base=0)
            # return -abs(val * 15)
            return val * 5
            # return 0
            # return 4 - (x * x) - (z * z)

        def add_vert_to_dict(vertex, normal, index):
            if (vertex in vert_dictionary):
                vert_dictionary[vertex]["normals"].append(normal)
                vert_dictionary[vertex]["indices"].append(index)
            else:
                vert_dictionary[vertex] = {
                    "normals": [normal],
                    "indices": [index]
                }

        indices = []
        normals = []
        heights = []
        uvs = []
        current_index = 0
        current_vert = 0

        step = round(size/segments, 3)
        x = -(size)
        z = -(size)

        def add_vert(arr, vert, count):
            try:
                arr[count] = vert[0]
                arr[count + 1] = vert[1]
                arr[count + 2] = vert[2]
                count += 3
            except IndexError as e:
                print(e)
                raise e
            return count

        grid_num = int((size * 2)/step)


        numpy_verts = np.zeros((grid_num * grid_num * 18))
        numpy_norms = np.zeros((grid_num * grid_num * 18))

        row = 0
        while(x < size):
            col = 0

            while(z < size):
                temp_heights = []
                temp_vertices = np.zeros((18))

                if (row == 0):
                    # check for first initial square
                    if (col == 0):
                        for i in range(4):
                            temp_heights.append(get_random(z, x))
                        # 0
                        zero = glm.vec3(z, temp_heights[0], x)
                        current_vert = add_vert(
                            numpy_verts, zero, current_vert)
                        # 1
                        one = glm.vec3(z + step, temp_heights[1], x)
                        current_vert = add_vert(numpy_verts, one, current_vert)
                        # 2
                        two = glm.vec3(z, temp_heights[2], x + step)
                        current_vert = add_vert(
                            numpy_verts, two, current_vert)
                        # 3
                        three = glm.vec3(z, temp_heights[2], x + step)
                        current_vert = add_vert(
                            numpy_verts, three, current_vert)
                        # 4
                        four = glm.vec3(z + step, temp_heights[1], x)
                        current_vert = add_vert(
                            numpy_verts, four, current_vert)
                        # 5
                        five = glm.vec3(z + step, temp_heights[3], x + step)
                        current_vert = add_vert(
                            numpy_verts, five, current_vert)

                        if (smooth):
                            add_vert_to_dict(zero, calculate_normal(
                                zero, two, one), 0 + current_index)

                            add_vert_to_dict(one, calculate_normal(
                                one, zero, two), 1 + current_index)

                            add_vert_to_dict(two, calculate_normal(
                                two, one, zero), 2 + current_index)

                            add_vert_to_dict(three, calculate_normal(
                                three, five, four), 3 + current_index)

                            add_vert_to_dict(four, calculate_normal(
                                four, three, five), 4 + current_index)

                            add_vert_to_dict(five, calculate_normal(
                                five, four, three), 5 + current_index)

                    # not beginning of row
                    else:
                        height_2 = get_random(z, x)
                        height_3 = get_random(z, x)

                        temp_heights.append(heights[col - 1][1])
                        temp_heights.append(height_2)
                        temp_heights.append(heights[col - 1][3])
                        temp_heights.append(height_3)

                        # 0
                        zero = glm.vec3(z, heights[col - 1][1], x)
                        current_vert = add_vert(
                            numpy_verts, zero, current_vert)
                        # 1
                        one = glm.vec3(z + step, height_2, x)
                        current_vert = add_vert(
                            numpy_verts, one, current_vert)
                        # 2
                        two = glm.vec3(z, heights[col - 1][3], x + step)
                        current_vert = add_vert(
                            numpy_verts, two, current_vert)
                        # 3
                        three = glm.vec3(z, heights[col - 1][3], x + step)
                        current_vert = add_vert(
                            numpy_verts, three, current_vert)
                        # 4
                        four = glm.vec3(z + step, height_2, x)
                        current_vert = add_vert(
                            numpy_verts, four, current_vert)
                        # 5
                        five = glm.vec3(z + step, height_3, x + step)
                        current_vert = add_vert(
                            numpy_verts, five, current_vert)

                        if (smooth):
                            add_vert_to_dict(zero, calculate_normal(
                                zero, two, one), 0 + current_index)

                            add_vert_to_dict(one, calculate_normal(
                                one, zero, two), 1 + current_index)

                            add_vert_to_dict(two, calculate_normal(
                                two, one, zero), 2 + current_index)

                            add_vert_to_dict(three, calculate_normal(
                                three, five, four), 3 + current_index)

                            add_vert_to_dict(four, calculate_normal(
                                four, three, five), 4 + current_index)

                            add_vert_to_dict(five, calculate_normal(
                                five, four, three), 5 + current_index)

                else:
                    # check for first col
                    if (col == 0):
                        height_2 = get_random(z, x)
                        height_3 = get_random(z, x)

                        temp_heights.append(
                            heights[(row * grid_num) - grid_num][2])
                        temp_heights.append(
                            heights[(row * grid_num) - grid_num][3])
                        temp_heights.append(height_2)
                        temp_heights.append(height_3)

                        # 0
                        zero = glm.vec3(
                            z, heights[(row * grid_num) - grid_num][2], x)
                        current_vert = add_vert(
                            numpy_verts, zero, current_vert)
                        # 1
                        one = glm.vec3(
                            z + step, heights[(row * grid_num) - grid_num][3], x)
                        current_vert = add_vert(
                            numpy_verts, one, current_vert)
                        # 2
                        two = glm.vec3(z, height_2, x + step)
                        current_vert = add_vert(
                            numpy_verts, two, current_vert)
                        # 3
                        three = glm.vec3(z, height_2, x + step)
                        current_vert = add_vert(
                            numpy_verts, three, current_vert)
                        # 4
                        four = glm.vec3(
                            z + step, heights[(row * grid_num) - grid_num][3], x)
                        current_vert = add_vert(
                            numpy_verts, four, current_vert)
                        # 5
                        five = glm.vec3(z + step, height_3, x + step)
                        current_vert = add_vert(
                            numpy_verts, five, current_vert)

                        if (smooth):
                            add_vert_to_dict(zero, calculate_normal(
                                zero, two, one), 0 + current_index)

                            add_vert_to_dict(one, calculate_normal(
                                one, zero, two), 1 + current_index)

                            add_vert_to_dict(two, calculate_normal(
                                two, one, zero), 2 + current_index)

                            add_vert_to_dict(three, calculate_normal(
                                three, five, four), 3 + current_index)

                            add_vert_to_dict(four, calculate_normal(
                                four, three, five), 4 + current_index)

                            add_vert_to_dict(five, calculate_normal(
                                five, four, three), 5 + current_index)

                    else:
                        height_3 = get_random(z, x)

                        temp_heights.append(
                            heights[(row * grid_num) + col - 1][1])
                        temp_heights.append(
                            heights[((row * grid_num) - grid_num) + col][3])
                        temp_heights.append(
                            heights[(row * grid_num) + col - 1][3])
                        temp_heights.append(height_3)

                        # 0
                        zero = glm.vec3(
                            z, heights[(row * grid_num) + col - 1][1], x)
                        current_vert = add_vert(
                            numpy_verts, zero, current_vert)
                        # 1
                        one = glm.vec3(
                            z + step, heights[((row * grid_num) - grid_num) + col][3], x)
                        current_vert = add_vert(
                            numpy_verts, one, current_vert)
                        # 2
                        two = glm.vec3(
                            z, heights[(row * grid_num) + col - 1][3], x + step)
                        current_vert = add_vert(
                            numpy_verts, two, current_vert)
                        # 3
                        three = glm.vec3(
                            z, heights[(row * grid_num) + col - 1][3], x + step)
                        current_vert = add_vert(
                            numpy_verts, three, current_vert)
                        # 4
                        four = glm.vec3(
                            z + step, heights[((row * grid_num) - grid_num) + col][3], x)
                        current_vert = add_vert(
                            numpy_verts, four, current_vert)
                        # 5
                        five = glm.vec3(z + step, height_3, x + step)
                        current_vert = add_vert(
                            numpy_verts, five, current_vert)

                        if (smooth):
                            add_vert_to_dict(zero, calculate_normal(
                                zero, one, two), 0 + current_index)

                            add_vert_to_dict(one, calculate_normal(
                                one, two, zero), 1 + current_index)

                            add_vert_to_dict(two, calculate_normal(
                                two, one, zero), 2 + current_index)

                            add_vert_to_dict(three, calculate_normal(
                                three, five, four), 3 + current_index)

                            add_vert_to_dict(four, calculate_normal(
                                four, three, five), 4 + current_index)

                            add_vert_to_dict(five, calculate_normal(
                                five, four, three), 5 + current_index)

                indices += [
                    0 + current_index,
                    2 + current_index,
                    1 + current_index,
                    3 + current_index,
                    5 + current_index,
                    4 + current_index,
                ]
                current_index += 6

                if (not smooth):
                    index = current_vert - 18
                    temp_vertices = numpy_verts[index:current_vert].copy()

                    for i in range(0, len(temp_vertices), 9):
                        normal_calc = calculate_normal(
                            glm.vec3(
                                temp_vertices[i], temp_vertices[i + 1], temp_vertices[i + 2]),
                            glm.vec3(
                                temp_vertices[i + 6], temp_vertices[i + 7], temp_vertices[i + 8]),
                            glm.vec3(
                                temp_vertices[i + 3], temp_vertices[i + 4], temp_vertices[i + 5])
                        )

                        normals += normal_calc.to_list()
                        normals += normal_calc.to_list()
                        normals += normal_calc.to_list()
                uvs += [
                    z, x,
                    z + step, x,
                    z, x + step,
                    z, x + step,
                    z + step, x,
                    z + step, x + step
                ]
                z += step
                z = round(z, 3)
                heights.append(temp_heights)
                col += 1

            row += 1
            z = -(size)
            x += step
            x = round(x, 3)

        if (smooth):
            for key in vert_dictionary:
                temp_normal = glm.vec3(0, 0, 0)
                for norm in vert_dictionary[key]["normals"]:
                    temp_normal += norm

                temp_normal = glm.normalize(temp_normal)

                for index in vert_dictionary[key]["indices"]:
                    actual_index = index * 3
                    numpy_norms[actual_index] = temp_normal[0]
                    numpy_norms[actual_index + 1] = temp_normal[1]
                    numpy_norms[actual_index + 2] = temp_normal[2]

        self._vertices = numpy_verts
        self._normals = normals if not smooth else numpy_norms
        self._texture_coords = uvs
        self._indicies = indices
