from geometry.Line import *


class Axis():
    def __init__(self):
        self.x_line = Line("x-line", glm.vec3(0.0, 0.0, 0.0), glm.vec3(
            3.0, 0.0, 0.0), material=Material(diffuse=glm.vec3(1.0, 0.0, 0.0)))
        self.y_line = Line("y-line", glm.vec3(0.0, 0.0, 0.0), glm.vec3(
            0.0, 3.0, 0.0), material=Material(diffuse=glm.vec3(0.0, 1.0, 0.0)))
        self.z_line = Line("z-line", glm.vec3(0.0, 0.0, 0.0), glm.vec3(
            0.0, 0.0, 3.0), material=Material(diffuse=glm.vec3(0.0, 0.0, 1.0)))
        shader_name = "flatShader"

        self.x_line.shader.load_frag_source(
            file_name=shader_name)
        self.x_line.shader.load_vert_source(
            file_name=shader_name)
        self.x_line.shader.init()
        self.x_line.setup()

        self.y_line.shader.load_frag_source(
            file_name=shader_name)
        self.y_line.shader.load_vert_source(
            file_name=shader_name)
        self.y_line.shader.init()
        self.y_line.setup()

        self.z_line.shader.load_frag_source(
            file_name=shader_name)
        self.z_line.shader.load_vert_source(
            file_name=shader_name)
        self.z_line.shader.init()
        self.z_line.setup()

        self.lines = [self.x_line, self.y_line, self.z_line]

    def get_lines(self):
        return self.lines

    def set_position(self, position):
        for i in range(len(self.lines)):
            self.lines[i].model.set_position(position)
