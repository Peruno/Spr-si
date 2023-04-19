import numpy as np
import pytest

from src.Line import Line
from src.Nozzle import Nozzle
from src.Point import Point
from src.Profile import Profile
from pytest import approx


def test_profile_raises_if_line_and_spray_heights_do_not_fit():
    line = Line(Point(0, 0), Point(1, 0), number_of_points=2)
    spray_heights = [1, 2, 3]

    with pytest.raises(Exception):
        Profile(line, spray_heights)


def test_profile_invariant_for_horizontal_and_covered_line():
    line = Line(Point(0, 0), Point(1, 0), number_of_points=2)
    spray_heights = [1, 1]
    profile = Profile(line, spray_heights)

    assert profile.get_x_values() == line.get_x_values()
    assert profile.get_y_values() == spray_heights


def test_profile_only_keeps_non_zero_values():
    horizontal_line = Line(Point(0, 0), Point(10, 0), 10)
    nozzle = Nozzle("nozzle1", Point(5, 5))
    spray_heights = nozzle.get_spray_height_for_line(horizontal_line)
    profile = Profile(horizontal_line, spray_heights)

    x_values = profile.get_x_values()
    y_values = profile.get_y_values()

    assert x_values == [x for (x, y) in zip(horizontal_line.get_x_values(), spray_heights) if y > 0]
    assert y_values == [h for h in spray_heights if h > 0]


def test_profile_works_for_right_tilted_line():
    horizontal_line = Line(Point(0, 0), Point(1, -1), number_of_points=2)
    spray_heights = [1, 1]
    profile = Profile(horizontal_line, spray_heights)

    x_expected = [np.sin(np.pi / 4), np.sin(np.pi / 4) + 1]
    y_expected = [np.sin(np.pi / 4), np.sin(np.pi / 4) - 1]

    assert profile.get_x_values() == approx(x_expected, 0.000001)
    assert profile.get_y_values() == approx(y_expected, 0.000001)


def test_profile_works_for_left_tilted_line():
    horizontal_line = Line(Point(0, 0), Point(1, 1), number_of_points=2)
    spray_heights = [1, 1]
    profile = Profile(horizontal_line, spray_heights)

    x_expected = [-np.sin(np.pi / 4), -np.sin(np.pi / 4) + 1]
    y_expected = [np.sin(np.pi / 4), np.sin(np.pi / 4) + 1]

    angle = horizontal_line.get_angle()
    assert np.cos(angle) == np.cos(-angle)

    assert profile.get_x_values() == approx(x_expected, 0.000001)
    assert profile.get_y_values() == approx(y_expected, 0.000001)


def test_line_without_angle_has_correct_integral():
    line = Line(Point(0, 0), Point(1, 0), number_of_points=2)
    spray_heights = [1, 1]
    profile = Profile(line, spray_heights)

    assert profile.get_integral() == 1


def test_line_with_angle_has_correct_integral():
    line = Line(Point(0, 0), Point(1, 1), number_of_points=2)
    spray_heights = [1, 1]
    profile = Profile(line, spray_heights)

    assert profile.get_integral() == 1
