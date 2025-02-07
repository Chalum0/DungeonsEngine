from packages.entities.mobs.MobController import MobController
from packages.textures.text.Text import Text
from packages.entities.Entity import Entity
from packages.entities.Player import Player
from packages.shaders.Shader import Shader
from packages.controllers import Controls
from packages.textures.Textures import *
from packages.entities.Settings import *
from packages.controllers import Camera
from packages.logic.Clock import Clock
from packages.tkinter.app import *

from pyrr import Matrix44
import moderngl
import random
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
        self.mob_controller = MobController()
        for i in range(1):
            self.mob_controller.spawn_zombie(2, 0, 2)

        self.controls = Controls.Controls(self.window)
        self.camera = Camera.Camera(self.window_size[0], self.window_size[1], self.window, self.player)
        self.text = Text(self.ctx, self.window_size)
        self.text.load_font("Minecraft")
        glfw.set_scroll_callback(self.window, self.scroll_callback)

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
            self.movements()

            self.shared_data["fps"] = self.clock.fps
            self.shared_data["coords"] = (self.camera.pos[0], self.camera.pos[1], self.camera.pos[2])
            self.shared_data["yaw"] = self.camera.yaw
            self.shared_data["pitch"] = self.camera.pitch
            self.shared_data["mob_count"] = self.mob_controller.get_mobs_count()

            self.ctx.screen.use()
            self.ctx.clear(0.05, 0.05, 0.1)
            self.ctx.enable(moderngl.DEPTH_TEST)

            self.tasks()
            self.render()

            glfw.swap_buffers(self.window)
            glfw.poll_events()

    def movements(self):
        dt = self.clock.dt
        player = self.player
        camera = self.camera
        keys = self.controls.get_pressed()


        if keys["FORWARDS"]:
            camera.move_forwards(dt)
        if keys["BACKWARDS"]:
            camera.move_backwards(dt)
        if keys["LEFT"]:
            camera.move_left(dt)
        if keys["RIGHT"]:
            camera.move_right(dt)

        if keys["P_FORWARDS"]:
            player.translate(0, 0, -8*dt)
            camera.move_forwards(dt)
        if keys["P_BACKWARDS"]:
            player.translate(0, 0, 8*dt)
            camera.move_backwards(dt)
        if keys["P_LEFT"]:
            player.translate(-8*dt, 0, 0)
            camera.move_left(dt)
        if keys["P_RIGHT"]:
            player.translate(8*dt, 0, 0)
            camera.move_right(dt)

        if keys["P_R_F"]:
            player.rotate(0, 1*dt, 0)
        if keys["P_R_B"]:
            player.rotate(0, -1*dt, 0)

    def tasks(self):
        if self.mob_controller.get_mobs_count() <= 100:
            for mob in self.mob_controller.get_all_mobs():
                mob.update_ai(self.player, self.clock.dt)
                if self.player.collides_with(mob):
                    self.mob_controller.kill_zombie(mob)
                    self.mob_controller.spawn_zombie(random.randint(-2, 2), 0, random.randint(-2, 2))
                    # self.mob_controller.spawn_zombie(random.randint(-2, 2), 0, random.randint(-2, 2))
        pass

    def render(self):
        view = self.camera.update(self.clock.dt)
        proj = Matrix44.perspective_projection(45.0, self.window_size[0] / self.window_size[1], 0.1, 1000.0)

        for entity in [self.player] + self.mob_controller.get_all_mobs():
            if entity.get_vertex_object()["vao"] is not None:
                # entity.get_vertex_object()["vao"].program["model"].write(Matrix44.identity().astype("f4").tobytes())
                entity.get_vertex_object()["vao"].program["model"].write(entity.model.astype("f4").tobytes())
                entity.get_vertex_object()["vao"].program["view"].write(view.astype("f4").tobytes())
                entity.get_vertex_object()["vao"].program["proj"].write(proj.astype("f4").tobytes())
                entity.get_vertex_object()["vao"].render(moderngl.TRIANGLES, vertices=entity.get_vertices_amount())
            else:
                entity.create_object(self.ctx, self.shader)

    def terminate(self):
        glfw.terminate()

    # ---------------------------------------------------------------------------------------------------------------------------------

    def scroll_callback(self, window, xoffset, yoffset):
        """Scroll wheel callback - pass scroll input on to the camera."""
        self.camera.on_scroll(yoffset)


if __name__ == "__main__":
    shared_data = {"fps": 0, "coords": (0, 0, 0), "yaw": 0, "pitch": 0, "mob_count": 0}
    debug_app(shared_data)
    main = Main()
