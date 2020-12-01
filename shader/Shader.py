import sys
from OpenGL import GL as gl


class Shader:
    def __init__(self):
        self._fragSource = ""
        self._vertSource = ""
        self.program_id = None

    def load_frag_source(self, file_name=None, source=None):
        if (source):
            self._fragSource = source
        elif (file_name):
            f = open("./shader/" + file_name, 'r')
            self._fragSource = f.read()
            f.close()
        else:
            raise Exception("Need to provide file_name or source string")

    def load_vert_source(self, file_name=None, source=None):
        if (source):
            self._vertSource = source
        elif (file_name):
            f = open("./shader/" + file_name, 'r')
            self._vertSource = f.read()
            f.close()
        else:
            raise Exception("Need to provide file_name or source string")

    def init(self):
        shaders = {
            gl.GL_VERTEX_SHADER: self._vertSource,
            gl.GL_FRAGMENT_SHADER: self._fragSource
        }
        self.program_id = gl.glCreateProgram()
        shader_ids = []
        for shader_type, shader_src in shaders.items():
            shader_id = gl.glCreateShader(shader_type)
            gl.glShaderSource(shader_id, shader_src)

            gl.glCompileShader(shader_id)

            # check if compilation was successful
            result = gl.glGetShaderiv(shader_id, gl.GL_COMPILE_STATUS)
            info_log_len = gl.glGetShaderiv(shader_id, gl.GL_INFO_LOG_LENGTH)
            if info_log_len:
                logmsg = gl.glGetShaderInfoLog(shader_id)
                print("ERROR: ", logmsg)
                sys.exit(10)

            gl.glAttachShader(self.program_id, shader_id)
            shader_ids.append(shader_id)

        gl.glLinkProgram(self.program_id)

        # check if linking was successful
        result = gl.glGetProgramiv(self.program_id, gl.GL_LINK_STATUS)
        info_log_len = gl.glGetProgramiv(
            self.program_id, gl.GL_INFO_LOG_LENGTH)
        if info_log_len:
            logmsg = gl.glGetProgramInfoLog(self.program_id)
            log.error(logmsg)
            sys.exit(11)

    def bind(self):
        gl.glUseProgram(self.program_id)

    def link_mat4(self, name, matrix):
        gl.glUniformMatrix4fv(gl.glGetUniformLocation(self.program_id, name), 1, False, matrix)

    def link_vec3(self, name, vec, count):
        gl.glUniform3fv(gl.glGetUniformLocation(self.program_id, name), count, vec)

    def link_float(self, name, val):
        gl.glUniform1f(gl.glGetUniformLocation(self.program_id, name), val)

    def link_int(self, name, val):
        gl.glUniform1i(gl.glGetUniformLocation(self.program_id, name), val)