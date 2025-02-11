from packages.environment.Scene import Scene

class SceneManager:
    def __init__(self):
        self.current_scene = None
        self._scenes = {}

    def ceate_scene(self, name=None):
        if name is None:
            name = f"scene{len(self._scenes)}"
        if not name in self._scenes.keys():
            self._scenes[name] = Scene(name)
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

    def __str__(self):
        return f"{list(self._scenes.keys())}"

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
