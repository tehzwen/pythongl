# version 430 core

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

uniform Material material;
uniform bool diffuseSamplerExists;
uniform sampler2D diffuseSampler;

void main(){
    vec3 total = vec3(0,0,0);
    vec3 normal = normalize(normalInterp);
    if (diffuseSamplerExists) {
        vec3 textureColor = texture(diffuseSampler, oUV).rgb;
        total = material.diffuse * textureColor;
    } else {
        total = material.diffuse;
    }
    fragColor = vec4(total, material.alpha);
}