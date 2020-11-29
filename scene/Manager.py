
class Manager():
    def __init__(self):
        self._objects = {}

    def add_object(self, object):
        if (object.get_name() not in self._objects):
            self._objects[object.get_name()] = object
        else:
            raise Exception("Object with this name already exists in the scene, names must be unique")

    def get_objects(self):
        return self._objects