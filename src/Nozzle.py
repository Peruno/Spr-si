import numpy as np

from Calculator import Calculator
from Catalogue import Catalogue
from Line import Line
from Point import Point


class Nozzle:

    def __init__(self, name, nozzle_position=Point(0, 0)):
        catalogue = Catalogue(name)
        self.measurement_height = catalogue.get_height()
        self.x_measurement = catalogue.get_x_measurement()
        self.h_measurement = catalogue.get_h_measurement()
        self.polynomial_fit_coefficients = np.polyfit(self.x_measurement, self.h_measurement, deg=5)

        self.nozzle_x = nozzle_position.x
        self.nozzle_y = nozzle_position.y
        self.measurement_crossing_left, self.measurement_crossing_right = self.get_zero_crossings()

    def get_spray_height(self, point):

        h_0 = self.get_spray_height_at_intersection_with_measurement_line(point)
        h_distance_adjusted = self.adjust_for_distance(h_0, point.y)
        h_distance_and_angle_adjusted = self.adjust_for_angle(h_distance_adjusted, point)
        return h_distance_and_angle_adjusted

    def adjust_for_distance(self, h_0, y):
        relative_y = self.get_relative_y(y)

        return h_0 / relative_y

    def get_spray_height_at_intersection_with_measurement_line(self, point):
        relative_y = self.get_relative_y(point.y)
        relative_x = point.x - self.nozzle_x

        x_0 = relative_x / relative_y

        return self.get_basic_spray_height(x_0)

    def get_relative_y(self, y):
        relative_y = (self.nozzle_y - y) / self.measurement_height  # y/y_0

        if relative_y < 0:
            raise Exception("Line is above the nozzle.")
        elif relative_y == 0:
            raise Exception(f"The point can not be at same y-position as the nozzle ({y, self.nozzle_y}).")

        return relative_y

    def adjust_for_angle(self, height, point):
        if point.beta is None:
            return height

        x_distance = np.abs(point.x - self.nozzle_x)
        y_distance = point.y - self.nozzle_y
        alpha = np.arctan(x_distance / y_distance)

        adjustment_factor = np.cos(alpha + point.beta) / np.cos(alpha)

        return height * adjustment_factor

    def get_spray_height_for_line(self, line):
        h_values = [self.get_spray_height(point) for point in line.get_points()]

        return h_values

    def get_basic_spray_height(self, x):
        if isinstance(x, int) or isinstance(x, float):
            if self.measurement_crossing_left <= x <= self.measurement_crossing_right:
                return np.polyval(self.polynomial_fit_coefficients, x)
            else:
                return 0

        result = []
        for x_value in x:
            if self.measurement_crossing_left <= x_value <= self.measurement_crossing_right:
                result.append(np.polyval(self.polynomial_fit_coefficients, x_value))
            else:
                result.append(0)
        return result

    def get_integral(self, baskets=1000):
        x_values = np.linspace(self.measurement_crossing_left - 1, self.measurement_crossing_right + 1, baskets)
        y_values = self.get_basic_spray_height(x_values)
        return Calculator.get_integral(x_values, y_values)

    def get_zero_crossings(self):
        x_values = np.linspace(min(self.x_measurement) - 1, max(self.x_measurement) + 1, 1000)
        y_values = np.polyval(self.polynomial_fit_coefficients, x_values)

        crossing_x_values = []
        for i in range(len(y_values) - 1):
            if (y_values[i] < 0 < y_values[i + 1]) or (y_values[i] > 0 > y_values[i + 1]):
                crossing_x_values.append((x_values[i] + x_values[i + 1]) / 2)

        if len(crossing_x_values) != 2:
            raise Exception("Not exactly 2 intersections with x-Axis!")

        return crossing_x_values[0], crossing_x_values[1]

    def get_left_outer_line(self, surface_line):
        start_point_measurement = Point(self.measurement_crossing_left, 0)
        end_point_measurement = Point(0, self.measurement_height)

        x_diff = self.nozzle_x
        y_diff = self.nozzle_y - self.measurement_height

        position_adjusted_end_point = Point(end_point_measurement.x + x_diff, end_point_measurement.y + y_diff)
        position_adjusted_start_point = Point(start_point_measurement.x + x_diff, start_point_measurement.y + y_diff)

        line_without_length_adjustment = Line(position_adjusted_start_point, position_adjusted_end_point)
        crossing_with_surface = Calculator.get_crossing_point(line_without_length_adjustment, surface_line)

        line_from_nozzle_to_surface = Line(crossing_with_surface, Point(self.nozzle_x, self.nozzle_y))
        return line_from_nozzle_to_surface

    def get_right_outer_line(self, surface_line):
        start_point_measurement = Point(0, self.measurement_height)
        end_point_measurement = Point(self.measurement_crossing_right, 0)

        x_diff = self.nozzle_x
        y_diff = self.nozzle_y - self.measurement_height

        position_adjusted_start_point = Point(start_point_measurement.x + x_diff, start_point_measurement.y + y_diff)
        position_adjusted_end_point = Point(end_point_measurement.x + x_diff, end_point_measurement.y + y_diff)

        line_without_length_adjustment = Line(position_adjusted_start_point, position_adjusted_end_point)
        crossing_with_surface = Calculator.get_crossing_point(line_without_length_adjustment, surface_line)

        line_from_nozzle_to_surface = Line(Point(self.nozzle_x, self.nozzle_y), crossing_with_surface)
        return line_from_nozzle_to_surface

    def is_radius_covered_by(self, line):
        left_within = self.measurement_crossing_left > line.get_x_values()[0]
        right_within = self.measurement_crossing_right > line.get_x_values()[-1]


        assert False # still false!!! Uses crossings with measurement line
        return left_within and right_within
