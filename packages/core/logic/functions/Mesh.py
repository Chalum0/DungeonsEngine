from numba import njit
import numpy as np


# def create_combined_mesh():
#     all_vertices = np.en
#     return None, None
# @njit()
def create_cube_mesh(center, size, tex_id):
    all_vertices = create_cube_vertices(center, size, tex_id)
    all_indices = np.array([
    # front face
    0, 1, 2, 0, 2, 3,
    # back face
    4, 5, 6, 4, 6, 7,
    # top face
    8, 9, 10, 8, 10, 11,
    # bottom face
    12, 13, 14, 12, 14, 15,
    # right face
    16, 17, 18, 16, 18, 19,
    # left face
    20, 21, 22, 20, 22, 23,
], dtype='i4')
    return all_vertices, all_indices


# @njit()
def create_cube_vertices(center, size, tex_id):
    x, y, z = center
    half = size / 2
    vertices = [

        # font
        x - half, y - half, z + half, 0, 0, tex_id,
        x + half, y - half, z + half, 1, 0, tex_id,
        x + half, y + half, z + half, 1, 1, tex_id,
        x - half, y + half, z + half, 0, 1, tex_id,
        # back
        x - half, y - half, z - half, 1, 0, tex_id,
        x + half, y - half, z - half, 0, 0, tex_id,
        x + half, y + half, z - half, 0, 1, tex_id,
        x - half, y + half, z - half, 1, 1, tex_id,
        # top
        x - half, y + half, z - half, 0, 0, tex_id,
        x + half, y + half, z - half, 1, 0, tex_id,
        x + half, y + half, z + half, 1, 1, tex_id,
        x - half, y + half, z + half, 0, 1, tex_id,
        # bottom
        x - half, y - half, z - half, 1, 1, tex_id,
        x + half, y - half, z - half, 0, 1, tex_id,
        x + half, y - half, z + half, 0, 0, tex_id,
        x - half, y - half, z + half, 1, 0, tex_id,
        # right
        x + half, y - half, z - half, 0, 0, tex_id,
        x + half, y + half, z - half, 0, 1, tex_id,
        x + half, y + half, z + half, 1, 1, tex_id,
        x + half, y - half, z + half, 1, 0, tex_id,
        # left
        x - half, y - half, z - half, 1, 0, tex_id,
        x - half, y + half, z - half, 1, 1, tex_id,
        x - half, y + half, z + half, 0, 1, tex_id,
        x - half, y - half, z + half, 0, 0, tex_id,
    ]

    vertices = np.array(vertices, dtype='f4')
    return vertices
