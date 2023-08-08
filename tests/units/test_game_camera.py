import logging
import time
from unittest.mock import MagicMock, patch

import numpy as np
import pytest
import requests_mock

from bball_trainer import settings
from bball_trainer.game import GamingClient
from bball_trainer.hand_game import HandsDetectorBasketball

pytestmark = pytest.mark.slow


@pytest.mark.parametrize(
    "total_time, difficulty, hand_constraint, user_id",
    [
        (30, "Easy", False, 1),
        (60, "Medium", True, 2),
        (45, "Hard", True, 3),
    ],
)
def test_gc_start(total_time, difficulty, hand_constraint, user_id, caplog):
    # Mocking camera
    img = np.zeros((720, 1280, 3), dtype=np.uint8)
    capture_mock = MagicMock()
    capture_mock.read.return_value = (True, img)

    with patch("cv2.VideoCapture", return_value=capture_mock):
        gc = GamingClient(
            total_time=total_time, difficulty=difficulty, hand_constraint=hand_constraint, user_id=user_id
        )
        with caplog.at_level(logging.DEBUG):
            gc.start_entire_game(testing_nb=1)

    assert "Game shuts down" in caplog.text


def test_gc_points(two_hands):
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
            gc.start_entire_game(testing_nb=10)
            assert gc.score >= 1


def test_gc_save(caplog):
    # Mocking camera
    img = np.zeros((720, 1280, 3), dtype=np.uint8)
    capture_mock = MagicMock()
    capture_mock.read.return_value = (True, img)
    with patch("cv2.VideoCapture", return_value=capture_mock):
        with requests_mock.Mocker() as m:
            m.post(f"{settings.URL}/game_record/", json={}, status_code=201)
            gc = GamingClient(total_time=1, difficulty="Easy", hand_constraint=False, user_id=1)
            gc.starting_client.timeStart = time.time()
            gc.starting_client.waiting_for_start = False

            assert gc.starting_client.need_to_save is True
            with caplog.at_level(logging.DEBUG):
                gc.start_entire_game(testing_nb=40)

            assert gc.starting_client.need_to_save is False

            assert "Game saved:" in caplog.text


def test_gc_save_error(caplog):
    # Mocking camera
    img = np.zeros((720, 1280, 3), dtype=np.uint8)
    capture_mock = MagicMock()
    capture_mock.read.return_value = (True, img)
    with patch("cv2.VideoCapture", return_value=capture_mock):
        with requests_mock.Mocker() as m:
            m.post(f"{settings.URL}/game_record/", exc=KeyError)  # error doesn't matter
            gc = GamingClient(total_time=1, difficulty="Easy", hand_constraint=False, user_id=1)
            gc.starting_client.timeStart = time.time()
            gc.starting_client.waiting_for_start = False

            with caplog.at_level(logging.DEBUG):
                gc.start_entire_game(testing_nb=40)

            assert "Error while saving" in caplog.text


def test_gc_restart():
    # Mocking camera
    img = np.zeros((720, 1280, 3), dtype=np.uint8)
    capture_mock = MagicMock()
    capture_mock.read.return_value = (True, img)
    with patch("cv2.VideoCapture", return_value=capture_mock):
        gc = GamingClient(total_time=10, difficulty="Easy", hand_constraint=False, user_id=1)
        gc.starting_client.timeStart = time.time()
        gc.starting_client.waiting_for_start = False
        gc.score = 10
        with patch("cv2.waitKey", return_value=ord("r")):
            gc.start_entire_game(testing_nb=10)
            assert gc.score == 0
            assert gc.starting_client.waiting_for_start is True
            assert gc.starting_client.timeStart is None
            assert gc.starting_client.need_to_save is True
