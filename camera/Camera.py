import glm


class Camera():
    def __init__(self, position=None, up=None, center=None):
        self.position = position if position else glm.vec3()
        self.up = up if up else glm.vec3(0.0, 1.0, 0.0)
        self.center = center if center else glm.vec3()