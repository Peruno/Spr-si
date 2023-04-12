import numpy as np

from src.Point import Point


class Profile:
    def __init__(self, line, spray_heights):
        if len(line.get_points()) != len(spray_heights):
            raise Exception("The number of points in the line the the number of values for the spray_heights do not "
                            "match")

        beta = line.get_angle()
        points = []
        for position, spray_height in zip(line.get_points(), spray_heights):
            x = position.x + spray_height * np.sin(beta)
            y = position.y + spray_height * np.cos(beta)
            points.append(Point(x, y))

        self.points = points
        self.integral = Profile._calculate_integral(line, spray_heights)

    def get_points(self):
        return self.points

    def get_x_values(self):
        return [point.x for point in self.get_points()]

    def get_y_values(self):
        return [point.y for point in self.get_points()]

    def get_integral(self):
        return self.integral

    @staticmethod
    def _calculate_integral(line, spray_heights):
        """Returns the area between the upper limit of the spray and the line on which it has been sprayed on."""

        integral = 0
        x_values = line.get_x_values()

        for i in range(len(spray_heights) - 1):
            average_height = (spray_heights[i] + spray_heights[i+1]) / 2
            x_distance = x_values[i + 1] - x_values[i]
            integral += average_height * x_distance

        return integral
