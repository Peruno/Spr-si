import numpy as np

from main.Calculator import Calculator
from main.Line import Line
from main.Nozzle import Nozzle
from main.Point import Point


def test_get_spray_height_returns_correct_total_amount():
    nozzle_position = Point(0, 10)
    nozzle = Nozzle("nozzle1", nozzle_position)

    height = 5
    start = Point(-10, height)
    end = Point(10, height)
    line = Line(start, end)

    heights = nozzle.get_spray_height_for_line(line)
    integral = Calculator.get_integral(line.get_x_values(), heights)

    tolerance = 0.1
    assert np.abs(nozzle.get_integral() - integral) < tolerance


def test_get_spray_heights_returns_correct_total_amount2():
    nozzle_position = Point(0, 12)
    nozzle = Nozzle("nozzle1", nozzle_position)

    height = 5
    start = Point(-10, height)
    end = Point(10, height)
    line = Line(start, end)

    spray_heights = nozzle.get_spray_height_for_line(line)
    integral = Calculator.get_integral(line.get_x_values(), spray_heights)

    tolerance = 0.1
    assert np.abs(nozzle.get_integral() - integral) < tolerance


def test_get_basic_spray_height_does_not_crash():
    nozzle_position = Point(0, 0)

    nozzle = Nozzle("nozzle1", nozzle_position)

    x_values = [1, 2, 3]
    y_values = nozzle.get_basic_spray_height(x_values)

    print(y_values)


def test_get_spray_height_returns_0_if_outside_of_range():

    nozzle_position = Point(0, 10)
    nozzle = Nozzle("nozzle1", nozzle_position)

    assert 0 == nozzle.get_spray_height(Point(-6, 0))


def test_get_zero_crossings():
    nozzle_position = Point(0, 20)
    nozzle = Nozzle("nozzle1", nozzle_position)

    x_1, x_2 = nozzle.get_zero_crossings()
    assert -5.5 < x_1 < -5
    assert 5 < x_2 < 5.5


def test_get_spray_height_for_line():
    nozzle_position = Point(0, 20)
    nozzle = Nozzle("nozzle1", nozzle_position)
    start_point = Point(0, 0)
    end_point = Point(10, 0)
    line = Line(start_point, end_point)

    h_expected = [nozzle.get_spray_height(point) for point in line.get_points()]
    h_received = nozzle.get_spray_height_for_line(line)

    assert h_expected == h_received


def test_radius_covered_by_big_line():
    line = Line(Point(-1000, 0), Point(1, 1000))
    nozzle = Nozzle("nozzle1", Point(10, 0))

    assert nozzle.is_radius_covered_by(line)


def test_radius_covered_by_small_line():
    line = Line(Point(-1, 0), Point(1, 1))
    nozzle = Nozzle("nozzle1", Point(10, 0))

    assert not nozzle.is_radius_covered_by(line)
