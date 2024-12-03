from packages.shaders.FragmentShader import FragmentShader
from packages.shaders.VertexShader import VertexShader

class Shader:
    def __init__(self):
        self.shaders = {}
        self.load_shader("default")

    def load_shader(self, name):
        self.shaders[name] = ShaderObject(name)

    def get_vertex_shader(self, name="default"):
        """
        :param name: The name of the shader to retrieve the vertex shader from.
        :return: The vertex shader associated with the given name, or the default vertex shader if the name does not exist.
        """
        if self._shader_exists(name):
            return self.shaders[name].vertex
        return self.shaders["default"].vertex

    def get_fragment_shader(self, name="default"):
        """
        :param name: The name of the shader to retrieve.
        :return: The fragment shader associated with the given name, or the default vertex shader if the name does not exist.
        """
        if self._shader_exists(name):
            return self.shaders[name].fragment
        return self.shaders["default"].fragment

    def get_shader(self, name):
        """
        :param name: The name of the shader to retrieve.
        :return: A tuple containing the vertex and fragment shaders. If the shader with the provided name does not exist, returns the default vertex and fragment shaders.
        """
        if self._shader_exists(name):
            return self.get_vertex_shader(name), self.get_fragment_shader(name)
        return self.get_vertex_shader("default"), self.get_fragment_shader("default")

    def _shader_exists(self, name):
        return name in self.shaders.keys()



class ShaderObject:
    def __init__(self, name):
        self.vertex = VertexShader(shader_name=name).get()
        self.fragment = FragmentShader(shader_name=name).get()

    def __eq__(self, other):
        return self.vertex == other.vertex and self.fragment == other.fragment