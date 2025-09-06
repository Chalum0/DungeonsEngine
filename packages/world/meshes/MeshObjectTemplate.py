from packages.world.ModelManager import ModelManager

class MeshObjectTemplate:
    def __init__(self, model_manager: ModelManager, template_name: str, model_path: str):
        self._model_name = template_name
        self._model_path = model_path
        self._pos = None
        self._all_vertices, self._all_indices = self._load_model()
        self._bounding_box = None

    def instantiate(self):
        self._pos = [0, 0, 0]

    def _load_model(self, model_manager: ModelManager):
        return model_manager.load(self._model_path)

