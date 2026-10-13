#version 330 core
in vec2 v_texcoord;
out vec4 FragColor;

uniform sampler2D screen_tex;

void main() {
    ivec2 tex_size = textureSize(screen_tex, 0);
    ivec2 texel = ivec2(v_texcoord * vec2(tex_size));
    FragColor = texelFetch(screen_tex, texel, 0);
}
