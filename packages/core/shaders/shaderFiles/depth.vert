// depth.vert
#version 330 core

in vec3 in_vert;

uniform mat4 lightSpaceMatrix;
uniform mat4 model;

void main()
{
    gl_Position = lightSpaceMatrix * model * vec4(in_vert, 1.0);
}

// depth.frag
#version 330 core

void main()
{
    // gl_FragDepth is automatically written
}