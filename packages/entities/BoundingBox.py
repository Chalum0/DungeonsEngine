class BoundingBox:
    def __init__(self):
        def __init__(self, min_point, max_point):
            self.min = min_point  # [x_min, y_min, z_min]
            self.max = max_point  # [x_max, y_max, z_max]

        def update(self, position):
            # Update the bounding box based on the entity's position
            self.min = [self.min[i] + position[i] for i in range(3)]
            self.max = [self.max[i] + position[i] for i in range(3)]