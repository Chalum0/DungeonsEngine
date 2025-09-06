import glfw
import moderngl

from packages.world.Cursor import Cursor
from packages.core.textures.Textures import Textures
from packages.core.shaders.Shader import Shader


class WindowManager:
    def __init__(self):
        self.window_settings = {"use-v-sync": False,
                                "set-cursor-invisible": True,
                                "use-fullscreen": False,
                                "width": 1920,
                                "height": 1080,
                                "title": "Hello world!"}

    # def _initialize_opengl(self, settings):
    #
    #     if not glfw.init():
    #         raise Exception("GLFW can't be initialized.")
    #
    #     primary_monitor = glfw.get_primary_monitor()
    #     video_mode = glfw.get_video_mode(primary_monitor)
    #
    #     if settings["use-fullscreen"]:
    #         self.window = glfw.create_window(video_mode.size.width, video_mode.size.height, settings["window-title"], primary_monitor, None)
    #     else:
    #         self.window = glfw.create_window(settings["width"], settings["height"], settings["title"], primary_monitor, None)
    #
    #     if not self.window:
    #         glfw.terminate()
    #         raise Exception("GLFW window can't be created.")
    #
    #     glfw.make_context_current(self.window)  # Bind current context to the window
    #
    #     if settings["use-v-sync"]:
    #         glfw.swap_interval(0)  # Disable V-Sync
    #     if settings["set-cursor-invisible"]:
    #         glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)  # make cursor invisible
    #     self.ctx = moderngl.create_context()
    #     self.window_size = glfw.get_window_size(self.window)
    #
    #     self.cursor = Cursor(self.window)

    def _initialize_opengl(self, settings):
        if not glfw.init():
            raise Exception("GLFW can't be initialized.")

        glfw.window_hint(glfw.CLIENT_API, glfw.OPENGL_API)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)

        primary_monitor = glfw.get_primary_monitor()
        video_mode = glfw.get_video_mode(primary_monitor)

        title = settings.get("title") or settings.get("window-title") or "My App"

        if settings["use-fullscreen"]:
            self.window = glfw.create_window(
                video_mode.size.width, video_mode.size.height, title, primary_monitor, None
            )
        else:
            self.window = glfw.create_window(
                settings["width"], settings["height"], title, None, None
            )

        if not self.window:
            glfw.terminate()
            raise Exception("GLFW window can't be created.")

        glfw.make_context_current(self.window)

        glfw.swap_interval(1 if settings.get("use-v-sync", True) else 0)

        if settings.get("set-cursor-invisible"):
            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

        self.ctx = moderngl.create_context(require=330)

        fb_w, fb_h = glfw.get_framebuffer_size(self.window)
        self.window_size = (fb_w, fb_h)

        self.cursor = Cursor(self.window)

    def _load_textures(self):
        texture = Textures(self.ctx)
        texture.get_array().use(location=0)  # Ensure texture unit 0 is used for the texture array

    def _load_shaders(self):
        self.shader = Shader()

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
 