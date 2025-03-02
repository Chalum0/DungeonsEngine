from packages.environment.entities.Model import Model

class ModelManager:
    def __init__(self):
        self._models = {}

    def load(self, model_path):
        if model_path in self._models.keys():
            model = self._models[model_path]
            return model.vertices, model.indices
        else:
            model = Model(model_path)
            self._models[model_path] = model
            return model.vertices, model.indices
