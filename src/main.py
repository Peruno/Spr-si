import matplotlib.pyplot as plt

from Line import Line
from Nozzle import Nozzle
from Point import Point

if __name__ == "__main__":
    nozzle_position = Point(5, 20)
    nozzle = Nozzle("nozzle1", nozzle_position)

    start_point = Point(0, 0)
    end_point = Point(10, 0)
    line = Line(start_point, end_point)

    x_values = line.get_x_values()
    h_values = nozzle.get_profile_for_line(line)

    left_outer_line = nozzle.get_left_outer_line(line)
    right_outer_line = nozzle.get_right_outer_line()

    plt.plot(left_outer_line.get_x_values(), left_outer_line.get_y_values(), "--k")
    plt.plot(right_outer_line.get_x_values(), right_outer_line.get_y_values(), "--k")

    plt.plot(x_values, h_values)
    plt.show()
