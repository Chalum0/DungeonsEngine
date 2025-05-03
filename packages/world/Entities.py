from numba import njit
import numpy as np
from pyrr import Vector3, Matrix44
import time


MAX_ENTITIES = 1_000_000

names = np.zeros(MAX_ENTITIES, dtype=np.str_)
model_paths = np.zeros(MAX_ENTITIES, dtype=np.str_)
hidden = np.zeros(MAX_ENTITIES, dtype=np.bool)

positions = np.zeros((MAX_ENTITIES, 3), dtype=Vector3)
rotations = np.zeros((MAX_ENTITIES, 3), dtype=Vector3)
model_matrices = np.zeros((MAX_ENTITIES, 4, 4), dtype=np.float32)

vbos = np.zeros(MAX_ENTITIES, dtype=np.uint32)
ibos = np.zeros(MAX_ENTITIES, dtype=np.uint32)
vaos = np.zeros(MAX_ENTITIES, dtype=np.uint32)

programs = []
program_indices = np.zeros(MAX_ENTITIES, dtype=np.int32)

