import numpy as np
import pytest

from src.Calculator import Calculator
from src.Line import Line
from src.Point import Point

tolerance = 0.00001


def test_get_crossing_point():
    line1 = Line(Point(0, 0), Point(1, 0))
    line2 = Line(Point(0, -1), Point(1, 1))

    cross_point = Calculator.get_crossing_point(line1, line2)

    assert cross_point == Point(0.5, 0)


def test_get_crossing_point_case2():
    line1 = Line(Point(0, 0), Point(1, 0))
    line2 = Line(Point(0, 1), Point(1, 1))

    with pytest.raises(Exception):
        Calculator.get_crossing_point(line1, line2)


def test_get_integral():
    x_values = [0, 1]
    y_values = [1, 1]

    assert Calculator.get_integral(x_values, y_values) == 1


def test_rotate_around_by():
    origin = Point(0, 0)
    point = Point(1, 0)

    c = Calculator.rotate_around_by(origin, point, np.pi / 2)
    expected = Point(0, 1)

    assert np.abs(c.x - expected.x) < tolerance
    assert np.abs(c.y - expected.y) < tolerance


def test_rotate_around_by2():
    origin = Point(0, 0)
    point = Point(-1, 0)

    c = Calculator.rotate_around_by(origin, point, np.pi / 2)
    expected = Point(0, -1)

    assert np.abs(c.x - expected.x) < tolerance
    assert np.abs(c.y - expected.y) < tolerance


def test_rotated_point_has_equal_distance():
    origin = Point(4, 2)
    point = Point(1, 2)

    c = Calculator.rotate_around_by(origin, point, np.pi / 3)
    distance_before = (point.x - origin.x)**2 + (point.y - origin.y)**2
    distance_after = (point.x - c.x)**2 + (point.y - c.y)**2

    assert np.abs(distance_before == distance_after) < tolerance

