import numpy as np

from Calculator import Calculator
from Line import Line
from Nozzle import Nozzle
from Point import Point


def test_get_profile_returns_correct_total_amount():
    nozzle_position = Point(0, 10)
    nozzle = Nozzle("nozzle1", nozzle_position)

    height = 5
    start = Point(-10, height)
    end = Point(10, height)
    line = Line(start, end)

    height_adjusted_profile = nozzle.get_spray_height_for_line(line)
    height_adjusted_integral = Calculator.get_integral(line.get_x_values(), height_adjusted_profile)

    tolerance = 0.1
    assert np.abs(nozzle.get_integral() - height_adjusted_integral) < tolerance


def test_get_profile_returns_correct_total_amount2():
    nozzle_position = Point(0, 12)
    nozzle = Nozzle("nozzle1", nozzle_position)

    height = 5
    start = Point(-10, height)
    end = Point(10, height)
    line = Line(start, end)

    height_adjusted_profile = nozzle.get_spray_height_for_line(line)
    height_adjusted_integral = Calculator.get_integral(line.get_x_values(), height_adjusted_profile)

    tolerance = 0.1
    assert np.abs(nozzle.get_integral() - height_adjusted_integral) < tolerance


def test_get_basic_profile_height_does_not_crash():
    nozzle_position = Point(0, 0)

    nozzle = Nozzle("nozzle1", nozzle_position)

    x_values = [1, 2, 3]
    y_values = nozzle.get_basic_spray_height(x_values)

    print(y_values)


def test_get_profile_returns_0_if_outside_of_range():

    nozzle_position = Point(0, 10)
    nozzle = Nozzle("nozzle1", nozzle_position)

    assert 0 == nozzle.get_spray_height(Point(-6, 0))


def test_get_zero_crossings():
    nozzle_position = Point(0, 20)
    nozzle = Nozzle("nozzle1", nozzle_position)

    x_1, x_2 = nozzle.get_zero_crossings()
    assert -5.5 < x_1 < -5
    assert 5 < x_2 < 5.5


def test_get_profile_for_line():
    nozzle_position = Point(0, 20)
    nozzle = Nozzle("nozzle1", nozzle_position)
    start_point = Point(0, 0)
    end_point = Point(10, 0)
    line = Line(start_point, end_point)

    h_expected = [nozzle.get_spray_height(point) for point in line.get_points()]
    h_received = nozzle.get_spray_height_for_line(line)

    assert h_expected == h_received


def test_line_with_angle_has_correct_integral():
    nozzle_position = Point(0, 10)
    nozzle = Nozzle("nozzle1", nozzle_position)

    start = Point(-100, -5)
    end = Point(100, 2)
    line_with_angle = Line(start, end)
    profile_with_angle = nozzle.get_spray_height_for_line(line_with_angle)
    integral_with_angle = Calculator.get_integral(line_with_angle.get_x_values(), profile_with_angle)

    tolerance = 0.1
    assert np.abs(nozzle.get_integral() - integral_with_angle) < tolerance
