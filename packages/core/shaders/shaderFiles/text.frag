#version 330 core

in vec2 v_texcoord;

out vec4 f_color;
uniform sampler2D u_texture;
uniform vec3 u_color;

void main(){
    float alpha = texture(u_texture, v_texcoord).r;
    f_color = vec4(u_color, alpha);
}