import glm
import noise

def get_pnoise(z, x, scale=10, octaves=1, lacunarity=1000, persistence=1000, added_scale=5, size=100):
    val = noise.pnoise2(z/scale, x/scale, octaves=octaves, persistence=persistence,
                        lacunarity=lacunarity, repeatx=size*2, repeaty=size*2, base=0)
    return val * added_scale
    # return 5.0

def lerp_to_vec3(source, target, speed, delta_time):
    sourceQuat = glm.quat(
        source[0], source[1], source[2], 1.0)
    targetQuat = glm.quat(
        target[0], target[1], target[2], 1.0)
    step = glm.lerp(sourceQuat, targetQuat, 1.0 - delta_time)
    step *= speed

    change = glm.vec3(source[0], source[1], source[2])

    # check x coord
    if (abs(source[0] - target[0]) > (speed * 2)):
        if (target[0] > source[0]):
            change = glm.vec3(
                change[0] + abs(step[0]), change[1], change[2])
        else:
            change = glm.vec3(
                change[0] - abs(step[0]), change[1], change[2])

    # check y coord
    if (abs(source[1] - target[1]) > (speed * 2)):
        if (target[1] > source[1]):
            change = glm.vec3(change[0],
                              change[1] + abs(step[1]), change[2])

        else:
            change = glm.vec3(change[0],
                              change[1] - abs(step[1]), change[2])

    # # check z coord
    if (abs(source[2] - target[2]) > (speed * 2)):
        if (target[2] > source[2]):
            change = glm.vec3(change[0], change[1],
                              change[2] + abs(step[2]))

        else:
            change = glm.vec3(change[0], change[1],
                              change[2] - abs(step[2]))

    if (abs(source[0] - target[0]) < (speed * 3) and abs(source[1] - target[1]) < (speed * 3) and abs(source[2] - target[2]) < (speed * 3)):
        return (True, change)
    else:
        return (False, change)
