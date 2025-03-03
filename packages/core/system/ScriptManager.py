from pathlib import Path
import importlib.util
import json
import sys
import os

from packages.core.system.Functions import Functions


class ScriptManager:
    def __init__(self):
        self.folders = []

    def add_folder(self, folder_path):
        self.folders.append(folder_path)

    def explore_folder(self):
        if not self.folders:
            return

        for folder in self.folders:
            path = Path(folder)
            if not path.exists():
                print(f"Warning: Folder does not exist: {path}")
                continue

            self._explore_recursive(path)

    def _explore_recursive(self, folder):
        entries = list(folder.iterdir())

        if (folder / "config.json").exists():
            self._process_model(folder)
        else:
            for entry in entries:
                if entry.is_dir():
                    self._explore_recursive(entry)

    def _process_model(self, model_path):
        config_path = model_path / 'config.json'

        with open(config_path, 'r') as f:
            config = json.load(f)


        functions = Functions()
        for py_file in model_path.rglob("*.py"):
            script_functions = self._load_script(py_file, config["name"])
            for name, attr in script_functions:
                setattr(functions, name, attr)

        if callable(getattr(functions, 'main', None)):
            functions.main(functions)

    def _load_script(self, script_path, model_name):
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

