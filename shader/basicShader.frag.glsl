# version 430 core
#define MAX_POINT_LIGHTS 20
out vec4 fragColor;

in vec3 oNormal;
in vec3 oFragPosition;
in vec3 normalInterp;
in vec2 oUV;

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

vec3 CalculatePointLight(PointLight light, vec3 normal, vec3 fragPos) {
    vec3 ambient = material.ambient * light.color;
    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(dot(normal, lightDir), 0.0);

    vec3 diffuse = light.color * material.diffuse * diff;

    return ambient + diffuse;
}


void main(){
    vec3 total = vec3(0,0,0);

    for (int i = 0; i < numPointLights; i++) {
        total += CalculatePointLight(pointLights[i], normalInterp, oFragPosition);
    }

    if (diffuseSamplerExists == 1) {
        vec4 textureColor = texture(diffuseSampler, oUV);
        fragColor = vec4(textureColor.xyz, 1.0);
    } else {
        fragColor = vec4(total, material.alpha);
    }
}