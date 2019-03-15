COLOR_VERT = """#version 330 core
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 color;

uniform mat4 projection, view;
uniform mat4 modelviewprojection;
out vec3 fragColor;

void main() {
    gl_Position = projection * view * vec4(position, 1.);
    //gl_Position = modelviewprojection * vec4(position, 1);
    fragColor = color;
}"""


COLOR_FRAG = """#version 330 core
in vec3 fragColor;
out vec4 outColor;
void main() {
    outColor = vec4(fragColor, 1);
    
    //outColor = vec4(vec3(1., 0., 0.) * mod(gl_FragCoord.x, 5.), 1);
}"""
