from packages.world.CameraManager import CameraManager
from packages.world.EntityManager import EntityManager


class Scene(CameraManager, EntityManager):
    def __init__(self, name, window):
        CameraManager.__init__(self)
        EntityManager.__init__(self)
        self.name = name
        self._window = window

    def _rename(self, new_name):
        self.name = new_name

    def _copy(self, scene: object) -> None:
        pass
