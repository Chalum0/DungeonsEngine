import unittest

from packages.core.shaders.Shader import Shader


class TestShader(unittest.TestCase):

    def setUp(self):
        self.shader = Shader()

    def test_load_shader_exists(self):
        self.shader.load_shader("default")

    def test_load_shader_not_exist(self):
        self.shader.load_shader("non-default")

    def test_load_invalid_shader_loads_default_shader(self):
        self.shader.load_shader("default")
        self.shader.load_shader("non-default")

    def test_get_vertex_shader_exists(self):
        vertex_shader = self.shader.get_vertex_shader("default")
        self.assertIsNotNone(vertex_shader)

    def test_get_vertex_shader_not_exists_returns_default_shader(self):
        vertex_shader = self.shader.get_vertex_shader("non-default")
        self.assertEqual(vertex_shader, self.shader.get_vertex_shader("default"))

    def test_get_fragment_shader_exists(self):
        fragment_shader = self.shader.get_fragment_shader("default")
        self.assertIsNotNone(fragment_shader)

    def test_get_fragment_shader_not_exists_returns_default_shader(self):
        fragment_shader = self.shader.get_fragment_shader("non-default")
        self.assertEqual(fragment_shader, self.shader.get_fragment_shader("default"))

if __name__ == '__main__':
    unittest.main()