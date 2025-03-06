from packages.world.EntityTemplateManager import EntityTemplateManager
from packages.world.Functions import Functions

from pathlib import Path
import importlib.util
import json
import os

class ScriptManager(EntityTemplateManager):
    def __init__(self):
        EntityTemplateManager.__init__(self)
        self._folders = []

    def add_script_folder(self, folder_path):
        self._folders.append(folder_path)

    def _load_models(self):
        self.models = []

        for folder in self._folders:
            path = Path(folder)
            if not path.exists():
                print(f"Warning: Folder does not exist: {path}")
                continue

            self.models += self._explore_recursive(path)

        for model in self.models:
            template = self.create_entity_template(model["name"], model["path"])
            if model["functions"].main:
                template.set_on_update_callback(model["functions"].main)
            # model["functions"].greetings()

    def _explore_recursive(self, folder) -> list:
        entries = list(folder.iterdir())

        models = []

        if (folder / "config.json").exists():
            models.append(self._process_model(folder))
        else:
            for entry in entries:
                if entry.is_dir():
                    self._explore_recursive(entry)
        return models

    def _process_model(self, model_path) -> Functions:
        config_path = model_path / 'config.json'

        with open(config_path, 'r') as f:
            config = json.load(f)


        functions = Functions()
        model = config
        for py_file in model_path.rglob("*.py"):
            script_functions = self._load_script(py_file, config["name"])
            for name, attr in script_functions:
                setattr(functions, name, attr)
        model["functions"] = functions
        model["path"] = model_path
        return model

        # if callable(getattr(functions, 'main', None)):
        #     functions.main(functions)

    def _load_script(self, script_path, model_name) -> list:
        if not os.path.isfile(script_path):
            raise FileNotFoundError(f"Script not found at: {script_path}")

        spec = importlib.util.spec_from_file_location(model_name, script_path)
        module = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(module)

        functions = []
        for name in dir(module):
            if name.startswith("__"):
                continue

            attr = getattr(module, name)
            if callable(attr):
                functions.append((name, attr))

        return functions

