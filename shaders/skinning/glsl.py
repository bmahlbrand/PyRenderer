MAX_VERTEX_BONES = 4
MAX_BONES = 128

SKINNING_VERT = """#version 330 core
// ---- camera geometry
uniform mat4 projection, view;

// ---- skinning globals and attributes
const int MAX_VERTEX_BONES=%d, MAX_BONES=%d;
uniform mat4 boneMatrix[MAX_BONES];

// ---- vertex attributes
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 color;
layout(location = 2) in vec4 bone_ids;
layout(location = 3) in vec4 bone_weights;

// ----- interpolated attribute variables to be passed to fragment shader
out vec3 fragColor;

void main() {

    // ------ creation of the skinning deformation matrix
    mat4 skinMatrix = mat4(1.);  // TODO complete shader here for exercise 1!

    // ------ compute world and normalized eye coordinates of our vertex
    vec4 wPosition4 = skinMatrix * vec4(position, 1.0);
    gl_Position = projection * view * wPosition4;
    
    fragColor = color;
}
""" % (MAX_VERTEX_BONES, MAX_BONES)