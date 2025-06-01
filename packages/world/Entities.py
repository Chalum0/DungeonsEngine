from packages.world.entities.EntityTemplate import EntityTemplate
from numba.experimental import jitclass
from numba import njit, types
from math import sin, cos
import numpy as np
import time

entity_spec = [
    ("id", types.int32),
    ("hidden", types.bool),

    ("pos", types.float32[:]),
    ("rotation", types.float32[:]),
    ("model", types.float32[:, :]),
    ("dirty", types.boolean),
]



@jitclass(entity_spec)
class Entity:
    def __init__(self, eid, hidden: bool=False):
        self.id = eid
        self.hidden = hidden
        self.pos = np.zeros(3, dtype=np.float32)
        self.rotation = np.zeros(3, dtype=np.float32)
        self.model = np.eye(4, dtype=np.float32)
        self.dirty = True
        self._update_model()
        self._update_prog = False

    def __str__(self):
        return f"id: {self.id}, hidden: {self.hidden}, pos: {self.pos}, rotation: {self.rotation}, model: {self.model}"

    def hide(self):
        self.hidden = True
    def show(self):
        self.hidden = False
    def toggle_hidden(self):
        self.hidden = not self.hidden

    # def _update_model(self):
    #     self.model[0:3, 3] = self.pos

    def set_pos(self, x, y, z):
        self.pos[0], self.pos[1], self.pos[2] = x, y, z
        self.dirty = True

    def translate(self, dx, dy, dz):
        self.pos[0] += dx
        self.pos[1] += dy
        self.pos[2] += dz
        self.dirty = True

    def _update_model(self):
        if self.dirty:
            _fill_model(self.pos, self.rotation, self.model)
            self.dirty = False
            self._update_prog = True


    def _calculate_model_matrix(self):
        self._update_model()
        return self.model

    def get_pos(self):
        return self.pos

    def get_model(self):
        return self.model







@njit(inline='always', fastmath=True, cache=True)
def _fill_model(pos, rot, out):
    rx, ry, rz = rot[0], rot[1], rot[2]
    sx, cx = sin(rx), cos(rx)
    sy, cy = sin(ry), cos(ry)
    sz, cz = sin(rz), cos(rz)

    # Row 0
    out[0, 0] = cy * cz
    out[0, 1] = sx * sy * cz + cx * sz
    out[0, 2] = -cx * sy * cz + sx * sz
    out[0, 3] = 0.0

    # Row 1
    out[1, 0] = -cy * sz
    out[1, 1] = -sx * sy * sz + cx * cz
    out[1, 2] = cx * sy * sz + sx * cz
    out[1, 3] = 0.0

    # Row 2
    out[2, 0] = sy
    out[2, 1] = -sx * cy
    out[2, 2] = cx * cy
    out[2, 3] = 0.0

    # Row 3 <= translation
    out[3, 0] = pos[0]
    out[3, 1] = pos[1]
    out[3, 2] = pos[2]
    out[3, 3] = 1.0

















my_entity = Entity(0)

@njit
def test_entity(entity: Entity):
    for i in range(1):
        entity.translate(1, 1, 1)
        entity._calculate_model_matrix()

def test_2(entities):
    for entity in entities:
        test_entity(entity)


start = time.time()
print(f"Compiling...")
test_entity(my_entity)
_fill_model(my_entity.pos, my_entity.rotation, my_entity.model)
print(f"Compiled in {time.time() - start}")
print(f"Running compiled test...")
start = time.time()
test_entity(my_entity)
print(f"Ran in {time.time() - start}")

my_entities = [Entity(1, ) for i in range(100_000)]
my_entities_array = np.array(my_entities)
start = time.time()
test_2(my_entities_array)
print(f"Ran in {time.time() - start}")


# my_entity.set_pos(2, 0, 0)
# my_entity.rotation[2] = -10.0
# my_second_entity = EntityTemplate('h', 'h')
# my_second_entity.instenciate(None, None)
# my_second_entity.set_position(2, 0, 0)
# my_second_entity._rotation[1] = 10.0
# print(my_second_entity._calculate_model_matrix() == my_entity._calculate_model_matrix())
# print(my_second_entity._calculate_model_matrix(), "|", my_entity._calculate_model_matrix())

print(my_entity)
