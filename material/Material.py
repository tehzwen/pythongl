import glm


class Material():
    def __init__(self, ambient=None, diffuse=None, specular=None, shader_type=None, alpha=None):
        self.diffuse = diffuse if diffuse else glm.vec3(0.5, 0.5, 0.5)
        self.ambient = ambient if ambient else glm.vec3(0.1, 0.1, 0.1)
        self.specular = specular if specular else glm.vec3(0.2, 0.2, 0.2)
        self.shader_type = shader_type if shader_type else 1
        self.alpha = alpha if alpha else 1.0
