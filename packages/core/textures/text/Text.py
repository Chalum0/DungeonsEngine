from packages.core.shaders.Shader import *

from freetype import FT_Exception
import numpy as np
import freetype


class Text:
    def __init__(self, context, window_size):
        self.fonts = {}
        self.load_font()

        self.context = context
        self.shader = ShaderObject("text")

        self.prog = self.context.program(vertex_shader=self.shader.vertex, fragment_shader=self.shader.fragment)

        self.u_screen_size = self.prog['u_screen_size']
        self.u_color = self.prog['u_color']
        self.u_screen_size.value = window_size

    def load_font(self, font_name="Minecraft"):
        self.fonts[font_name] = Font(name=font_name)

    def render_text(self, text, font_name, position=(0, 0), color=(1.0, 1.0, 1.0)):
        if font_name not in self.fonts:
            self.load_font(font_name)
        face = self.fonts[font_name].face
        pen_x, pen_y = position

        self.u_color.value = color

        for char in text:
            try:
                face.load_char(char)
            except FT_Exception:
                continue  # Skip characters that can't be loaded
            glyph = face.glyph

            # Convert bitmap to texture
            bitmap = glyph.bitmap
            width, height = bitmap.width, bitmap.rows
            if width == 0 or height == 0:
                continue  # Skip glyphs with no bitmap

            pixels = np.array(bitmap.buffer, dtype=np.uint8).reshape(height, width)

            # Create a texture in ModernGL using the bitmap
            texture = self.context.texture(
                (width, height),
                1,
                pixels.tobytes(),
                alignment=1
            )
            texture.use()

            # Calculate vertices
            x = pen_x + glyph.bitmap_left
            y = pen_y - glyph.bitmap_top
            w = width
            h = height

            vertices = np.array([
                x,     y + h, 0.0, 0.0,
                x,     y,     0.0, 1.0,
                x + w, y,     1.0, 1.0,
                x,     y + h, 0.0, 0.0,
                x + w, y,     1.0, 1.0,
                x + w, y + h, 1.0, 0.0,
            ], dtype='f4')

            vbo = self.context.buffer(vertices.tobytes())
            vao = self.context.simple_vertex_array(
                self.prog, vbo, 'in_position', 'in_texcoord')

            # Render the quad
            vao.render()

            # Advance the pen position
            pen_x += glyph.advance.x >> 6  # Convert from 26.6 fixed point to int

            # Release resources
            vao.release()
            vbo.release()
            texture.release()


class Font:
    def __init__(self, name, size=48*64):
        try:
            self.name = name
            self.face = freetype.Face(f"packages/textures/text/fonts/{self.name}.ttf")
            self.face.set_char_size(size)
        except FT_Exception:
            self.name = "Minecraft"
            self.face = freetype.Face(f"packages/textures/text/fonts/arial.ttf")
            self.face.set_char_size(size)
