class ModelSegment:
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