import glm
import math


class Manager():
    def __init__(self):
        self._objects = {}
        self._point_lights = {}
        self._cameras = {}
        self._active_camera = None
        self.switch_camera = {"camera": None,
                              "center": False, "position": False, "speed": 0.0}

    def add_object(self, object):
        if (object.get_name() not in self._objects):
            self._objects[object.get_name()] = object
        else:
            raise Exception(
                "Object with this name already exists in the scene, names must be unique")

    def switch_cameras(self, name, speed):
        self.switch_camera["camera"] = name
        self.switch_camera["speed"] = speed

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

    def add_camera(self, cam):
        if (cam.get_name() not in self._cameras):
            self._cameras[cam.get_name()] = cam
            if (not self._active_camera):
                self._active_camera = cam.get_name()

    def get_camera(self, name):
        if (name in self._cameras):
            return self._cameras[name]

    def get_active_camera(self):
        return self._cameras[self._active_camera]

    def set_active_camera(self, name):
        if (name in self._cameras):
            self._active_camera = name

    def lerp_camera_center(self, delta_time):
        cam = self.get_active_camera()
        secondCam = self.get_camera(self.switch_camera["camera"])
        speed = self.switch_camera["speed"]

        camPosition = cam.get_center()
        secondPosition = secondCam.get_center()

        camQuat = glm.quat(
            camPosition[0], camPosition[1], camPosition[2], 1.0)
        secondQuat = glm.quat(
            secondPosition[0], secondPosition[1], secondPosition[2], 1.0)
        step = glm.lerp(camQuat, secondQuat, 1.0 - delta_time)
        step *= speed

        change = glm.vec3(camPosition[0], camPosition[1], camPosition[2])

        # check x coord
        if (abs(camPosition[0] - secondPosition[0]) > (speed * 2)):
            if (secondPosition[0] > camPosition[0]):
                change = glm.vec3(
                    change[0] + abs(step[0]), change[1], change[2])
            else:
                change = glm.vec3(
                    change[0] - abs(step[0]), change[1], change[2])

        # check y coord
        if (abs(camPosition[1] - secondPosition[1]) > (speed * 2)):
            if (secondPosition[1] > camPosition[1]):
                change = glm.vec3(change[0],
                                  change[1] + abs(step[1]), change[2])

            else:
                change = glm.vec3(change[0],
                                  change[1] - abs(step[1]), change[2])

        # # check z coord
        if (abs(camPosition[2] - secondPosition[2]) > (speed * 2)):
            if (secondPosition[2] > camPosition[2]):
                change = glm.vec3(change[0], change[1],
                                  change[2] + abs(step[2]))

            else:
                change = glm.vec3(change[0], change[1],
                                  change[2] + abs(step[2]))

        if (abs(camPosition[0] - secondPosition[0]) < (speed * 2) and abs(camPosition[1] - secondPosition[1]) < (speed * 2) and abs(camPosition[2] - secondPosition[2]) < (speed * 2)):
            self.switch_camera["center"] = True
        else:
            cam.set_center(change)

    def lerp_to_camera(self, delta_time):
        cam = self.get_active_camera()
        secondCam = self.get_camera(self.switch_camera["camera"])
        speed = self.switch_camera["speed"]

        camPosition = cam.get_position()
        secondPosition = secondCam.get_position()

        camQuat = glm.quat(
            camPosition[0], camPosition[1], camPosition[2], 1.0)
        secondQuat = glm.quat(
            secondPosition[0], secondPosition[1], secondPosition[2], 1.0)
        step = glm.lerp(camQuat, secondQuat, 1.0 - delta_time)
        step *= speed

        change = glm.vec3(camPosition[0], camPosition[1], camPosition[2])

        # check x coord
        if (abs(camPosition[0] - secondPosition[0]) > (speed * 5)):
            if (secondPosition[0] > camPosition[0]):
                change = glm.vec3(
                    change[0] + abs(step[0]), change[1], change[2])
            else:
                change = glm.vec3(
                    change[0] - abs(step[0]), change[1], change[2])

        # check y coord
        if (abs(camPosition[1] - secondPosition[1]) > (speed * 5)):
            if (secondPosition[1] > camPosition[1]):
                change = glm.vec3(change[0],
                                  change[1] + abs(step[1]), change[2])

            else:
                change = glm.vec3(change[0],
                                  change[1] - abs(step[1]), change[2])

        # # check z coord
        if (abs(camPosition[2] - secondPosition[2]) > (speed * 5)):
            if (secondPosition[2] > camPosition[2]):
                change = glm.vec3(change[0], change[1],
                                  change[2] + abs(step[2]))

            else:
                change = glm.vec3(change[0], change[1],
                                  change[2] + abs(step[2]))

        if (abs(camPosition[0] - secondPosition[0]) < (speed * 5) and abs(camPosition[1] - secondPosition[1]) < (speed * 5) and abs(camPosition[2] - secondPosition[2]) < (speed * 5)):
            self.set_active_camera(secondCam.get_name())
            self.switch_camera["position"] = True
        else:
            cam.set_position(change)

    def update(self, delta_time):

        # check if camera switching is occuring
        if (self.switch_camera["camera"]):
            if (not self.switch_camera["position"]):
                self.lerp_to_camera(delta_time)
            if (not self.switch_camera["center"]):
                self.lerp_camera_center(delta_time)

            if (self.switch_camera["center"] and self.switch_camera["position"]):
                self.set_active_camera(self.switch_camera["camera"])
                self.switch_camera = {"camera": None,
                                      "center": False, "position": False, "speed": 0.0}
