PHONG_VERT = """#version 330 core
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 color;

uniform mat4 projection, view;
uniform mat4 modelviewprojection;

out vec3 fragColor;
out vec3 fragPos;

void main() {
    gl_Position = projection * view * vec4(position, 1.);
    //gl_Position = modelviewprojection * vec4(position, 1);
    fragColor = color;// * .5f - .5f;
    fragPos = position;

}"""


PHONG_FRAG = """#version 330 core
in vec3 fragColor;
in vec3 fragPos;

out vec4 outColor;

uniform vec3 lightPos = vec3(0.f, 0.f, 0.f);
uniform vec3 viewPos = vec3(0.f, 0.f, 6.f);
uniform vec3 lightColor = vec3(1.f, .8f, .8f);
const float shininess = 1.f;

void main() {

    vec3 normal = fragColor;// * 2.f - 1.f;

    vec3 lightDir   = normalize(lightPos - fragPos);
    vec3 viewDir    = normalize(viewPos - fragPos);
    vec3 halfwayDir = normalize(lightDir + viewDir);

    // phong
    const float kEnergyConservation = ( 2.0 + shininess ) / ( 2.0 * 3.14159f );
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = kEnergyConservation * pow(max(dot(viewDir, reflectDir), 0.0), shininess);

    // blinn-phong
    //float spec = pow(max(dot(normal, halfwayDir), 0.0), shininess);
    //const float kEnergyConservation = ( 8.0 + shininess ) / ( 8.0 * kPi ); 
    // float spec = kEnergyConservation * pow(max(dot(normal, halfwayDir), 0.0), shininess);

    vec3 specular = lightColor * spec;



    outColor = vec4(vec3(.2f, .7f, .9f) * specular, 1);
    
    //outColor = vec4(vec3(1., 0., 0.) * mod(gl_FragCoord.x, 5.), 1);
}"""
