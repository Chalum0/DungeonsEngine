from packages.shaders.Settings import *


class FragmentShader:
    def __init__(self, shader_name="default"):
        try:
            with open(f"{SHADER_PATH}{shader_name}.frag") as f:
                self.shader = f.read()
        except FileNotFoundError:
            with open(f"{SHADER_PATH}default.frag") as f:
                self.shader = f.read()

    def get(self):
        return self.shader
