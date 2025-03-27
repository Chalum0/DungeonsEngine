from packages.core.system.WindowManager import WindowManager
from packages.world.SceneManager import SceneManager

from packages.core.logic.Clock import Clock

from pyrr import Matrix44
import moderngl
import glfw

class Engine(WindowManager, SceneManager):
    def __init__(self):
        SceneManager.__init__(self)
        WindowManager.__init__(self)
        self.on_load = None
        self.on_loaded = None
        self.on_shutdown = None
        self.on_frame = None
    def run(self):
        if self.on_load:
            self.on_load()
        self._initialize_opengl(settings=self.window_settings)
        self._load_shaders()
        self._load_textures()
        self._load_models()
        if self.on_loaded:
            self.on_loaded(self)
        self._run_loop()
        self._terminate()

    def run_logic_only(self):
        print('Running in logic-only mode.')
        if self.on_load:
            self.on_load()
        print('Loaded user on_load().')
        self._load_models()
        print('Loaded model.')
        if self.on_loaded:
            self.on_loaded(self)
        print('Loaded user on_loaded().')
        print('Starting loop. Ctrl+c to stop.\n')
        self._run_logic_loop()

    def _run_logic_loop(self):
        print("Running...")
        self.clock = Clock()

        while True:
            self.clock.tick()
            self.update()

    def _run_loop(self):
        self.clock = Clock()
        while not self._window_should_close():
            self.clock.tick()
            # self.movements()

            # self.shared_data["fps"] = self.clock.fps
            # self.shared_data["coords"] = (self.camera.pos[0], self.camera.pos[1], self.camera.pos[2])
            # self.shared_data["yaw"] = self.camera.yaw
            # self.shared_data["pitch"] = self.camera.pitch
            # self.shared_data["mob_count"] = self.mob_controller.get_mobs_count()

            self.ctx.screen.use()
            self.ctx.clear(0.05, 0.05, 0.1)
            self.ctx.enable(moderngl.DEPTH_TEST)

            self.update()
            self.render()

            glfw.swap_buffers(self.window)
            glfw.poll_events()

    def update(self):
        for entity in self.current_scene.entities:
            entity.update()

    def render(self):
        if self.current_scene is not None:
            if self.current_scene.camera is not None:

                view = self.current_scene.camera.update(self.clock.dt, self.window_size[0], self.window_size[1], self.cursor)
                proj = Matrix44.perspective_projection(45.0, self.window_size[0] / self.window_size[1], 0.1, 1000.0)

                for entity in self.current_scene.entities:
                    if entity.get_vertex_object()["vao"] is not None:
                        entity.get_vertex_object()["vao"].program["model"].write(entity.model.astype("f4").tobytes())
                        entity.get_vertex_object()["vao"].program["view"].write(view.astype("f4").tobytes())
                        entity.get_vertex_object()["vao"].program["proj"].write(proj.astype("f4").tobytes())
                        entity.get_vertex_object()["vao"].render(moderngl.TRIANGLES, vertices=entity.get_vertices_amount())
                    else:
                        entity.create_object(self.ctx, self.shader)

    def quit(self):
        self._terminate()


#     def __init__(self):
#         # global shared_data
#         # self.shared_data: dict = {}
#
#         self.on_load = None
#         self.on_shutdown = None
#         self.on_update = None
#
#         self.window_size = (0, 0)
#         self.window = None
#         self.ctx = None
#
#         self.initialize_opengl()
#         self.load_textures()
#
#         self.shader = Shader()
#
#         self.clock = Clock()
#         self.player = Player(player_spawn_point_x, player_spawn_point_y, player_spawn_point_z)
#         self.mob_controller = MobController()
#         for i in range(1):
#             self.mob_controller.spawn_zombie(2, 0, 2)
#
#         self.controls = Controls.Controls(self.window)
#         self.camera = Camera.Camera(self.window_size[0], self.window_size[1], self.window, self.player)
#         # self.text = Text(self.ctx, self.window_size)
#         # self.text.load_font("Minecraft")
#         glfw.set_scroll_callback(self.window, self.scroll_callback)

