from bball_trainer.game import GamingClient
from bball_trainer.hand_game import HandsDetectorBasketball
from unittest.mock import patch, MagicMock
import cv2
import pytest
import numpy as np
import time


@pytest.mark.parametrize(
    "total_time, difficulty, hand_constraint, user_id",
    [
        (30, "Easy", False, 1),
        (60, "Medium", True, 2),
        (45, "Hard", True, 3),
    ],
)
def test_gaming_client_start(total_time, difficulty, hand_constraint, user_id):
    # Mocking camera
    img = np.zeros((720, 1280, 3), dtype=np.uint8)
    capture_mock = MagicMock()
    capture_mock.read.return_value = (True, img)
    with patch("cv2.VideoCapture", return_value=capture_mock):
        gc = GamingClient(
            total_time=total_time, difficulty=difficulty, hand_constraint=hand_constraint, user_id=user_id
        )
        gc.start(testing_nb=1)


def test_gaming_client_points(two_hands):
    # Mocking camera
    img = np.zeros((720, 1280, 3), dtype=np.uint8)
    capture_mock = MagicMock()
    capture_mock.read.return_value = (True, img)
    with patch("cv2.VideoCapture", return_value=capture_mock):
        gc = GamingClient(total_time=10, difficulty="Easy", hand_constraint=False, user_id=1)
        gc.starting_client.timeStart = time.time()
        gc.starting_client.waiting_for_start = False

        # FIXME: not pretty
        with patch.object(HandsDetectorBasketball, "findHands", return_value=two_hands):
            gc.point.cx = 140
            gc.point.cy = 300
            gc.start(testing_nb=10)
            assert gc.score == 1
