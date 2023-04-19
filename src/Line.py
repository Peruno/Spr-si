import numpy as np

from src.Point import Point


class Line:
    """The angle beta is defined w.r.t. the horizontal plane. Positive means that a ball would
    roll down to the right. Negative means a ball would roll down to the left. It can take values
    from -pi/2 to +pi/2."""

    def __init__(self, start, end, number_of_points=1000):
        if start == end:
            raise Exception("Startpoint and endpoint need to be different.")

        if end.x < start.x:
            raise Exception("Endpoint should be right of startpoint.")

        if number_of_points < 2:
            raise Exception("A line must consist of at least 2 points.")

        self.start_point = start
        self.end_point = end
        self.beta = self.__calculate_angle()
        self.points = self.__initialize_points(number_of_points)

    def get_angle(self):
        return self.beta

    def get_points(self):
        return self.points

    def get_x_values(self):
        return [point.x for point in self.points]

    def get_y_values(self):
        return [point.y for point in self.points]

    def __calculate_angle(self):
        x_diff = self.end_point.x - self.start_point.x
        y_diff = self.end_point.y - self.start_point.y

        if x_diff == 0:
            return np.pi / 2

        return -np.arctan(y_diff / x_diff)

    def __initialize_points(self, number_of_points):
        x_values = np.linspace(self.start_point.x, self.end_point.x, number_of_points)
        y_values = np.linspace(self.start_point.y, self.end_point.y, number_of_points)

        return [Point(x, y, self.beta) for (x, y) in zip(x_values, y_values)]
