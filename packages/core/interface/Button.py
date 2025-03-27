class Button:
    def __init__(self, x, y, width, height, name):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def is_clicked(self, x, y):
        if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
            return True
        return False
