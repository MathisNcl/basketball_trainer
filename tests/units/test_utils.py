from typing import List

import cv2
import numpy as np
import pytest

from bball_trainer.utils import (
    end_layout,
    getArea,
    incrustration,
    points_distance_is_enough,
)


def test_foreground_incrustration() -> None:
    foreground: np.ndarray = cv2.resize(cv2.imread("assets/left_hand.png", cv2.IMREAD_UNCHANGED), (100, 100))
    background: np.ndarray = np.ones((100, 100, 3)) * 255
    begin_corner: List[int] = [0, 0]
    img, _ = incrustration(foreground, background, begin_corner)
    assert np.all(img == np.load("assets/tests/test_incrustration.npy"))


def test_incrustration() -> None:
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


def test_incrustration_wrong_input() -> None:
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
def test_getArea(box: List[int], points: bool, expected: float) -> None:
    assert getArea(box, points) == expected


def test_getArea_type_error() -> None:
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
def test_points_distance_is_enough(x1: int, y1: int, x2: int, y2: int, minimal_distance: int, expected: bool) -> None:
    assert points_distance_is_enough(x1, y1, x2, y2, minimal_distance) == expected


def test_end_layout() -> None:
    img = np.zeros((720, 1280, 3), dtype=np.uint8)
    score = 100  # set score to 100
    result = end_layout(img, score)
    assert result.shape == (720, 1280, 3)  # check the shape of the returned image
    assert np.array_equal(result[400, 400], (255, 0, 255))  # check if the text "Game Over" is drawn
    assert np.array_equal(result[460, 500], (255, 0, 255))  # check if the score is displayed
    assert np.array_equal(result[460, 575], (255, 0, 255))  # check if the instruction to restart is displayed
