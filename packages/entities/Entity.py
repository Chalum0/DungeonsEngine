from packages.entities.models.Models import *
from packages.logic.functions.Mesh import *
from packages.shaders.Shader import *

from pyrr import Matrix44, Vector3
import numpy as np
import json


class Entity:
    def __init__(self, x, y, z):
        self.pos = (x, y, z)

        self.vbo = None
        self.ibo = None
        self.vao = None

        self.all_vertices, self.all_indices = self.create()

    def create(self):
        return Models().load("player")

    def create_object(self, ctx, shader):
        program = ctx.program(vertex_shader=shader.get_vertex_shader(), fragment_shader=shader.get_fragment_shader())
        self.vbo = ctx.buffer(self.all_vertices.tobytes())
        self.ibo = ctx.buffer(self.all_indices.tobytes())
        self.vao = ctx.simple_vertex_array(program, self.vbo, 'in_vert', 'in_text', 'in_text_id', index_buffer=self.ibo)

    def update_mesh(self):
        self.all_vertices, self.all_indices = self.create()
        self.vbo.write(self.all_vertices.tobytes())

    def get_vertex_object(self):
        return {"vbo": self.vbo, "ibo": self.ibo, "vao": self.vao}

    def get_vertices_amount(self):
        return len(self.all_vertices)
