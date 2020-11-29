import glm


class Model():
    def __init__(self, scale=None, position=None, rotation=None):
        self._position = position if position else glm.vec3(0.0, 0.0, 0.0)
        self._scale = scale if scale else glm.vec3(1.0, 1.0, 1.0)
        self._rotation = rotation if rotation else glm.mat4()
        self._matrix = glm.mat4()

    def translate(self, trans_vector):
        self._position += trans_vector

    def rotate(self, rot_vector, angle):
        self._rotation = glm.rotate(self._rotation, glm.radians(angle), rot_vector)
    
    def scale(self, scale_vector):
        self._scale *= scale_vector

    def get_scale(self):
        return self._scale

    def get_rotation(self):
        return self._rotation
    
    def get_position(self):
        return self._position

    def get_matrix(self):
        return self._matrix
    
    def set_matrix(self, mat):
        self._matrix = mat
