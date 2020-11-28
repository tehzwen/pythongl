from geometry.Geometry import Geometry


class Triangle(Geometry):
    def __init__(self):
        super().__init__()
        self._vertices = [
            -0.5, -0.5, 0,
            0.5, -0.5, 0,
            0,  0.5, 0
        ]
        self._indicies = [0, 1, 2]
        self._type = "triangle"
