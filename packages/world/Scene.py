from packages.world.EntityTemplateManager import EntityTemplateManager
from packages.world.entities.EntityTemplate import EntityTemplate
from packages.world.entities.ModelManager import ModelManager
from packages.world.CameraManager import CameraManager
from packages.world.EntityManager import EntityManager


class Scene(CameraManager, EntityManager):
    def __init__(self, name, window, entity_template_manager: EntityTemplateManager, model_manager: ModelManager):
        CameraManager.__init__(self)
        EntityManager.__init__(self, model_manager)
        self._entity_templates_manager: EntityTemplateManager = entity_template_manager
        self.name = name
        self._window = window

    def _rename(self, new_name):
        self.name = new_name

    def spawn_entity(self, template_name):
        entity: EntityTemplate = self._entity_templates_manager.get_entity_template_by_name(template_name)
        return self._spawn_entity(entity)


