from packages.world.entities.EntityTemplate import EntityTemplate

class EntityTemplateManager:
    def __init__(self):
        self._entity_templates = {}

    def create_entity_template(self, template_name, model_name="cube", hidden=False):
        self._entity_templates[template_name] = EntityTemplate(template_name, model_name, hidden)

    def get_entity_template_by_name(self, template_name):
        return self._entity_templates[template_name]
