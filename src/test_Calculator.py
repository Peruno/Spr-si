import pytest

from Calculator import Calculator
from Line import Line
from Point import Point


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
