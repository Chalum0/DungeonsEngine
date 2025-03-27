from packages.core.textures.TexturesList import *

from PIL import Image


class Textures:
    def __init__(self, ctx):
        self.textures_to_load = textures.values()
        self.array = None
        self.load_textures(self.textures_to_load, ctx)

    def load_textures(self, paths, ctx):
        # Load images and convert each to RGB to ensure there are no palette-based images
        images = [Image.open(f"packages/core/textures/{path}").convert('RGBA') for path in paths]
        if not all(img.size == images[0].size for img in images):
            raise ValueError("All textures must have the same dimensions for a texture array.")

        width, height = images[0].size
        texture_layers = len(paths)
        channels = 4  # Using RGBA, 4 channels

        # Create a buffer to store all images
        data = b''.join([img.tobytes("raw", "RGBA", 0, -1) for img in images])

        # Calculate expected buffer size and compare to actual
        expected_size = width * height * channels * texture_layers
        if len(data) != expected_size:
            raise ValueError(f"Data size mismatch: expected {expected_size}, got {len(data)}")

        # Create the texture array
        texture = ctx.texture_array((width, height, texture_layers), channels, data)

        texture.build_mipmaps()
        self.array = texture

    def get_array(self):
        return self.array