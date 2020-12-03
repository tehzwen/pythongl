import pyassimp
import itertools
import json
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
            child.scale(scale_vec)

    def calc_model_matrix(self):
        model_matrix = glm.mat4()
        model_matrix = glm.translate(model_matrix, self.model.get_position())
        model_matrix = glm.translate(model_matrix, self.centroid)
        model_matrix *= self.model.get_rotation()
        model_matrix = glm.scale(model_matrix, self.model.get_scale())
        model_matrix = glm.translate(model_matrix, -(self.centroid))
        self.model.set_matrix(model_matrix)

    def get_worldspace_centroid(self):
        temp = glm.vec4(self.centroid[0], self.centroid[1], self.centroid[2], 1.0)
        temp *= self.model.get_matrix()
        return glm.vec3(temp[0], temp[1], temp[2])
        

    def rotate(self, rot_vec, angle):
        self.model.rotate(rot_vec, angle)
        for child in self._children:
            child.model.rotate(rot_vec, angle)

    def translate(self, trans_vec):
        self.model.translate(trans_vec)
        for child in self._children:
            child.model.translate(trans_vec)

    def calculate_centroid(self, verts):
        center = glm.vec3()
        for i in range(0, len(verts), 3):
            center += glm.vec3(verts[i], verts[i + 1], verts[i + 2])

        center *= 1/(len(verts)/3)
        return center

    def load_model(self, filename=None):
        flatten = itertools.chain.from_iterable
        try:
            with pyassimp.load("./res/models/" + filename) as model_details:
                count = 0
                total_verts = []
                for detail in model_details.meshes:
                    tempChild = MeshChild(self.get_name() + str(count), list(flatten(
                        detail.vertices)), list(flatten(detail.normals)), list(flatten(list(flatten(detail.texturecoords)))), list(flatten(detail.faces)), detail.material)
                    tempChild.shader.load_vert_source(
                        self._shader_name + ".vert.glsl")
                    tempChild.shader.load_frag_source(
                        self._shader_name + ".frag.glsl")
                    tempChild.shader.init()
                    tempChild.model = self.model
                    self._children.append(tempChild)
                    total_verts += list(flatten(detail.vertices))
                    count += 1

                centroid = self.calculate_centroid(total_verts)
                self.centroid = centroid
                self.calc_model_matrix()
                # TODO add model matrix to parent so we can use centroid for calcs later on
                for child in self._children:
                    child.set_centroid(centroid)
                    child.setup()

        except Exception as e:
            print(e)


class MeshChild(Geometry):
    def __init__(self, name, vertices, normals, texture_coords, faces, material):
        super().__init__()
        self._name = name
        self._vertices = vertices
        self._normals = normals
        self._texture_coords = texture_coords
        self._indicies = faces
        material_properties = vars(material)["properties"]
        material_data = str(material_properties)
        material_data = material_data.replace("('", '"')
        material_data = material_data.replace(")", '"')
        material_data = material_data.replace(": '", ':"')
        material_data = material_data.replace("', \"", '", "')
        material_data = material_data.replace("'", "")

        material_data = json.loads(material_data)
        if ("ambient, 0" in material_data and glm.length(material_data["ambient, 0"]) > 0):
            self.material.ambient = glm.vec3(
                material_data["ambient, 0"][0], material_data["ambient, 0"][1], material_data["ambient, 0"][2])
        if ("diffuse, 0" in material_data and glm.length(material_data["diffuse, 0"]) > 0):
            self.material.diffuse = glm.vec3(
                material_data["diffuse, 0"][0], material_data["diffuse, 0"][1], material_data["diffuse, 0"][2])
        if ("specular, 0" in material_data and glm.length(material_data["specular, 0"]) > 0):
            self.material.specular = glm.vec3(
                material_data["specular, 0"][0], material_data["specular, 0"][1], material_data["specular, 0"][2])

        if ("opacity, 0" in material_data):
            self.material.opacity = material_data["opacity, 0"]

        if ("shininess, 0" in material_data):
            self.material.n = material_data["shininess, 0"]

        if ("file, 1" in material_data):
            self.material.diffuseTextureFile = material_data["file, 1"]

    def setup(self):
        self.model = Model()
        self.create_vertex_buffer()
        self.create_normal_buffer()
        self.create_texture_buffer()
        self.create_index_buffer()
