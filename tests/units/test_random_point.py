import numpy as np
import pytest

from bball_trainer.random_point import RandomPoint


def test_instantiate(config_point) -> None:
    point = RandomPoint(**config_point)
    assert point.cx <= 200 and point.cx >= 50 or point.cx <= 450 and point.cx >= 300
    assert point.cy <= 450 and point.cy >= 50


@pytest.mark.parametrize(
    "mocked_point, expected",
    [
        ((120, 90), True),
        ((15, 100), False),
    ],
)
def test_in_bbox(config_point, hand, mocked_point, expected) -> None:
    # kind of a mock
    point = RandomPoint(**config_point)
    point.cx = mocked_point[0]
    point.cy = mocked_point[1]

    assert point.in_bbox(hand) == expected


def test_draw_circle(config_point) -> None:
    img = np.zeros((500, 500, 3), dtype=np.uint8)
    # force a point in (250, 250)
    point = RandomPoint(**config_point)
    blue = (255, 0, 0)
    point.draw_circle(img, blue)
    white = (255, 255, 255)
    dark = (50, 50, 50)
    assert img.shape == (500, 500, 3)
    assert np.array_equal(img[point.cy, point.cx], white)
    assert np.array_equal(img[point.cy, point.cx + 15], blue)
    assert np.array_equal(img[point.cy, point.cx + 20], white)
    assert np.array_equal(img[point.cy, point.cx + 25], blue)
    assert np.array_equal(img[point.cy, point.cx + 30], dark)
    assert np.array_equal(img[point.cy, point.cx - 15], blue)
    assert np.array_equal(img[point.cy, point.cx - 20], white)
    assert np.array_equal(img[point.cy, point.cx - 25], blue)
    assert np.array_equal(img[point.cy, point.cx - 30], dark)
