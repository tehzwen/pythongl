#version 330 core
layout(location = 0) in vec3 vertexPosition;
layout(location = 2) in vec2 texture_coords;

out vec2 oUV;

void main(){
    oUV = texture_coords;
    gl_Position = vec4(vertexPosition, 1.0);
}
