from packages.controllers.Settings import *
import glfw

class Controls:
    def __init__(self, window):
        self.window = window

    def get_pressed(self):
        ks = {}
        for key in keys.keys():
            if glfw.get_key(self.window, keys[key]) == glfw.PRESS:
                ks[key] = True
            else:
                ks[key] = False

        return ks
