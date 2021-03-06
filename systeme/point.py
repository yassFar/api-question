from vector import Vector


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __rsub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __str__(self):
        return "Point, x: " + str(self.x) + ", y: " + str(self.y)

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
