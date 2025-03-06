import numpy as np
import json


class Models:
    def __init__(self):
        self.models = {
            "cube": self.load("cube")
        }

    def load(self, model):
        mdl = Model(model)
        return mdl.vertices, mdl.indices


# packages/entities/models/

class Model:
    def __init__(self, filename):
        self.filename = f"packages/entities/models/{filename}.json"
        self.segments: list[Segment] = []
        self.vertices = []
        self.indices = []

        self.load()

    def load(self):
        with open(self.filename, "r") as file:
            model_data = json.load(file)["segments"]
        for segment in model_data:
            self.segments.append(Segment(segment))

        for segment in self.segments:
            self.vertices += segment.vertices
            self.indices += segment.indices
        self.vertices = np.array(self.vertices, dtype='f4')
        self.indices = np.array(self.indices, dtype='i4')


class Segment:
    def __init__(self, segment_data):
        self.name = None
        self.sensitive = None
        self.vertices = []
        self.indices = []

        self.load_data(segment_data)

    def load_data(self, segment_data):
        self.name = segment_data["name"]
        self.sensitive = segment_data["sensitive"]

        for face in segment_data["faces"].values():

            # To change pos, these need to be process 3 by 3 (3 modified, 3 untouched)
            self.vertices += face["v"]
            self.indices += face["i"]


entity = Models()
