from packages.world.entities.EntityTemplate import EntityTemplate
from packages.world.entities.ModelManager import ModelManager


class EntityManager:
    def __init__(self):
        self._model_manager = ModelManager()
        self._entities = []
        self._entity_templates = {}

    def create_entity_template(self, template_name, model_name="cube", hidden=False):
        self._entity_templates[template_name] = EntityTemplate(template_name, self._entities, self._model_manager, model_name, hidden)

    def spawn_entity(self, template_name):
        entity: EntityTemplate = self._entity_templates[template_name]
        self._entities.append(entity)
        entity.instanciate()
        return entity

    @property
    def entities(self):
        return self._entities
