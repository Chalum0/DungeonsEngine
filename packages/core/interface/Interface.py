from packages.core.interface.Button import Button


class Interface:
    def __init__(self, name):
        self.name = name
        self.buttons = {}

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def add_button(self, x, y, width, height, name):
        if name not in self.buttons.keys():
            self.buttons[name](Button(x, y, width, height, name))

    def remove_button(self, name):
        del self.buttons[name]

    def get_click(self, x, y):
        buttons = {}
        for button in self.buttons.keys():
            if self.buttons[button].is_clicked(x, y):
                buttons[button] = True
            else:
                buttons[button] = False
        return buttons

