import pytest
import numpy as np
from utils import get_transform_result_api


def test_random_line():
    N = 30
    angle_degrees = [-45, 45, 0]
    shifts = [np.cos(np.radians(45)) * N, 0, np.cos(np.radians(0)) * N / 2]

    found_lines = get_transform_result_api(angle_degrees, shifts, (N, N))
    for idx, (res_tg, res_shift) in enumerate(found_lines):
        res_angle = np.degrees(np.arctan(res_tg))

        assert shifts[idx] - 2 < res_shift < shifts[idx] + 2
        assert angle_degrees[idx] - 5 < res_angle < angle_degrees[idx] + 5
