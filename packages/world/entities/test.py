from numba.experimental import jitclass
from numba import int32, float64, njit
import time

spec = [
    ('x', int32),
    ('y', int32),
]

@jitclass(spec)
class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_x_y(self):
        return self.x, self.y

    def move_x(self, amount):
        self.x += amount

    def move_y(self, amount):
        self.y += amount


@njit
def test(entity):
    for i in range(1000000):
        a = entity.get_x_y()
        entity.move_x(1)
        entity.move_y(1)


def test2(entity):
    for i in range(1000000):
        a = entity.get_x_y()
        entity.move_x(1)
        entity.move_y(1)


my_entity = Entity(1, 1)
start = time.time()
print(f"Compiling...")
test(my_entity)
print(f"Compiled in {time.time()-start}s")
print(f"Running compiled version...")
start = time.time()
test(my_entity)
print(f"Ran in {time.time()-start}s")
print(f"Running python version...")
start = time.time()
test2(my_entity)
print(f"Ran in {time.time()-start}s")

