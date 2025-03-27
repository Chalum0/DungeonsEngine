from packages.entities.Entity import Entity

from math import sqrt


class Mob(Entity):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.target = None
        self.speed = 0

    def update_ai(self, players, dt):
        pass

    def _set_speed(self, speed):
        self.speed = speed

    def _move_to_position(self, x, y, z, dt):
        current_x, current_y, current_z = self.pos
        target_x, target_y, target_z = x, y, z

        vector_x = target_x - current_x
        vector_y = target_y - current_y
        vector_z = target_z - current_z

        distance_to_target = sqrt(vector_x * vector_x + vector_y * vector_y + vector_z * vector_z)

        if distance_to_target > 1e-8:
            vector_x /= distance_to_target
            vector_y /= distance_to_target
            vector_z /= distance_to_target

            current_x += vector_x * self.speed * dt
            current_y += vector_y * self.speed * dt
            current_z += vector_z * self.speed * dt

        self.set_position(current_x, current_y, current_z)


