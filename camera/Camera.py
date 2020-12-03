import glm


class Camera():
    def __init__(self, name, position=None, up=None, center=None):
        self._name = name
        self._position = position if position else glm.vec3()
        self._up = up if up else glm.vec3(0.0, 1.0, 0.0)
        self._center = center if center else glm.vec3()
        self._input = {"move": False, "x": 0.0, "y": 0.0}

    def get_position(self):
        return self._position

    def get_up(self):
        return self._up

    def get_center(self):
        return self._center

    def set_position(self, position):
        self._position = position

    def set_up(self, up):
        self._up = up

    def set_center(self, center):
        self._center = center

    def get_name(self):
        return self._name
