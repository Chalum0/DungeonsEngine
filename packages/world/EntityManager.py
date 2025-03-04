from packages.world.entities.EntityTemplate import EntityTemplate
from packages.world.entities.ModelManager import ModelManager


class EntityManager:
    def __init__(self, model_manager: ModelManager):
        self._model_manager = ModelManager()
        self._entities = []

    def _spawn_entity(self, entity):
        self._entities.append(entity)
        entity.instanciate(self._entities, self._model_manager)
        return entity

    @property
    def entities(self):
        return self._entities
