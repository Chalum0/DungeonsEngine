import glfw
import moderngl

from packages.textures.Textures import Textures


class windowManager:
    def __init__(self):
        self.window_settings = {"use-v-sync": False,
                                "set-cursor-invisible": True,
                                "use-fullscreen": False,
                                "width": 1920,
                                "height": 1080,
                                "title": "Hello world!"}

    def _initialize_opengl(self, settings):

        if not glfw.init():
            raise Exception("GLFW can't be initialized.")

        primary_monitor = glfw.get_primary_monitor()
        video_mode = glfw.get_video_mode(primary_monitor)

        if settings["use-fullscreen"]:
            self.window = glfw.create_window(video_mode.size.width, video_mode.size.height, settings["window-title"], primary_monitor, None)
        else:
            self.window = glfw.create_window(settings["width"], settings["height"], settings["title"], primary_monitor, None)

        if not self.window:
            glfw.terminate()
            raise Exception("GLFW window can't be created.")

        glfw.make_context_current(self.window)  # Bind current context to the window

        if settings["use-v-sync"]:
            glfw.swap_interval(0)  # Disable V-Sync
        if settings["set-cursor-invisible"]:
            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)  # make cursor invisible
        self.ctx = moderngl.create_context()
        self.window_size = glfw.get_window_size(self.window)

    def _load_textures(self):
        texture = Textures(self.ctx)
        texture.get_array().use(location=0)  # Ensure texture unit 0 is used for the texture array

    def _window_should_close(self) -> bool:
        return glfw.window_should_close(self.window)

    @staticmethod
    def _terminate():
        glfw.terminate()

    def set_window_title(self, new_title: str):
        if not type(new_title) == str:
            raise TypeError

        if self.window:
            glfw.set_window_title(self.window, new_title)
        else:
            self.window_settings["title"] = new_title
 