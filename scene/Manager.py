
class Manager():
    def __init__(self):
        self._objects = {}
        self._point_lights = {}

    def add_object(self, object):
        if (object.get_name() not in self._objects):
            self._objects[object.get_name()] = object
        else:
            raise Exception(
                "Object with this name already exists in the scene, names must be unique")

    def get_objects(self):
        return self._objects

    def get_object(self, name):
        if (name in self._objects):
            return self._objects[name]
        else:
            raise Exception("No object with this name")

    def add_point_light(self, light):
        if (light.get_name() not in self._point_lights):
            self._point_lights[light.get_name()] = light
        else:
            raise Exception(
                "Pointlight with this name already exists in the scene, names must be unique")

    def get_point_lights(self):
        return self._point_lights

    def get_point_light(self, name):
        if (name in self._point_lights):
            return self._point_lights[name]
        else:
            raise Exception("No Pointlight with this name")
