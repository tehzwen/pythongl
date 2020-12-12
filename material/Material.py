import glm
import numpy
from PIL import Image
from OpenGL import GL as gl


class Material():
    def __init__(self, ambient=None, diffuse=None, specular=None, shader_type=None, alpha=None, nVal=None, diffuseTexture=None):
        self.ambient = ambient if ambient else glm.vec3(0.1, 0.1, 0.1)
        self.diffuse = diffuse if diffuse else glm.vec3(0.5, 0.5, 0.5)
        self.specular = specular if specular else glm.vec3(0.2, 0.2, 0.2)
        self.shader_type = shader_type if shader_type else 1
        self.alpha = alpha if alpha else 1.0
        self.n = nVal if nVal else 1.0
        self.diffuseTextureFile = diffuseTexture
        self.diffuseTexture = self.load_texture(
            self.diffuseTextureFile) if diffuseTexture else None

    def __repr__(self):
        return (
            f'''Ambient:        {str(self.ambient)}
Diffuse:        {str(self.diffuse)}
Specular:       {str(self.specular)}
ShaderType:     {str(self.shader_type)}
Alpha:          {str(self.alpha)}
Shininess:      {str(self.n)}
DiffuseTexture: {str(self.diffuseTextureFile)}'''
        )

    def set_diffuse_texture(self, filename):
        self.diffuseTextureFile = filename
        self.diffuseTexture = self.load_texture(filename)

    def load_texture(self, filename=None):
        try:
            image = Image.open(filename)
        except IOError as ex:
            print('IOError: failed to open ' + filename)

        image = image.convert('RGBA')

        imageData = numpy.array(image.getdata(), numpy.uint8)
        textureID = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, textureID)

        # gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
        # gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_R, gl.GL_CLAMP)
        # gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP)

        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, image.size[0], image.size[1],
                        0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, imageData)
        # gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_NEAREST)
        gl.glTexParameterf(
            gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameterf(
            gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        image.close()
        return textureID
