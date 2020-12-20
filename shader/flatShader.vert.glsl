# version 430 core
layout(location = 0) in vec3 vertexPosition;

uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;
uniform mat4 modelMatrix;

out vec3 oCameraPosition;
out vec3 oNormal;
out vec3 oFragPosition;

void main(){
    oFragPosition = (modelMatrix * vec4(vertexPosition, 1.0)).xyz;
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
}