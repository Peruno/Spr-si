import numpy as np

from Calculator import get_integral
from Line import Line
from Nozzle import Nozzle
from Point import Point


def test_get_profile_returns_correct_total_amount():
    nozzle_position = Point(0, 0)
    nozzle = Nozzle("nozzle1", nozzle_position)

    x_values = np.linspace(-10, 10, 10000)

    spray_distance = 20
    height_adjusted_profile = nozzle.get_profile(x_values, spray_distance)
    height_adjusted_integral = get_integral(x_values, height_adjusted_profile)

    tolerance = 0.1
    assert np.abs(nozzle.get_integral() - height_adjusted_integral) < tolerance


def test_get_profile_returns_correct_total_amount2():
    nozzle_position = Point(0, 0)

    nozzle = Nozzle("nozzle1", nozzle_position)

    x_values = np.linspace(-10, 10, 10000)

    spray_distance = 5
    height_adjusted_profile = nozzle.get_profile(x_values, spray_distance)
    height_adjusted_integral = get_integral(x_values, height_adjusted_profile)

    tolerance = 0.1
    assert np.abs(nozzle.get_integral() - height_adjusted_integral) < tolerance


def test_get_basic_profile_height_does_not_crash():
    nozzle_position = Point(0, 0)

    nozzle = Nozzle("nozzle1", nozzle_position)

    x_values = [1, 2, 3]
    y_values = nozzle.get_basic_profile_height(x_values)

    print(y_values)


def test_get_profile_returns_0_if_outside_of_range():

    nozzle_position = Point(0, 0)

    nozzle = Nozzle("nozzle1", nozzle_position)
    measurement_height = nozzle.measurement_height

    assert 0 == nozzle.get_profile(-6, measurement_height)
    assert 0 == nozzle.get_profile(-18, 3 * measurement_height)


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

    h_expected = [nozzle.get_profile(point.x, point.y) for point in line.get_points()]
    h_received = nozzle.get_profile_for_line(line)

    assert h_expected == h_received


