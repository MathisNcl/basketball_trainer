from bball_trainer.hand_game import HandsDetectorBasketball
import numpy as np


def test_instanciation() -> None:
    detector: HandsDetectorBasketball = HandsDetectorBasketball()
    assert isinstance(detector, HandsDetectorBasketball)


def test_compute_distance(hand) -> None:
    detector: HandsDetectorBasketball = HandsDetectorBasketball()
    distanceCM = detector.compute_distance(hand)
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
