import time
from unittest.mock import MagicMock, patch

import numpy as np
import pytest
import requests_mock

from bball_trainer import settings
from bball_trainer.game import GamingClient
from bball_trainer.hand_game import HandsDetectorBasketball


def test_gc_hand_handler(two_hands):
    img = np.zeros((720, 1280, 3), dtype=np.uint8)
    gc = GamingClient(total_time=10, difficulty="Medium", hand_constraint=False, user_id=1)

    gc.point.cx = 140
    gc.point.cy = 300
    gc.hand_handler(two_hands, img)
    assert gc.counter == 1


def test_gc_hand_handler_no_hands():
    img = np.zeros((720, 1280, 3), dtype=np.uint8)
    gc = GamingClient(total_time=10, difficulty="Medium", hand_constraint=False, user_id=1)

    gc.point.cx = 140
    gc.point.cy = 300
    gc.hand_handler([], img)
    assert gc.counter == 0


@pytest.mark.parametrize(
    "difficulty, counter, nb_img, score_expected, nb_img_expected, new_point_expected",
    [
        ("Easy", 1, 50, 1, 0, True),
        ("Medium", 1, 50, 1, 0, True),
        ("Hard", 1, 50, 1, 0, True),
        ("Easy", 0, 50, 0, 50, False),
        ("Medium", 0, 50, 0, 0, True),
        ("Medium", 0, 40, 0, 40, False),
        ("Hard", 0, 30, 0, 0, True),
        ("Hard", 0, 10, 0, 10, False),
    ],
)
def test_gc_counter_difficulty_handler(
    difficulty, counter, nb_img, score_expected, nb_img_expected, new_point_expected
):
    gc = GamingClient(total_time=10, difficulty=difficulty, hand_constraint=False, user_id=1)

    # set counter to 1 as a point had been hit
    gc.counter = counter
    gc.nb_img = nb_img
    old_point = gc.point
    gc.counter_difficulty_handler()

    assert gc.score == score_expected
    assert gc.counter == 0
    assert gc.nb_img == nb_img_expected

    if new_point_expected:
        assert old_point.cx != gc.point.cx
        assert old_point.cy != gc.point.cy
    else:
        assert old_point.cx == gc.point.cx
        assert old_point.cy == gc.point.cy


def test_gc_determine_new_point():
    gc = GamingClient(total_time=10, difficulty="Medium", hand_constraint=False, user_id=1)
    old_point = gc.point
    gc.determine_new_point()

    assert old_point.cx != gc.point.cx
    assert old_point.cy != gc.point.cy


@pytest.mark.parametrize(
    "total_time, difficulty, hand_constraint, user_id",
    [
        (30, "Easy", False, 1),
        (60, "Medium", True, 2),
        (45, "Hard", True, 3),
    ],
)
def test_gc_start(total_time, difficulty, hand_constraint, user_id):
    # Mocking camera
    img = np.zeros((720, 1280, 3), dtype=np.uint8)
    capture_mock = MagicMock()
    capture_mock.read.return_value = (True, img)
    with patch("cv2.VideoCapture", return_value=capture_mock):
        gc = GamingClient(
            total_time=total_time, difficulty=difficulty, hand_constraint=hand_constraint, user_id=user_id
        )
        gc.start(testing_nb=1)


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
            gc.start(testing_nb=10)
            assert gc.score >= 1


def test_gc_save():
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
            gc.start(testing_nb=40)
            assert gc.starting_client.need_to_save is False


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
            gc.start(testing_nb=10)
            assert gc.score == 0
            assert gc.starting_client.waiting_for_start is True
            assert gc.starting_client.timeStart is None
            assert gc.starting_client.need_to_save is True
