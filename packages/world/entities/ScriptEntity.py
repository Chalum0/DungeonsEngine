class ScriptEntity:
    def __init__(self, template):
        self._template = template

    @property
    def pos(self):
        return self._template._pos
    @pos.setter
    def pos(self, position):
        self._template.set_position(position[0], position[1], position[2])
    def translate(self, dx, dy, dz):
        self._template.translate(dx, dy, dz)

    @property
    def other_entities(self):
        return self._template._all_entities

    @property
    def name(self):
        return self._template._name

    @property
    def hidden(self):
        return self._template._hidden
    def show(self):
        self._template.show()
    def hide(self):
        self._template.hide()

    @property
    def bounding_box(self):
        return self._template._bounding_box
