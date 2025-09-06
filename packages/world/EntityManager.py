from packages.world.ModelManager import ModelManager


class EntityManager:
    def __init__(self, model_manager: ModelManager):
        self._model_manager = model_manager
        self._entities = []

    def _spawn_entity(self, entity):
        self._entities.append(entity)
        entity.instantiate(self._entities, self._model_manager)
        return entity

    def update_entities(self):
        for entity in self.entities:
            entity.update()

    def get_times(self):
        entity_time = []
        callback_time = []
        position_update_times = []
        for entity in self.entities:
            if entity.entity_creation_times != []:
                entity_time.append(sum(entity.entity_creation_times) / len(entity.entity_creation_times))
                callback_time.append(sum(entity.callback_functions_times) / len(entity.callback_functions_times))
                position_update_times.append(sum(entity.position_update_times) / len(entity.position_update_times))

        return sum(entity_time) / len(entity_time), sum(callback_time) / len(callback_time), sum(position_update_times) / len(position_update_times)

    @property
    def entities(self):
        return self._entities
