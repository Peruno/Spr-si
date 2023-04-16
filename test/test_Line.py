import pytest

from main.Line import Line
from main.Point import Point
from numpy import pi


def test_line_throws_if_start_and_end_are_equal():
    start_point = Point(0, 0)
    end_point = Point(0, 0)
    with pytest.raises(Exception):
        Line(start_point, end_point)


def test_line_throws_if_end_left_of_start():
    start_point = Point(0, 0)
    end_point = Point(-1, 0)

    with pytest.raises(Exception):
        Line(start_point, end_point)


def test_line_throws_if_only_one_point_is_given():
    start_point = Point(0, 0)
    end_point = Point(-1, 0)

    with pytest.raises(Exception):
        Line(start_point, end_point, 1)


def test_get_angle_case1():
    start_point = Point(0, 0)
    end_point = Point(2, 0)

    line = Line(start_point, end_point)
    angle = line.get_angle()

    assert angle == 0


def test_get_angle_case2():
    start_point = Point(0, 0)
    end_point = Point(1, 1)

    line = Line(start_point, end_point)
    angle = line.get_angle()

    assert angle == -pi / 4


def test_get_angle_case3():
    start_point = Point(0, 0)
    end_point = Point(1, -1)
    line = Line(start_point, end_point)

    angle = line.get_angle()

    assert angle == pi / 4


def test_get_angle_case4():
    start_point = Point(0, 0)
    end_point = Point(0, 1)
    line = Line(start_point, end_point)

    angle = line.get_angle()

    assert angle == pi / 2


def test_get_points_returns_correct_number_of_points():
    start_point = Point(0, 0)
    end_point = Point(0, 1)
    number_of_points = 99
    line = Line(start_point, end_point, number_of_points)

    points = line.get_points()

    assert len(points) == 99
