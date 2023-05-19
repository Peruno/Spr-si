#!/usr/bin/env python3

import matplotlib.pyplot as plt

from Line import Line
from Nozzle import Nozzle
from Point import Point
from src.Profile import Profile

if __name__ == "__main__":
    nozzle_x = 0
    nozzle_y = 10
    start_x = -10
    start_y = -5
    end_x = 0
    end_y = 0
    alpha = 66

    start_point = Point(start_x, start_y)
    end_point = Point(end_x, end_y)
    line = Line(start_point, end_point, number_of_points=200)
    x_values = line.get_x_values()
    y_values = line.get_y_values()

    nozzle_position = Point(nozzle_x, nozzle_y)
    nozzle = Nozzle("nozzle1", nozzle_position)
    nozzle.set_angle_in_degrees(alpha)
    h_values = nozzle.get_spray_height_for_line(line)

    print(len(line.get_points()))
    print(len(h_values))
    profile = Profile(line, h_values)
