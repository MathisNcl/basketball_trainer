from bball_trainer.hand_game import HandsDetectorBasketball
import pytest
import numpy as np

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


def test_instanciation() -> None:
    detector: HandsDetectorBasketball = HandsDetectorBasketball()
    assert isinstance(detector, HandsDetectorBasketball)


def test_compute_distance() -> None:
    detector: HandsDetectorBasketball = HandsDetectorBasketball()
    distanceCM = detector.compute_distance(HAND)
    assert round(distanceCM, 2) == 28.52


def test_print_hand() -> None:
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    hand = {"bbox": (100, 100, 200, 200)}
    distanceCM = 50.5
    color = (255, 0, 255)
    HandsDetectorBasketball.print_hand(img, hand, distanceCM, color)

    assert isinstance(img, np.ndarray)
    assert img.shape == (480, 640, 3)

    # looking for color corner
    assert np.array_equal(img[100, 100], np.array(color, dtype=np.uint8))
    assert np.array_equal(img[100, 200], np.array(color, dtype=np.uint8))
    assert np.array_equal(img[200, 100], np.array(color, dtype=np.uint8))

    # looking for a white pixel from the text
    assert np.array_equal(img[80, 130], np.array((255, 255, 255), dtype=np.uint8))
