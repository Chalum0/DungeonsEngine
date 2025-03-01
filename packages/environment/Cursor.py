import glfw

class Cursor:
    def __init__(self, window):
        self.window = window

    def get_position(self) -> tuple[float, float]:
        x, y = glfw.get_cursor_pos(self.window)
        return x, y

    def set_position(self, x, y):
        glfw.set_cursor_pos(self.window, x, y)

    def get_pressed(self) -> tuple[bool, bool, bool]:
        return glfw.get_mouse_button(self.window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS, glfw.get_mouse_button(self.window, glfw.MOUSE_BUTTON_MIDDLE) == glfw.PRESS, glfw.get_mouse_button(self.window, glfw.MOUSE_BUTTON_RIGHT) == glfw.PRESS
