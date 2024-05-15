import pytest
import numpy as np
from utils import get_transform_result


def simple_lines_test_generator(angle_degree, shift):
    def test_simple_line():
        N = 10
        res_tg, res_shift = get_transform_result(angle_degree, shift, (N, N))
        res_angle = np.degrees(np.arctan(res_tg))

        beta = shift / np.cos(np.radians(angle_degree))

        dx = 2 / (N - 1)
        dy = dx

        res_beta = (res_tg * (-1) + res_shift - (-1)) / dy

        assert beta - 2 < res_beta
        assert res_beta < beta + 2
        assert angle_degree - 5 < res_angle < angle_degree + 5

    return test_simple_line


for angle in range(85, 4, -5):
    test_name = f"test_angle_{angle}_shift_0"
    test_func = simple_lines_test_generator(angle, 0)
    globals()[test_name] = test_func


if __name__ == "__main__":
    pytest.main()
