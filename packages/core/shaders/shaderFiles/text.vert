#version 330 core

in vec2 in_position;
in vec2 in_texcoord;

out vec2 v_texcoord;
uniform vec2 u_screen_size;

void main() {
    vec2 pos = in_position / u_screen_size * 2.0 - 1.0;
    gl_Position = vec4(pos, 0.0, 1.0);
    v_texcoord = in_texcoord;
}