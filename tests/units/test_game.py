import numpy as np
import pytest

from bball_trainer.game import GamingClient


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
