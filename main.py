from packages.controllers import Camera, Controls
from packages.textures.text.Text import Text
from packages.entities.Player import Player
from packages.shaders.Shader import Shader
from packages.textures.Textures import *
from packages.entities.Settings import *
from packages.logic.Clock import Clock
from packages.tkinter.app import *

from pyrr import Matrix44
import moderngl
import time
import glfw

class Main:
    def __init__(self):
        global shared_data
        self.shared_data: dict = shared_data
        self.window_size = (0, 0)
        self.window = None
        self.ctx = None

        self.initialize_opengl()
        self.load_textures()

        self.shader = Shader()

        self.clock = Clock()
        self.player = Player(player_spawn_point_x, player_spawn_point_y, player_spawn_point_z)
        self.entities = [self.player]
        self.camera = Camera.Camera(self.window_size[0], self.window_size[1], self.window, self.player)
        self.text = Text(self.ctx, self.window_size)
        self.text.load_font("Minecraft")

        self.loop()
        self.terminate()

    def initialize_opengl(self):
        if not glfw.init():
            raise Exception("GLFW can't be initialized.")

        primary_monitor = glfw.get_primary_monitor()
        video_mode = glfw.get_video_mode(primary_monitor)
        self.window = glfw.create_window(video_mode.size.width, video_mode.size.height, "Textured Cubes",
                                         primary_monitor, None)
        if not self.window:
            glfw.terminate()
            raise Exception("GLFW window can't be created.")

        glfw.make_context_current(self.window)  # Bind current context to the window
        glfw.swap_interval(0)  # Disable V-Sync
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)  # make cursor invisible
        self.ctx = moderngl.create_context()
        self.window_size = glfw.get_window_size(self.window)

    def load_textures(self):
        # Load texture
        texture = Textures(self.ctx)
        texture.get_array().use(location=0)  # Ensure texture unit 0 is used for the texture array

    def loop(self):
        while not glfw.window_should_close(self.window):
            self.clock.tick()

            self.shared_data["fps"] = self.clock.fps
            self.shared_data["coords"] = (self.camera.pos[0], self.camera.pos[1], self.camera.pos[2])

            self.ctx.screen.use()
            self.ctx.clear(0.05, 0.05, 0.1)
            self.ctx.enable(moderngl.DEPTH_TEST)

            self.tasks()
            self.render()

            glfw.swap_buffers(self.window)
            glfw.poll_events()


    def tasks(self):
        pass

    def render(self):
        view = self.camera.update(self.clock.dt)
        proj = Matrix44.perspective_projection(45.0, self.window_size[0] / self.window_size[1], 0.1, 1000.0)

        for entity in self.entities:
            if entity.get_vertex_object()["vao"] is not None:
                entity.get_vertex_object()["vao"].program["model"].write(Matrix44.identity().astype("f4").tobytes())
                entity.get_vertex_object()["vao"].program["view"].write(view.astype("f4").tobytes())
                entity.get_vertex_object()["vao"].program["proj"].write(proj.astype("f4").tobytes())
                entity.get_vertex_object()["vao"].render(moderngl.TRIANGLES, vertices=entity.get_vertices_amount())
            else:
                entity.create_object(self.ctx, self.shader)

    def terminate(self):
        glfw.terminate()


if __name__ == "__main__":
    shared_data = {"fps": 0, "coords": (0, 0, 0)}
    debug_app(shared_data)
    main = Main()
