import numpy as np

import Calculator
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

    def get_profile(self, x, y):
        relative_y = np.abs(y - self.nozzle_y) / self.measurement_height  # y/y_0
        if relative_y == 0:
            raise Exception(f"The point can not be at same y-position as the nozzle ({y, self.nozzle_y})")

        relative_x = x - self.nozzle_x

        x_0 = relative_x / relative_y
        h_0 = self.get_basic_profile_height(x_0)

        distance_adjusted_h = h_0 / relative_y
        return distance_adjusted_h

    def get_profile_for_line(self, line):
        h_values = [self.get_profile(point.x, point.y) for point in line.get_points()]

        return h_values

    def get_basic_profile_height(self, x):
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
        x_values = np.linspace(self.measurement_crossing_left, self.measurement_crossing_right, baskets)
        y_values = self.get_basic_profile_height(x_values)
        return Calculator.get_integral(x_values, y_values)

    def get_zero_crossings(self):
        x_values = np.linspace(min(self.x_measurement) - 1, max(self.x_measurement) + 1, 1000)
        y_values = np.polyval(self.polynomial_fit_coefficients, x_values)

        crossing_points = []
        for i in range(len(y_values) - 1):
            if (y_values[i] < 0 < y_values[i + 1]) or (y_values[i] > 0 > y_values[i + 1]):
                crossing_points.append((x_values[i] + x_values[i + 1]) / 2)

        if len(crossing_points) != 2:
            raise Exception("Not exactly 2 intersections with x-Axis!")

        return crossing_points[0], crossing_points[1]

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
