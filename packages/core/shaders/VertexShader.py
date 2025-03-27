from packages.core.shaders.Settings import *


class VertexShader:
    def __init__(self, shader_name="default"):
        try:
            with open(f"{SHADER_PATH}{shader_name}.vert") as f:
                self.shader = f.read()
        except FileNotFoundError:
            with open(f"{SHADER_PATH}default.vert") as f:
                self.shader = f.read()

    def get(self):
        return self.shader
