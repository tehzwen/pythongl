# version 430 core
#define MAX_POINT_LIGHTS 20
out vec4 fragColor;

in vec3 oNormal;
in vec3 oFragPosition;
in vec3 normalInterp;
in vec2 oUV;
in vec3 oCameraPosition;

struct Material {
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
    float shininess;
    float alpha;
};

struct PointLight {
    vec3 position;
    vec3 color;
    float strength;
};

uniform int numPointLights;
uniform Material material;
uniform PointLight[MAX_POINT_LIGHTS] pointLights;
uniform int diffuseSamplerExists;
uniform sampler2D diffuseSampler;

vec3 CalculatePointLight(PointLight light, vec3 normal, vec3 fragPos, vec3 diffuseValue) {
    vec3 ambient = material.ambient * light.color * material.diffuse;
    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(dot(normal, lightDir), 0.0);
    float distance = length(light.position - fragPos);
    float attenuation = light.strength / (distance * distance);
    vec3 diffuse = light.color * diffuseValue * diff;

    return attenuation * (ambient + diffuse);
}


void main(){
    vec3 total = vec3(0,0,0);

    if (diffuseSamplerExists == 1) {
        for (int i = 0; i < numPointLights; i++) {
            total += CalculatePointLight(pointLights[i], normalInterp, oFragPosition, material.diffuse * texture(diffuseSampler, oUV).rgb);
        }
    } else {
        for (int i = 0; i < numPointLights; i++) {
            total += CalculatePointLight(pointLights[i], normalInterp, oFragPosition, material.diffuse);
        }
    }
    fragColor = vec4(total, material.alpha);
}