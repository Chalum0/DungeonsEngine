from packages.world.entities.ModelManager import ModelManager
from packages.world.entities.BoundingBox import BoundingBox

from pyrr import Vector3, Vector4, Matrix44
import numpy as np

class EntityTemplate:
    def __init__(self, name, model_path, hidden: bool=False):
        self._model_manager: ModelManager = None
        self._all_entities = None

        self._name = name
        self._model_path = model_path
        self._hidden = hidden

        self._pos = None
        self._rotation = None
        self._model = None
        self._vbo = None
        self._ibo = None
        self._vao = None
        self._program = None
        self._all_vertices = None
        self._all_indices = None
        self._bounding_box = None

        self._on_update_callback = None

    def instanciate(self, entities_container, model_manager: ModelManager):
        self._all_entities = entities_container
        self._model_manager = model_manager
        self._pos = [0, 0, 0]
        self._rotation = Vector3([0.0, 0.0, 0.0], dtype='float32')

        self._model = Matrix44.from_translation(self._pos, dtype='float32')

        self._all_vertices, self._all_indices = self._create()
        self._bounding_box = BoundingBox()
        self._update_bounding_box()

    def kill(self):
        if self in self._all_entities:
            self._all_entities.remove(self)

    def hide(self):
        self._hidden = True
    def show(self):
        self._hidden = False
    def toggle_hidden(self):
        self._hidden = not self._hidden

    def _create(self) -> tuple[float, float]:
        return self._model_manager.load(self._model_path)

    def create_object(self, ctx, shader):
        program = ctx.program(
            vertex_shader=shader.get_vertex_shader(),
            fragment_shader=shader.get_fragment_shader()
        )
        self._program = program

        self._vbo = ctx.buffer(self._all_vertices.tobytes())
        self._ibo = ctx.buffer(self._all_indices.tobytes())
        self._vao = ctx.simple_vertex_array(
            program,
            self._vbo,
            'in_vert', 'in_text', 'in_text_id',
            index_buffer=self._ibo
        )
    def get_vertex_object(self):
        return {"vbo": self._vbo, "ibo": self._ibo, "vao": self._vao}
    def get_vertices_amount(self):
        return len(self._all_vertices)
    def set_position(self, x, y, z):
        self._pos = (x, y, z)
        self._model = Matrix44.from_translation(self._pos, dtype='float32')
        self._update_pos()
    def translate(self, dx, dy, dz):
        self._pos = (
            self._pos[0] + dx,
            self._pos[1] + dy,
            self._pos[2] + dz
        )
        self._model = Matrix44.from_translation(self._pos, dtype='float32')
        self._update_pos()
    def _update_pos(self):
        if self._program is None:
            return

        self.model = self._calculate_model_matrix()
        self._program['model'].write(self.model)
        self._update_bounding_box()
    def _calculate_model_matrix(self):
        """
        Combines translation and rotation into a single Matrix44.
        The multiplication order here means we rotate first, then translate.
        """
        translation_matrix = Matrix44.from_translation(self._pos, dtype='float32')

        # You can choose a single Euler-based rotation:
        rotation_matrix = Matrix44.from_eulers(self._rotation, dtype='float32')

        # If you want to apply rotations in a specific axis order (e.g., Z * Y * X):
        # rotation_matrix_z = Matrix44.from_z_rotation(self.rotation.z, dtype='float32')
        # rotation_matrix_y = Matrix44.from_y_rotation(self.rotation.y, dtype='float32')
        # rotation_matrix_x = Matrix44.from_x_rotation(self.rotation.x, dtype='float32')
        # rotation_matrix = rotation_matrix_z * rotation_matrix_y * rotation_matrix_x

        # The final model
        model_matrix = translation_matrix * rotation_matrix

        return model_matrix
    def _update_bounding_box(self):
        """
        Returns the bounding box (min_x, min_y, min_z, max_x, max_y, max_z)
        of this entity, accounting for the current position and rotation
        via 'self.model'.
        """
        # Since each vertex is stored as [x, y, z, ..., ..., ...] (6 floats total),
        # reshape or iterate in steps of 6 to isolate the actual positions.
        stride = 6

        min_x, min_y, min_z = float('inf'), float('inf'), float('inf')
        max_x, max_y, max_z = -float('inf'), -float('inf'), -float('inf')

        for i in range(0, len(self._all_vertices), stride):
            # Extract local vertex coordinates
            x = self._all_vertices[i + 0]
            y = self._all_vertices[i + 1]
            z = self._all_vertices[i + 2]

            # Convert to a 4D vector so it can be multiplied by the model matrix
            local_pos = Vector4([x, y, z, 1.0], dtype='float32')
            world_pos = self._model * local_pos

            # Update min/max bounds
            if world_pos.x < min_x: min_x = world_pos.x
            if world_pos.y < min_y: min_y = world_pos.y
            if world_pos.z < min_z: min_z = world_pos.z

            if world_pos.x > max_x: max_x = world_pos.x
            if world_pos.y > max_y: max_y = world_pos.y
            if world_pos.z > max_z: max_z = world_pos.z

        self._bounding_box.update_with_min_max(min_x, min_y, min_z, max_x, max_y, max_z)

    def get_pos(self):
        return self._pos

    @property
    def model(self):
        return self._model

    def set_on_update_callback(self, callback_function):
        self._on_update_callback = callback_function

    def on_update(self):
        if self._on_update_callback is not None:
            self._on_update_callback()
