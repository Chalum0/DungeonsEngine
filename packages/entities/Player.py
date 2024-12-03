from packages.entities.Settings import *
from packages.entities.Entity import *

class Player(Entity):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
