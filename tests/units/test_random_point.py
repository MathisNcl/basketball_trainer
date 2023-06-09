from bball_trainer.random_point import RandomPoint
import pytest
import numpy as np

config_point = {
    "xfrom1": 50,
    "xto1": 200,
    "xfrom2": 300,
    "xto2": 450,
    "yfrom": 50,
    "yto": 450,
}
HAND: dict = {
    "lmList": [
        [139, 460, 0],
        [226, 437, -27],
        [304, 362, -29],
        [350, 290, -30],
        [368, 226, -31],
        [286, 269, -6],
        [336, 199, -25],
        [364, 158, -43],
        [386, 121, -56],
        [233, 245, -7],
        [274, 166, -19],
        [301, 118, -35],
        [326, 81, -48],
        [174, 236, -13],
        [210, 156, -28],
        [240, 112, -39],
        [271, 80, -48],
        [110, 240, -22],
        [133, 167, -39],
        [161, 128, -44],
        [195, 102, -47],
    ],
    "bbox": (110, 80, 276, 380),
    "center": (248, 270),
    "type": "Right",
}


def test_instantiate():
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
def test_in_bbox(mocked_point, expected) -> None:
    # kind of a mock
    point = RandomPoint(**config_point)
    point.cx = mocked_point[0]
    point.cy = mocked_point[1]

    assert point.in_bbox(HAND) == expected


def test_draw_circle() -> None:
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
