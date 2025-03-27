from packages.entities.BoundingBox import BoundingBox
from packages.entities.models.Models import *

from pyrr import Matrix44, Vector3, Vector4


class Entity:
    def __init__(self, x, y, z):
        self.pos = (x, y, z)
        self.rotation = Vector3([0.0, 0.0, 0.0], dtype='float32')

        self.model = Matrix44.from_translation(self.pos, dtype='float32')
        self.vbo = None
        self.ibo = None
        self.vao = None

        self.program = None

        self.all_vertices, self.all_indices = self.create()
        self.bounding_box = BoundingBox()
        self._update_bounding_box()

    def create(self):
        return Models().load("cube")
    
    def create_object(self, ctx, shader):
        # Create the ModernGL program
        program = ctx.program(
            vertex_shader=shader.get_vertex_shader(),
            fragment_shader=shader.get_fragment_shader()
        )
        self.program = program  # Save reference so we can update uniforms later

        self.vbo = ctx.buffer(self.all_vertices.tobytes())
        self.ibo = ctx.buffer(self.all_indices.tobytes())
        self.vao = ctx.simple_vertex_array(
            program,
            self.vbo,
            'in_vert', 'in_text', 'in_text_id',
            index_buffer=self.ibo
        )


    def get_vertex_object(self):
        return {"vbo": self.vbo, "ibo": self.ibo, "vao": self.vao}
    def get_vertices_amount(self):
        return len(self.all_vertices)


    def set_position(self, x, y, z):
        """
        Sets the absolute position of the entity
        and updates the model matrix accordingly.
        """
        self.pos = (x, y, z)
        self.model = Matrix44.from_translation(self.pos, dtype='float32')
        self._update_pos()
    def translate(self, dx, dy, dz):
        """
        Moves the entity by a relative offset.
        Also updates the model matrix accordingly.
        """
        # Update self.pos
        self.pos = (
            self.pos[0] + dx,
            self.pos[1] + dy,
            self.pos[2] + dz
        )
        self.model = Matrix44.from_translation(self.pos, dtype='float32')
        self._update_pos()
    def _update_pos(self):
        """
        Writes the current model matrix to the GPU uniform.
        Call this before rendering.
        """
        if self.program is None:
            return

        # Update the 'model' uniform on the GPU
        self.model = self._calculate_model_matrix()
        self.program['model'].write(self.model)
        self._update_bounding_box()

    def collides_with(self, obj):
        return self.bounding_box.collides_with(obj.bounding_box)

    def set_rotation(self, rx, ry, rz):
        """
        Sets the absolute rotation of the entity (in radians),
        and updates the model matrix accordingly.
        """
        self.rotation = Vector3([rx, ry, rz], dtype='float32')
        self._update_model()
    def rotate(self, dx, dy, dz):
        """
        Applies incremental rotation (in radians) to the entity.
        """
        self.rotation += Vector3([dx, dy, dz], dtype='float32')
        self._update_model()
    def _update_model(self):
        """
        Recalculates the model matrix from the entity’s current
        position and rotation, and updates GPU uniforms + bounding box.
        """
        self.model = self._calculate_model_matrix()
        self._update_pos()
    def _calculate_model_matrix(self):
        """
        Combines translation and rotation into a single Matrix44.
        The multiplication order here means we rotate first, then translate.
        """
        translation_matrix = Matrix44.from_translation(self.pos, dtype='float32')

        # You can choose a single Euler-based rotation:
        rotation_matrix = Matrix44.from_eulers(self.rotation, dtype='float32')

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

        for i in range(0, len(self.all_vertices), stride):
            # Extract local vertex coordinates
            x = self.all_vertices[i + 0]
            y = self.all_vertices[i + 1]
            z = self.all_vertices[i + 2]

            # Convert to a 4D vector so it can be multiplied by the model matrix
            local_pos = Vector4([x, y, z, 1.0], dtype='float32')
            world_pos = self.model * local_pos  # Transform by the model matrix

            # Update min/max bounds
            if world_pos.x < min_x: min_x = world_pos.x
            if world_pos.y < min_y: min_y = world_pos.y
            if world_pos.z < min_z: min_z = world_pos.z

            if world_pos.x > max_x: max_x = world_pos.x
            if world_pos.y > max_y: max_y = world_pos.y
            if world_pos.z > max_z: max_z = world_pos.z

        self.bounding_box.update_with_min_max(min_x, min_y, min_z, max_x, max_y, max_z)
        # return (min_x, min_y, min_z, max_x, max_y, max_z)
