import numpy as np

from src.Calculator import Calculator
from src.Catalogue import Catalogue
from src.Line import Line
from src.Point import Point


class Nozzle:
    def __init__(self, name, nozzle_position=Point(0, 0)):
        catalogue = Catalogue(name)
        self.measurement_height = catalogue.get_height()
        self.x_measurement = catalogue.get_x_measurement()
        self.h_measurement = catalogue.get_h_measurement()
        self.polynomial_fit_coefficients = np.polyfit(self.x_measurement, self.h_measurement, deg=5)

        self.position = nozzle_position
        self.alpha = 0
        self.measurement_crossing_left, self.measurement_crossing_right = self._get_zero_crossings()

    def get_spray_height_for_line(self, line):
        if self.alpha != 0:
            transformed_line = self._transform_line_into_rotated_system(line)
        else:
            transformed_line = line

        return [self._get_spray_height_for_point(point) for point in transformed_line.get_points()]

    def _get_spray_height_for_point(self, point):
        h_0 = self.get_spray_height_at_intersection_with_measurement_line(point)
        h_distance_adjusted = self.adjust_for_distance(h_0, point.y)
        h_distance_and_angle_adjusted = self.adjust_for_angle(h_distance_adjusted, point)
        return h_distance_and_angle_adjusted

    def get_spray_height_at_intersection_with_measurement_line(self, point):
        if x_0 := self.get_x_projected_to_measurement_line(point):
            return self._get_basic_spray_height(x_0)
        return 0

    def adjust_for_distance(self, h_0, y):
        try:
            relative_y = self.get_relative_y(y)
        except:
            return h_0

        return h_0 / relative_y

    def get_x_projected_to_measurement_line(self, point):
        try:
            relative_y = self.get_relative_y(point.y)
        except:
            # If that is not possible, return value outside of range
            return None

        relative_x = point.x - self.position.x
        return relative_x / relative_y

    def get_relative_y(self, y):
        relative_y = (self.position.y - y) / self.measurement_height  # y/y_0

        if relative_y < 0:
            raise Exception("Line is above the nozzle.")
        elif relative_y == 0:
            raise Exception(f"The point can not be at same y-position as the nozzle ({y, self.position.y}).")

        return relative_y

    def adjust_for_angle(self, height, point):
        if not point.beta:
            return height

        x_distance = np.abs(point.x - self.position.x)
        y_distance = point.y - self.position.y

        if y_distance == 0:
            return 0

        alpha = np.arctan(x_distance / y_distance)

        adjustment_factor = np.cos(alpha + point.beta) / np.cos(alpha)

        return height * adjustment_factor

    def _transform_line_into_rotated_system(self, line):
        start_point = line.get_start_point()
        end_point = line.get_end_point()

        rotated_start_point = Calculator.rotate_around_by(origin=self.position, point=start_point, angle=-self.alpha)
        rotated_end_point = Calculator.rotate_around_by(origin=self.position, point=end_point, angle=-self.alpha)

        if rotated_start_point.x < rotated_end_point.x:
            return Line(rotated_start_point, rotated_end_point, number_of_points=line.get_number_of_points())
        else:
            return Line(rotated_end_point, rotated_start_point, number_of_points=line.get_number_of_points())

    def _get_basic_spray_height(self, x):
        if self.measurement_crossing_left <= x <= self.measurement_crossing_right:
            return np.polyval(self.polynomial_fit_coefficients, x)
        else:
            return 0

    def get_integral(self, baskets=1000):
        x_values = np.linspace(self.measurement_crossing_left - 1, self.measurement_crossing_right + 1, baskets)
        y_values = [self._get_basic_spray_height(x) for x in x_values]
        return Calculator.get_integral(x_values, y_values)

    def _get_zero_crossings(self):
        x_values = np.linspace(min(self.x_measurement) - 1, max(self.x_measurement) + 1, 1000)
        y_values = np.polyval(self.polynomial_fit_coefficients, x_values)

        crossing_x_values = []
        for i in range(len(y_values) - 1):
            if (y_values[i] < 0 < y_values[i + 1]) or (y_values[i] > 0 > y_values[i + 1]):
                crossing_x_values.append((x_values[i] + x_values[i + 1]) / 2)

        if len(crossing_x_values) != 2:
            raise Exception("Not exactly 2 intersections with x-Axis!")

        return crossing_x_values[0], crossing_x_values[1]

    def get_outer_line(self, left_or_right):
        if left_or_right == "left":
            measurement_boundary = Point(self.measurement_crossing_left + self.position.x,
                                         self.position.y - self.measurement_height)
        elif left_or_right == "right":
            measurement_boundary = Point(self.measurement_crossing_right + self.position.x,
                                         self.position.y - self.measurement_height)
        else:
            raise Exception("Only 'left' or 'right' allowed.")

        rotated_end_of_line = Calculator.rotate_around_by(self.position, measurement_boundary, self.alpha)

        if rotated_end_of_line.x < self.position.x:
            return Line(rotated_end_of_line, self.position)
        else:
            return Line(self.position, rotated_end_of_line)

    def is_radius_covered_by(self, line):
        leftmost_point, *others, rightmost_point = line.get_points()
        left_projected = self.get_x_projected_to_measurement_line(leftmost_point)
        right_projected = self.get_x_projected_to_measurement_line(rightmost_point)

        return left_projected < self.measurement_crossing_left and right_projected > self.measurement_crossing_right

    def set_angle_in_degrees(self, alpha):
        if not -90 <= alpha <= 90:
            raise Exception("Only angles between -90 and +90 degrees are allowed.")

        angle_in_radiant = alpha / 180 * np.pi

        self.alpha = angle_in_radiant
