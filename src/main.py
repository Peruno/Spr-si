import matplotlib.pyplot as plt
import numpy as np


from Line import Line
from Nozzle import Nozzle
from Point import Point
from src.Profile import Profile

if __name__ == "__main__":
    # nozzle_position = Point(5, 20)
    # nozzle = Nozzle("nozzle1", nozzle_position)
    #
    # start_point = Point(0, 0)
    # end_point = Point(10, 0)
    # big_line = Line(start_point, end_point)
    #
    # h_values = nozzle.get_spray_height_for_line(big_line)
    #
    # left_outer_line = nozzle.get_left_outer_line(big_line)
    # right_outer_line = nozzle.get_right_outer_line(big_line)
    #
    # plt.plot(left_outer_line.get_x_values(), left_outer_line.get_y_values(), "--k")
    # plt.plot(right_outer_line.get_x_values(), right_outer_line.get_y_values(), "--k")
    #
    # x_values = big_line.get_x_values()
    # plt.plot(x_values, h_values)
    # plt.show()


    nozzle = Nozzle("nozzle1", nozzle_position=Point(0, 10))
    line = Line(Point(-20, -1), Point(20, 1), number_of_points=100)
    spray_heights = nozzle.get_spray_height_for_line(line)
    profile = Profile(line, spray_heights)

    print(profile.get_integral())
    print(nozzle.get_integral())

    assert np.abs(profile.get_integral() - nozzle.get_integral()) < 0.00001
