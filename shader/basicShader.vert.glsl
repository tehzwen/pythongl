# version 430 core
layout(location = 0) in vec3 vertexPosition;
layout(location = 1) in vec3 vertexNormal;
layout(location = 2) in vec2 texture_coords;

uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;
uniform mat4 modelMatrix;
uniform mat4 normalMatrix;

out vec3 oNormal;
out vec3 oFragPosition;
out vec3 normalInterp;
out vec2 oUV;


void main(){
    oNormal = vertexNormal;
    oFragPosition = (modelMatrix * vec4(vertexPosition, 1.0)).xyz;
    normalInterp = (normalMatrix * vec4(vertexNormal, 0.0)).xyz;
    oUV = texture_coords;
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
}