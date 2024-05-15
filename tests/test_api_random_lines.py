import pytest
import numpy as np
from utils import get_transform_result_api


def simple_lines_test_generator(angle_degree, shift, thickness):
    def test_random_line():
        N = 10
        found_lines = get_transform_result_api(
            [angle_degree], [shift], (N, N), thickness
        )
        for res_tg, res_shift in found_lines:
            res_angle = np.degrees(np.arctan(res_tg))

            assert shift - 2 < res_shift < shift + 2
            assert angle_degree - 5 < res_angle < angle_degree + 5

    return test_random_line


for i in range(10):
    test_name = f"test_random_line_{i}"
    angle = np.random.randint(low=0, high=89)
    shift = np.random.randint(low=-5, high=5)
    thickness = np.random.randint(low=1, high=3)
    test_func = simple_lines_test_generator(angle, shift, thickness)
    globals()[test_name] = test_func

if __name__ == "__main__":
    np.random.seed(42)
    pytest.main()
