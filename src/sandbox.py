#!/usr/bin/env python3

from Point import Point
from src.Calculator import Calculator
import numpy as np


if __name__ == "__main__":
    # tolerance = 0.0001
    #
    # a = Point(-1, 0.001)
    # b = Point(0, 0)
    #
    # c = Calculator.rotate_around_by(a, b, np.pi / 2)
    # expected = Point(0, -1)
    #
    # assert np.abs(c.x - expected.x) < tolerance
    # assert np.abs(c.y - expected.y) < tolerance
    a = Point(0, 0)
    b = Point(1, 1)

    assert Calculator.get_angle_between(a, b) == np.pi / 4
