import numpy as np

class BoundingBox:
    def __init__(self):
        self.min = None
        self.max = None

    def update(self, vertices):
        self._create_bounding_box(vertices)

    def update_with_min_max(self, min_x, min_y, min_z, max_x, max_y, max_z):
        self.min = (min_x, min_y, min_z)
        self.max = (max_x, max_y, max_z)

    def collides_with(self, bb) -> bool:
        for i in range(3):
            if self.max[i] < bb.min[i] or bb.max[i] < self.min[i]:
                return False
        return True

    def _create_bounding_box(self, vertices):
        arr = np.array(vertices).reshape(-1, 3)

        min_x = np.min(arr[:, 0])
        min_y = np.min(arr[:, 1])
        min_z = np.min(arr[:, 2])

        max_x = np.max(arr[:, 0])
        max_y = np.max(arr[:, 1])
        max_z = np.max(arr[:, 2])

        self.min = [min_x, min_y, min_z]
        self.max = [max_x, max_y, max_z]
