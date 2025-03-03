#version 330 core

in vec2 v_text;
flat in int text_id;

out vec4 f_color;

uniform sampler2DArray textures;

void main(){
    ivec2 texSize = textureSize(textures, 0).xy;
    ivec2 texel_coords = ivec2(v_text * vec2(texSize));
    f_color = texelFetch(textures, ivec3(texel_coords, text_id), 0);

    // Optional: Discard fragments with low alpha (if using cutout transparency)
    // if (f_color.a < 0.1)
        // discard;
}
