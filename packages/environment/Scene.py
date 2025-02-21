class Scene:
    def __init__(self, name):
        self.name = name
        self._camera = None
        self._cameras = []

    def _rename(self, new_name):
        self.name = new_name

    def _copy(self, scene: object) -> None:
        pass
