from packages.world.ModelManager import ModelManager
from packages.world.meshes.MeshObjectTemplate import MeshObjectTemplate


class MeshManager:
    def __init__(self):
        self._model_manager: ModelManager = None
        self._meshes = {}
        self._templates = {}

    def create_template(self, model_name):
        self._templates[model_name] = MeshObjectTemplate(self._model_manager, model_name)

    def create_mesh(self, name):
        pass
        # self._meshes = self._templates[name]

    def get_mesh(self, name):
        return self._meshes[name]


