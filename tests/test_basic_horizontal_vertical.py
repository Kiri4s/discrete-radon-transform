import pytest
import numpy as np
from utils import get_transform_result


def test_vertical_line():
    N = 30
    angle_degree = 89
    shift = 0
    res_tg, res_shift = get_transform_result(angle_degree, shift, (N, N))
    res_angle = np.degrees(np.arctan(res_tg))
    beta = shift / np.cos(np.radians(angle_degree))

    dx = 2 / (N - 1)
    dy = dx

    res_beta = (res_tg * (-1) + res_shift - (-1)) / dy

    assert beta - 2 < res_beta
    assert res_beta < beta + 2
    assert angle_degree - 5 < res_angle < angle_degree + 5


def test_horizontal_line():
    N = 30
    angle_degree = 0
    shift = 0
    res_tg, res_shift = get_transform_result(angle_degree, shift, (N, N))
    res_angle = np.degrees(np.arctan(res_tg))
    beta = shift / np.cos(np.radians(angle_degree))

    dx = 2 / (N - 1)
    dy = dx

    res_beta = (res_tg * (-1) + res_shift - (-1)) / dy

    assert beta - 2 < res_beta
    assert res_beta < beta + 2
    assert angle_degree - 5 < res_angle < angle_degree + 5
