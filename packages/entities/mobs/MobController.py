from packages.entities.mobs.Zombie import Zombie


class MobController:
    def __init__(self):
        self.Zombie = Zombie

        self.current_mobs = []

    def spawn_zombie(self, x=0, y=0, z=0) -> None:
        self.current_mobs.append(self.Zombie(x, y, z))

    def kill_zombie(self, zombie) -> None:
        self.current_mobs.remove(zombie)

    def get_all_mobs(self) -> list:
        return self.current_mobs

    def get_mobs_count(self) -> int:
        return len(self.current_mobs)
