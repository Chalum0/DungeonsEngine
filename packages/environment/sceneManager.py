from packages.environment.Scene import Scene

class SceneManager:
    def __init__(self):
        self.current_scene: Scene = None
        self._used_window = None
        self._scenes = {}

    def create_scene(self, name=None):
        if name is None:
            name = f"scene{len(self._scenes)}"
        if not name in self._scenes.keys():
            self._scenes[name] = Scene(name, self._used_window)
        else:
            raise SceneAlreadyExists(name)

    def rename_scene(self, scene_name, new_name):
        if scene_name in self._scenes.keys():
            if not new_name in self._scenes.keys():
                self._scenes[new_name] = Scene(new_name)
                self._scenes[new_name]._copy(self._scenes[scene_name])
                del self._scenes[scene_name]
            else:
                raise SceneAlreadyExists(new_name)
        else:
            raise UnknownScene(scene_name)

    def use_scene(self, scene_name):
        if scene_name is None:
            self.current_scene = None
        if scene_name in self._scenes.keys():
            self.current_scene = self._scenes[scene_name]
        else:
            raise UnknownScene(scene_name)

    def _use_window(self, window):
        print("using window 1")
        if self.current_scene is not None:
            self.current_scene.use_window(window)
        self._used_window = window

    def __str__(self):
        return f"{list(self._scenes.keys())}"

    # @property
    # def camera(self):
    #     return self.current_scene._camera
    #
    # @camera.setter
    # def camera(self, new_value):
    #     self.current_scene._camera = new_value

class SceneAlreadyExists(Exception):
    def __init__(self, name):
        super().__init__(
            f'A scene already exists with name "{name}"'
        )

class UnknownScene(Exception):
    def __init__(self, name):
        super().__init__(
            f'No scene found with name "{name}"'
        )
