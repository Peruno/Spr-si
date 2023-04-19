class Point:
    def __init__(self, x, y, beta=None):
        self.x = x
        self.y = y
        self.beta = beta

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y
