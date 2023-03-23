from Point import Point


def get_integral(x_values, y_values):
    if len(x_values) != len(y_values):
        raise Exception("Length not equal!")

    integral = 0

    for i in range(len(x_values) - 1):
        y_average = (y_values[i] + y_values[i + 1]) / 2
        distance = x_values[i + 1] - x_values[i]
        integral += y_average * distance

    return integral


def get_parameters_of_line(start_point, end_point):
    """Returns a, b where y = a * x + b is the equation of the line that crosses
    start_point and end_point."""
    x_1, y_1 = start_point.x, start_point.y
    x_2, y_2 = end_point.x, end_point.y

    a = (y_2 - y_1) / (x_2 - x_1)
    b = y_1 - x_1 * a

    return a, b


def get_crossing_point(line1, line2):
    a_1, b_1 = get_parameters_of_line(line1.start_point, line1.end_point)
    a_2, b_2 = get_parameters_of_line(line2.start_point, line2.end_point)

    if a_1 == a_2 and b_1 != b_2:
        raise Exception("The lines never cross!")
    elif a_1 == a_2 and b_1 == b_2:
        raise Exception("The lines are equal")

    x_cross = (b_2 - b_1) / (a_1 - a_2)
    y_cross = (b_2 - b_1) / (a_1 - a_2) * a_1 + b_1

    return Point(x_cross, y_cross)
