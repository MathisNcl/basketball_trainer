from typing import List
import pytest

import cv2
import numpy as np

from basketball_trainer.src.utils import getArea, incrustration, random_number


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


@pytest.mark.parametrize([([10, 10, 110, 110], True, 10000)])
def test_get_area(bbox, points, expected):
    assert getArea(bbox, points) == expected
