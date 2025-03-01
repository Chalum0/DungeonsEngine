from packages.environment.entities.Entity import Entity

from math import dist, sqrt


class Zombie(Entity):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.target = None
        self.speed = 1

    def update_ai(self, player, dt):
        self._update_target(player)
        if self.target is not None:
            self._move_to_target(dt)


    def _update_target(self, player):
        if dist(self.pos, player.pos) < 4:
            self.target = player
        elif dist(self.pos, player.pos) > 6:
            self.target = None

    def _move_to_target(self, dt):
        ex, ey, ez = self.pos
        px, py, pz = self.target.pos

        dx = px - ex
        dy = py - ey
        dz = pz - ez

        distance_to_target = sqrt(dx * dx + dy * dy + dz * dz)

        if distance_to_target > 1e-8:
            dx /= distance_to_target
            dy /= distance_to_target
            dz /= distance_to_target

            ex += dx * self.speed * dt
            ey += dy * self.speed * dt
            ez += dz * self.speed * dt

        self.set_position(ex, ey, ez)
