from typing import List
import pytest

import cv2
import numpy as np

from basketball_trainer_src.utils import getArea, incrustration, points_distance_is_enough, random_number


def test_get_random() -> None:
    assert random_number(1, 2, 4, 5) != 3
    rand: int = random_number(1, 5, 10, 20)
    assert rand <= 5 or rand >= 10


def test_foreground_incrustration() -> None:
    foreground: np.ndarray = cv2.resize(cv2.imread("assets/left_hand.png", cv2.IMREAD_UNCHANGED), (100, 100))
    background: np.ndarray = np.ones((100, 100, 3)) * 255
    begin_corner: List[int] = [0, 0]
    img, _ = incrustration(foreground, background, begin_corner)
    assert np.all(img == np.load("assets/tests/test_incrustration.npy"))


def test_incrustration():
    foreground = np.zeros((50, 50, 4), dtype=np.uint8)
    foreground[:, :, 0] = 255
    foreground[:, :, 3] = 255

    background = np.zeros((100, 100, 3), dtype=np.uint8)
    background[:, :] = (255, 255, 255)

    begin_corner = [25, 25]

    expected_result = background.copy()
    expected_result[begin_corner[1] : begin_corner[1] + 50, begin_corner[0] : begin_corner[0] + 50] = foreground[
        :, :, 0:3
    ]
    cv2.rectangle(expected_result, (25, 25), (75, 75), (255, 0, 255), 3)

    result, (x, y, w, h) = incrustration(foreground, background, begin_corner)

    assert np.all(result == expected_result)
    assert (x, y, w, h) == (25, 25, 50, 50)


def test_incrustration_wrong_input():
    with pytest.raises(IndexError):
        incrustration(np.zeros((50, 50, 3), dtype=np.uint8), np.zeros((100, 100, 3), dtype=np.uint8), [101, 101])


@pytest.mark.parametrize(
    "box, points, expected",
    [
        ([0, 0, 2, 2], True, 4.0),
        ([0, 0, 1, 1], True, 1.0),
        ([0, 0, 0, 0], True, 0.0),
        ([2, 2, 4, 4], False, 16.0),
        ([1, 1, 2, 2], False, 4.0),
        ([0, 0, 0, 0], False, 0.0),
    ],
)
def test_getArea(box, points, expected):
    assert getArea(box, points) == expected


def test_getArea_type_error():
    with pytest.raises(TypeError):
        getArea("box", True)


@pytest.mark.parametrize(
    "x1, y1, x2, y2, minimal_distance, expected",
    [
        (0, 0, 0, 0, 0, True),  # same point, distance=0
        (0, 0, 3, 4, 5, True),  # distance=5 < minimal_distance=5
        (0, 0, 3, 4, 4, False),  # distance=5 > minimal_distance=4
        (1, 2, 3, 4, 2, False),  # distance=sqrt(8) > minimal_distance=2
    ],
)
def test_points_distance_is_enough(x1, y1, x2, y2, minimal_distance, expected):
    assert points_distance_is_enough(x1, y1, x2, y2, minimal_distance) == expected
