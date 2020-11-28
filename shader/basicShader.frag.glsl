# version 430 core
out vec4 fragColor;

uniform vec3 diffuseValue;


void main(){
    fragColor = vec4(diffuseValue, 1.0);
}