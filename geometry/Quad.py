from PIL.Image import new
import noise
import glm
import math
import numpy as np
from mymath.Utilities import *
from geometry.Geometry import *
from model.Model import *
from material.Material import *


class Quad(Geometry):
    def __init__(self, name, size, segments, smooth=False, dynamic=False, material=None, model=None):
        super().__init__(dynamic=dynamic)
        self.size = size
        self.create_segmented(size, segments, smooth)
        self._type = "quad"
        self._name = name
        self.material = material if material else Material()
        self.model = model if model else Model()
        self.draw_mode = gl.GL_DYNAMIC_DRAW if dynamic else gl.GL_STATIC_DRAW

    def alter_heights(self, function):
        keys_to_delete = []
        keys_to_add = []

        for key in self.vert_dictionary:
            temp_vert = key
            keys_to_delete.append(temp_vert)
            new_vert = glm.vec3(key[0], function(), key[2])
            temp_key_value = {"key": new_vert, "values": {"normals": [],
                                                          "indices": self.vert_dictionary[key]["indices"]}}

            temp_normal = glm.vec3(0, 0, 0)
            for norm in self.vert_dictionary[key]["normals"]:
                changed_normal = glm.vec3(
                    norm[0], norm[1] + new_vert[1], norm[2])
                temp_key_value["values"]["normals"].append(changed_normal)
                temp_normal += changed_normal
            temp_normal = glm.normalize(temp_normal)

            for index in self.vert_dictionary[key]["indices"]:
                actual_index = index * 3
                self._vertices[actual_index] = new_vert[0]
                self._vertices[actual_index + 1] = new_vert[1]
                self._vertices[actual_index + 2] = new_vert[2]

                self._normals[actual_index] = temp_normal[0]
                self._normals[actual_index + 1] = temp_normal[1]
                self._normals[actual_index + 2] = temp_normal[2]

            keys_to_add.append(temp_key_value)

        for key in keys_to_add:
            self.vert_dictionary[key["key"]] = {
                "normals": key["values"]["normals"], "indices": key["values"]["indices"]}

        for key in keys_to_delete:
            del self.vert_dictionary[key]

        self.update_buffers()

    def create_segmented(self, size, segments, smooth):
        vert_dictionary = {}
        
        # helper function to calculate the normals
        def calculate_normal(a, b, c):
            return glm.cross(b-a, c-a)

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
        current_uv = 0

        step = round(size/segments, 3)
        z = -(size)
        x = -(size)

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
        while(z < size):
            col = 0

            while(x < size):
                temp_heights = []
                temp_vertices = np.zeros((18))

                if (row == 0):
                    # check for first initial square
                    if (col == 0):
                        for i in range(4):
                            temp_heights.append(get_pnoise(x, z, size=self.size))
                        # 0
                        zero = glm.vec3(x, temp_heights[0], z)
                        current_vert = add_vert(
                            numpy_verts, zero, current_vert)
                        # 1
                        one = glm.vec3(x + step, temp_heights[1], z)
                        current_vert = add_vert(numpy_verts, one, current_vert)
                        # 2
                        two = glm.vec3(x, temp_heights[2], z + step)
                        current_vert = add_vert(
                            numpy_verts, two, current_vert)
                        # 3
                        three = glm.vec3(x, temp_heights[2], z + step)
                        current_vert = add_vert(
                            numpy_verts, three, current_vert)
                        # 4
                        four = glm.vec3(x + step, temp_heights[1], z)
                        current_vert = add_vert(
                            numpy_verts, four, current_vert)
                        # 5
                        five = glm.vec3(x + step, temp_heights[3], z + step)
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
                        height_2 = get_pnoise(x, z, size=self.size)
                        height_3 = get_pnoise(x, z, size=self.size)

                        temp_heights.append(heights[col - 1][1])
                        temp_heights.append(height_2)
                        temp_heights.append(heights[col - 1][3])
                        temp_heights.append(height_3)

                        # 0
                        zero = glm.vec3(x, heights[col - 1][1], z)
                        current_vert = add_vert(
                            numpy_verts, zero, current_vert)
                        # 1
                        one = glm.vec3(x + step, height_2, z)
                        current_vert = add_vert(
                            numpy_verts, one, current_vert)
                        # 2
                        two = glm.vec3(x, heights[col - 1][3], z + step)
                        current_vert = add_vert(
                            numpy_verts, two, current_vert)
                        # 3
                        three = glm.vec3(x, heights[col - 1][3], z + step)
                        current_vert = add_vert(
                            numpy_verts, three, current_vert)
                        # 4
                        four = glm.vec3(x + step, height_2, z)
                        current_vert = add_vert(
                            numpy_verts, four, current_vert)
                        # 5
                        five = glm.vec3(x + step, height_3, z + step)
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
                        height_2 = get_pnoise(x, z, size=self.size)
                        height_3 = get_pnoise(x, z, size=self.size)

                        temp_heights.append(
                            heights[(row * grid_num) - grid_num][2])
                        temp_heights.append(
                            heights[(row * grid_num) - grid_num][3])
                        temp_heights.append(height_2)
                        temp_heights.append(height_3)

                        # 0
                        zero = glm.vec3(
                            x, heights[(row * grid_num) - grid_num][2], z)
                        current_vert = add_vert(
                            numpy_verts, zero, current_vert)
                        # 1
                        one = glm.vec3(
                            x + step, heights[(row * grid_num) - grid_num][3], z)
                        current_vert = add_vert(
                            numpy_verts, one, current_vert)
                        # 2
                        two = glm.vec3(x, height_2, z + step)
                        current_vert = add_vert(
                            numpy_verts, two, current_vert)
                        # 3
                        three = glm.vec3(x, height_2, z + step)
                        current_vert = add_vert(
                            numpy_verts, three, current_vert)
                        # 4
                        four = glm.vec3(
                            x + step, heights[(row * grid_num) - grid_num][3], z)
                        current_vert = add_vert(
                            numpy_verts, four, current_vert)
                        # 5
                        five = glm.vec3(x + step, height_3, z + step)
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
                        height_3 = get_pnoise(x, z, size=self.size)

                        temp_heights.append(
                            heights[(row * grid_num) + col - 1][1])
                        temp_heights.append(
                            heights[((row * grid_num) - grid_num) + col][3])
                        temp_heights.append(
                            heights[(row * grid_num) + col - 1][3])
                        temp_heights.append(height_3)

                        # 0
                        zero = glm.vec3(
                            x, heights[(row * grid_num) + col - 1][1], z)
                        current_vert = add_vert(
                            numpy_verts, zero, current_vert)
                        # 1
                        one = glm.vec3(
                            x + step, heights[((row * grid_num) - grid_num) + col][3], z)
                        current_vert = add_vert(
                            numpy_verts, one, current_vert)
                        # 2
                        two = glm.vec3(
                            x, heights[(row * grid_num) + col - 1][3], z + step)
                        current_vert = add_vert(
                            numpy_verts, two, current_vert)
                        # 3
                        three = glm.vec3(
                            x, heights[(row * grid_num) + col - 1][3], z + step)
                        current_vert = add_vert(
                            numpy_verts, three, current_vert)
                        # 4
                        four = glm.vec3(
                            x + step, heights[((row * grid_num) - grid_num) + col][3], z)
                        current_vert = add_vert(
                            numpy_verts, four, current_vert)
                        # 5
                        five = glm.vec3(x + step, height_3, z + step)
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
                # uvs += [
                #     current_uv, current_uv,
                #     current_uv + step, current_uv,
                #     current_uv, current_uv + step,
                #     current_uv, current_uv + step,
                #     current_uv + step, current_uv,
                #     current_uv + step, current_uv + step
                # ]
                uvs += [
                    0.0, 0.0,
                    0.5, 0.0,
                    0.0, 0.5,
                    0.0, 0.5,
                    0.5, 0.0,
                    0.5, 0.5
                ]
                current_uv += step
                x += step
                x = round(x, 3)
                heights.append(temp_heights)
                col += 1

            row += 1
            x = -(size)
            z += step
            z = round(z, 3)

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

        self.vert_dictionary = vert_dictionary
        self._vertices = numpy_verts
        self._normals = normals if not smooth else numpy_norms
        self._texture_coords = uvs
        self._indicies = indices
