import glfw


class Controls:
    def __init__(self, window):
        self.window = window

    def get_mouse_position(self):
        x, y = glfw.get_cursor_pos(self.window)
        return x, y

    def set_mouse_position(self, x, y):
        glfw.set_cursor_pos(self.window, x, y)

