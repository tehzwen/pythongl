import glm


class Model():
    def __init__(self, scale=None, position=None, rotation=None):
        self.position = position if position else glm.vec3(0.0, 0.0, 0.0)
        self.scale = scale if scale else glm.vec3(1.0, 1.0, 1.0)
        self.rotation = rotation if rotation else glm.mat4()
