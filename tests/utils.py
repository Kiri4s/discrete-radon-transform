import numpy as np
import cv2

import pathlib
from PIL import Image
import sys

sys.path.append("../discrete_radon_transform")
sys.path.append("./discrete_radon_transform")
from Discrete_Radon_Transform import Discrete_Radon_Transform


def rotation_matrix(theta):
    return np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])


def make_line(angle_degrees, shift, thikness, image, to_show=False):
    """
    Функция принимает изображение и рисует на нем прямую с углом angle_degrees,
    заданным в градусах, относительно оси oX, расстоянием shift от начала
    координат. Толщина прямой задается целым числом параметром thikness.
    Отображает полученное изображение, если параметр to_show=True.
    Функция возвращает исходное изображение с нарисованной прямой.
    """
    # Set constants
    oX = np.array([1, 0])
    scale_factor = 10 * max(image.shape)

    # Convert angle to radians
    angle_radians = np.radians(angle_degrees)

    # Calculate normal and directional vectors
    normal_vector_angle = angle_radians + np.pi / 2
    normal_vector = rotation_matrix(normal_vector_angle) @ oX
    direction_vector = rotation_matrix(angle_radians) @ oX
    center = normal_vector * shift

    # Calculate start and end points of line
    start_point = center + direction_vector * -scale_factor
    end_point = center + direction_vector * scale_factor

    # Draw line
    start_point = start_point.astype(int)
    end_point = end_point.astype(int)

    cv2.line(image, start_point, end_point, (255, 255, 255), thikness)

    # Show image
    if to_show:
        cv2.imshow("Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return 255 - image


def get_transform_result(angle_degree, shift, image_shape, thickness=1):
    angle_tangent_acc = 500
    shift_acc = 50
    tg = np.tan(np.pi * 89 / 180)
    p = np.linspace(-tg, tg, angle_tangent_acc)
    t = np.linspace(-5, 5, shift_acc)

    img_h = image_shape[0]
    img_w = image_shape[1]
    image = np.zeros((img_h, img_w, 3), dtype=np.uint8)
    image = make_line(angle_degree, shift, thickness, image)
    im = Image.fromarray(image)
    im.save("tests/test_img.jpeg")

    tf = Discrete_Radon_Transform("tests/test_img.jpeg", angle_tangent_acc, shift_acc)
    tf.display_result()
    pathlib.Path.unlink("tests/test_img.jpeg")

    offset_idx, slope_idx = np.unravel_index(
        tf.get_transform().argmax(), tf.get_transform().shape
    )
    res_tg = p[slope_idx]
    res_shift = t[offset_idx]

    return res_tg, res_shift


def get_transform_result_api(angle_degrees, shifts, image_shape, thickness=1):
    angle_tangent_acc = 500
    shift_acc = 50
    tg = np.tan(np.pi * 89 / 180)
    p = np.linspace(-tg, tg, angle_tangent_acc)
    t = np.linspace(-5, 5, shift_acc)

    img_h = image_shape[0]
    img_w = image_shape[1]
    image = np.zeros((img_h, img_w, 3), dtype=np.uint8)
    for angle_degree, shift in zip(angle_degrees, shifts):
        image = make_line(angle_degree, shift, thickness, image)
    im = Image.fromarray(image)
    im.save("tests/test_img.jpeg")

    tf = Discrete_Radon_Transform("tests/test_img.jpeg", angle_tangent_acc, shift_acc)
    tf.display_result()
    pathlib.Path.unlink("tests/test_img.jpeg")

    found_lines = tf.get_params()
    return found_lines
