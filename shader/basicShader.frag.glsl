# version 430 core
#define MAX_POINT_LIGHTS 20
#define MAX_AREA_LIGHTS 20
#define MAX_DIR_LIGHTS 5

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

struct DirectionalLight {
    vec3 position;
    vec3 color;
    vec3 direction;
    float strength;
};

struct CircularAreaLight {
    vec3 position;
    vec3 color;
    float strength;
    float linear;
    float quadratic;
    float radius;
};

uniform int numPointLights;
uniform int numAreaLights;
uniform int numDirectionalLights;
uniform Material material;
uniform PointLight[MAX_POINT_LIGHTS] pointLights;
uniform CircularAreaLight[MAX_AREA_LIGHTS] circularAreaLights;
uniform DirectionalLight[MAX_DIR_LIGHTS] dirLights;
uniform bool diffuseSamplerExists;
uniform sampler2D diffuseSampler;

vec3 CalculateDirectionalLight(DirectionalLight light, vec3 cameraPosition, vec3 normal, vec3 fragPos, vec3 diffuseValue) {
    vec3 ambient = material.ambient * light.color * diffuseValue;
    vec3 lightDir = normalize(-light.direction);
    float diff = max(dot(normal, lightDir), 0.0);
    vec3 diffuse = light.color * diffuseValue * diff * light.strength;
    vec3 viewDir = normalize(cameraPosition - fragPos);
    vec3 reflectDir = reflect(-lightDir, normal);  
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
    vec3 specular = spec * light.color;  
    return (ambient + diffuse + specular);
}

vec3 CalculatePointLight(PointLight light, vec3 cameraPosition, vec3 normal, vec3 fragPos, vec3 diffuseValue) {
    vec3 ambient = material.ambient * light.color * diffuseValue;
    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(dot(normal, lightDir), 0.0);
    float light_distance = length(light.position - fragPos);
    float attenuation = light.strength / (1.0 + (light.linear * light_distance) + (light.quadratic * (light_distance * light_distance)));
    vec3 diffuse = light.color * diffuseValue * diff;

    vec3 viewDir = normalize(cameraPosition - fragPos);
    vec3 reflectDir = reflect(-lightDir, normal);  
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
    vec3 specular = spec * light.color;  
    return attenuation * (ambient + diffuse + specular);
}

// TODO NEED TO FIX THIS
vec3 CalculateCircularAreaLight(CircularAreaLight light, vec3 cameraPosition, vec3 normal, vec3 fragPos, vec3 diffuseValue) {
    vec3 lightDir = normalize(light.position - fragPos);
    vec3 viewDir = normalize(cameraPosition - fragPos);
    vec3 reflectDir = reflect(-lightDir, normal);
    // vec3 L = ((light.position * light.radius) - fragPos);
    vec3 L = (light.position - fragPos);
    vec3 centerToRay = ((dot(L,reflectDir) * reflectDir) - L);
    vec3 closestPoint = L + centerToRay * clamp((light.radius/ length(centerToRay)), 0, 1);
    float distLight = length(closestPoint);
    float falloff = pow(clamp(1.0 - pow(distLight/(light.radius), 4), 0, 1), 2)/((distLight * distLight) + 1.0);

    vec3 ambient = material.ambient * light.color * diffuseValue;
    float diff = max(dot(normal, lightDir), 0.0);
    float light_distance = length(light.position - fragPos);
    float attenuation = light.strength / (1.0 + (light.linear * light_distance) + (light.quadratic * (light_distance * light_distance)));
    vec3 diffuse = light.color * diffuseValue * diff;

    float spec = pow(max(dot(viewDir, centerToRay), 0.0), material.shininess);
    vec3 specular = (spec * light.color);  
    return specular;
}


void main(){
    vec3 total = vec3(0,0,0);
    vec3 normal = normalize(normalInterp);
    if (diffuseSamplerExists) {
        vec4 textureColor = texture(diffuseSampler, oUV);
        for (int i = 0; i < numPointLights; i++) {
            total += CalculatePointLight(pointLights[i], oCameraPosition, normal, oFragPosition, material.diffuse * textureColor.rgb);
        }

        for (int i = 0; i < numAreaLights; i++) {
            total += CalculateCircularAreaLight(circularAreaLights[i], oCameraPosition, normal, oFragPosition, material.diffuse * textureColor.rgb);
        }

        for (int i = 0; i < numDirectionalLights; i++) {
            total += CalculateDirectionalLight(dirLights[i], oCameraPosition, normal, oFragPosition, material.diffuse * textureColor.rgb);
        }

    } else {
        for (int i = 0; i < numPointLights; i++) {
            total += CalculatePointLight(pointLights[i], oCameraPosition, normal, oFragPosition, material.diffuse);
        }
        for (int i = 0; i < numDirectionalLights; i++) {
            total += CalculateDirectionalLight(dirLights[i], oCameraPosition, normal, oFragPosition, material.diffuse);
        }
    }
    fragColor = vec4(total, material.alpha);
    // fragColor = vec4(0.5, 0.5, 0.5, material.alpha);

}