from packages.world.entities.ModelSegment import ModelSegment

import numpy as np
import json

class Model:
    def __init__(self, model_path):
        self.model_path = model_path
        self.segments: list[ModelSegment] = []
        self.vertices = []
        self.indices = []

        self.load()

    def load(self):
        try:
            with open(self.model_path, "r") as file:
                model_data = json.load(file)["segments"]
            for segment in model_data:
                self.segments.append(ModelSegment(segment))

            for segment in self.segments:
                self.vertices += segment.vertices
                self.indices += segment.indices
            self.vertices = np.array(self.vertices, dtype='f4')
            self.indices = np.array(self.indices, dtype='i4')
        except Exception as e:
            raise ModelLoadingError(self.model_path, e)


class ModelLoadingError(Exception):
    def __init__(self, model_name, error):
        super().__init__(
            f'Unable to load model "{model_name}": {error}'
        )