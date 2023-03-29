import numpy as np

from src.Point import Point


class Profile:
    def __init__(self, line, spray_heights):
        beta = line.beta
        points = []
        for position, height in zip(line.get_points(), spray_heights):
            x = position.x + height * np.sin(beta)
            y = position.y - height * (1 - np.cos(beta))
            points.append(Point(x, y))

        self.points = points

    def get_points(self):
        return self.points