pass

#     def initialize_opengl(self):
#         if not glfw.init():
#             raise Exception("GLFW can't be initialized.")
#
#         primary_monitor = glfw.get_primary_monitor()
#         video_mode = glfw.get_video_mode(primary_monitor)
#         self.window = glfw.create_window(video_mode.size.width, video_mode.size.height, "Textured Cubes",
#                                          primary_monitor, None)
#         if not self.window:
#             glfw.terminate()
#             raise Exception("GLFW window can't be created.")
#
#         glfw.make_context_current(self.window)  # Bind current context to the window
#         glfw.swap_interval(0)  # Disable V-Sync
#         glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)  # make cursor invisible
#         self.ctx = moderngl.create_context()
#         self.window_size = glfw.get_window_size(self.window)

pass

#     def load_textures(self):
#         # Load texture
#         texture = Textures(self.ctx)
#         texture.get_array().use(location=0)  # Ensure texture unit 0 is used for the texture array

pass

#     def run(self):
#         self.on_load_exec()
#         self.loop()
#         self.terminate()
#
#     def set_on_load(self, on_load):
#         self.on_load = on_load
#
#     def on_load_exec(self):
#         if self.on_load is not None:
#             self.on_load()

pass

#     def loop(self):
#         while not glfw.window_should_close(self.window):
#             self.clock.tick()
#             self.movements()
#
#             # self.shared_data["fps"] = self.clock.fps
#             # self.shared_data["coords"] = (self.camera.pos[0], self.camera.pos[1], self.camera.pos[2])
#             # self.shared_data["yaw"] = self.camera.yaw
#             # self.shared_data["pitch"] = self.camera.pitch
#             # self.shared_data["mob_count"] = self.mob_controller.get_mobs_count()
#
#             self.ctx.screen.use()
#             self.ctx.clear(0.05, 0.05, 0.1)
#             self.ctx.enable(moderngl.DEPTH_TEST)
#
#             self.tasks()
#             self.render()
#
#             glfw.swap_buffers(self.window)
#             glfw.poll_events()

pass

#     def movements(self):
#         dt = self.clock.dt
#         player = self.player
#         camera = self.camera
#         keys = self.controls.get_pressed()
#
#
#         if keys["FORWARDS"]:
#             camera.move_forwards(dt)
#         if keys["BACKWARDS"]:
#             camera.move_backwards(dt)
#         if keys["LEFT"]:
#             camera.move_left(dt)
#         if keys["RIGHT"]:
#             camera.move_right(dt)
#
#         if keys["P_FORWARDS"]:
#             player.translate(0, 0, -8*dt)
#             camera.move_forwards(dt)
#         if keys["P_BACKWARDS"]:
#             player.translate(0, 0, 8*dt)
#             camera.move_backwards(dt)
#         if keys["P_LEFT"]:
#             player.translate(-8*dt, 0, 0)
#             camera.move_left(dt)
#         if keys["P_RIGHT"]:
#             player.translate(8*dt, 0, 0)
#             camera.move_right(dt)
#
#         if keys["P_R_F"]:
#             player.rotate(0, 1*dt, 0)
#         if keys["P_R_B"]:
#             player.rotate(0, -1*dt, 0)

pass

#     def tasks(self):
#         if self.mob_controller.get_mobs_count() <= 100:
#             for mob in self.mob_controller.get_all_mobs():
#                 mob.update_ai(self.player, self.clock.dt)
#                 if self.player.collides_with(mob):
#                     self.mob_controller.kill_zombie(mob)
#                     self.mob_controller.spawn_zombie(random.randint(-2, 2), 0, random.randint(-2, 2))
#                     # self.mob_controller.spawn_zombie(random.randint(-2, 2), 0, random.randint(-2, 2))
#         pass

pass

#     def terminate(self):
#         glfw.terminate()
#
#     # ---------------------------------------------------------------------------------------------------------------------------------
#
#     def scroll_callback(self, window, xoffset, yoffset):
#         """Scroll wheel callback - pass scroll input on to the camera."""
#         self.camera.on_scroll(yoffset)
