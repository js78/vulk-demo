#version 450
#extension GL_ARB_separate_shader_objects : enable

layout(location = 0) in vec2 position;
layout(location = 1) in uvec3 color;
layout(location = 2) in vec2 textureCoord;

layout(location = 0) out vec3 fragColor;
layout(location = 1) out vec2 tex;

out gl_PerVertex {
    vec4 gl_Position;
};


void main() {
    fragColor = vec3(float(color.r), float(color.g), float(color.b));
    tex = textureCoord;
    gl_Position = vec4(position, 0.0, 1.0);
}

