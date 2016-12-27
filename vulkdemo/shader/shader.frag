#version 450
#extension GL_ARB_separate_shader_objects : enable

layout(location = 0) in vec3 fragColor;
layout(location = 1) in vec2 tex;
layout(location = 0) out vec4 outColor;

layout(binding = 0) uniform UniformBufferObject {
    float alpha;
} ubo;
layout(binding = 1) uniform sampler2D texSampler;

void main() {
    outColor = vec4(texture(texSampler, tex).rgb, 1.0);
}

