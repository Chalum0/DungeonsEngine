from packages.world.entities.EntityTemplate import EntityTemplate

class EntityTemplateManager:
    def __init__(self):
        self._entity_templates = {}

    def create_entity_template(self, template_name, model_name, hidden=False) -> EntityTemplate:
        if not template_name in self._entity_templates.keys():
            self._entity_templates[template_name] = EntityTemplate(template_name, model_name, hidden)
            return self._entity_templates[template_name]
        else:
            raise EntityTemplateAlreadyExists(template_name)

    def get_entity_template_by_name(self, template_name):
        return self._entity_templates[template_name]


class EntityTemplateAlreadyExists(Exception):
    def __init__(self, template_name):
        super().__init__(f'Entity Template with name "{template_name}" already exists.')
