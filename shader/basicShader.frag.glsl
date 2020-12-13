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
    float linear;
    float quadratic;
};

uniform int numPointLights;
uniform Material material;
uniform PointLight[MAX_POINT_LIGHTS] pointLights;
uniform bool diffuseSamplerExists;
uniform sampler2D diffuseSampler;

vec3 CalculatePointLight(PointLight light, vec3 cameraPosition, vec3 normal, vec3 fragPos, vec3 diffuseValue) {
    vec3 ambient = material.ambient * light.color * diffuseValue;
    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(dot(normal, lightDir), 0.0);
    float distance = length(light.position - fragPos);
    float attenuation = light.strength / (1.0 + (light.linear * distance) + (light.quadratic * (distance * distance)));
    vec3 diffuse = light.color * diffuseValue * diff;

    vec3 viewDir = normalize(cameraPosition - fragPos);
    vec3 reflectDir = reflect(-lightDir, normal);  
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
    vec3 specular = spec * light.color;  
    return attenuation * (ambient + diffuse + specular);
}


void main(){
    vec3 total = vec3(0,0,0);
    total = vec3(0.5, 0.5, 0.5);
    // if (diffuseSamplerExists) {
    //     for (int i = 0; i < numPointLights; i++) {
    //         vec4 textureColor = texture(diffuseSampler, oUV);
    //         total += CalculatePointLight(pointLights[i], oCameraPosition, normalInterp, oFragPosition, material.diffuse * textureColor.rgb);
    //     }
    // } else {
    //     for (int i = 0; i < numPointLights; i++) {
    //         total += CalculatePointLight(pointLights[i], oCameraPosition, normalInterp, oFragPosition, material.diffuse);
    //     }
    // }
    fragColor = vec4(total, material.alpha);
}