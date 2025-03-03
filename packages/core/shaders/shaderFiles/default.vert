#version 330 core

in vec3 in_vert;
in vec2 in_text;
in float in_text_id;

out vec2 v_text;
flat out int text_id;

uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;

void main(){
    vec4 fragPos = model * vec4(in_vert, 1.0);
    gl_Position = proj * view * fragPos;
    v_text = in_text;
    text_id = int(in_text_id);
}
