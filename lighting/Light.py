import glm

class Light():
    def __init__(self, name):
        self._position = glm.vec3()
        self._color = glm.vec3(1.0, 1.0, 1.0)
        self._strength = 1.0
        self._name = name

    def set_position(self, position):
        self._position = position

    def get_position(self):
        return self._position

    def set_color(self, color):
        self._color = color

    def get_color(self):
        return self._color

    def set_strength(self, val):
        self._strength = val

    def get_strength(self):
        return self._strength

    def get_name(self):
        return self._name