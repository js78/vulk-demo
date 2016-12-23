#version 450
#extension GL_ARB_separate_shader_objects : enable

layout(location = 0) in vec3 fragColor;
layout(location = 0) out vec4 outColor;

layout(binding = 0) uniform UniformBufferObject {
    float alpha;
} ubo;

void main() {
    outColor = vec4(fragColor.x, fragColor.y, ubo.alpha, 1.0);
}

