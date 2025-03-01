from packages.environment.CameraManager import CameraManager


class Scene(CameraManager):
    def __init__(self, name):
        CameraManager.__init__(self)
        self.name = name
        self._window = None

    def _rename(self, new_name):
        self.name = new_name

    def _copy(self, scene: object) -> None:
        pass

    def use_window(self, window):
        self._window = window
