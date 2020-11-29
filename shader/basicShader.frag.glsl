# version 430 core
#define MAX_POINT_LIGHTS 20
out vec4 fragColor;

uniform vec3 diffuseValue;
uniform int numPointLights;

in vec3 oNormal;
in vec3 oFragPosition;
in vec3 normalInterp;


struct PointLight {
    vec3 position;
    vec3 color;
    float strength;
};

uniform PointLight[MAX_POINT_LIGHTS] pointLights;

vec3 CalculatePointLight(PointLight light, vec3 normal, vec3 fragPos) {
    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(dot(normal, lightDir), 0.0);

    vec3 diffuse = light.color * diffuseValue * diff;

    return diffuse;
}


void main(){
    vec3 total = vec3(0,0,0);

    for (int i = 0; i < numPointLights; i++) {
        total += CalculatePointLight(pointLights[i], normalInterp, oFragPosition);
    }
    fragColor = vec4(total, 1.0);
}