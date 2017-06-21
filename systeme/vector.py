class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y

    def __str__(self):
        print self.x, self.y
        return "Vector, x: " + str(self.x) + ", y: " + str(self.y)
