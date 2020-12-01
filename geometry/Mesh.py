import glm
import pyassimp
import itertools
from geometry.Geometry import *
from model.Model import *


class Mesh():
    def __init__(self, name, shaderName=None):
        self._name = name
        self._children = []
        self._shader_name = shaderName if shaderName else "basicShader"
        self.model = Model()

    def get_name(self):
        return self._name

    def get_children(self):
        return self._children

    def update_model(self, model):
        self.model = model
        for child in self._children:
            child.model = model

    def scale(self, scale_vec):
        self.model.scale(scale_vec)
        for child in self._children:
            child.model.scale(scale_vec)

    def rotate(self, rot_vec, angle):
        self.model.rotate(rot_vec, angle)
        for child in self._children:
            child.model.rotate(rot_vec, angle)

    def translate(self, trans_vec):
        self.model.translate(trans_vec)
        for child in self._children:
            child.model.translate(trans_vec)

    def load_model(self, filename=None):
        flatten = itertools.chain.from_iterable
        # model_details = pyassimp.load("./res/models/" + filename)
        with pyassimp.load("./res/models/" + filename) as model_details:
            count = 0
            for detail in model_details.meshes:
                tempChild = MeshChild(self.get_name() + str(count), list(flatten(
                    detail.vertices)), detail.normals, list(flatten(list(flatten(detail.texturecoords)))), list(flatten(detail.faces)), detail.material)
                tempChild.shader.load_vert_source(
                    self._shader_name + ".vert.glsl")
                tempChild.shader.load_frag_source(
                    self._shader_name + ".frag.glsl")
                tempChild.shader.init()
                tempChild.setup()
                tempChild.model = self.model
                self._children.append(tempChild)
                count += 1


class MeshChild(Geometry):
    def __init__(self, name, vertices, normals, texture_coords, faces, material):
        super().__init__()
        self._name = name
        self._vertices = vertices
        self._normals = normals
        self._texture_coords = texture_coords
        self._indicies = faces
        for prop in material.properties.items():
            print(prop)
