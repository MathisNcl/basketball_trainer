from typing import List

import cv2
import numpy as np
import pytest

from bball_trainer.starting_client import StartingClient

left_hand: np.ndarray = cv2.imread("assets/left_hand.png", cv2.IMREAD_UNCHANGED)
size_y: int = 100
size_x: int = 150
left_hand = cv2.resize(left_hand, (size_y, size_x))


img_quart_h: int = 320
img_quart_v: int = 180
begin_left: list[int] = [245, 130]
begin_right: list[int] = [885, 130]


def test_instanciation() -> None:
    with pytest.raises(TypeError):
        StartingClient()
    starting_client: StartingClient = StartingClient(begin_left, begin_right, left_hand)
    assert isinstance(starting_client, StartingClient)


@pytest.mark.parametrize(
    "bbox_detected, draw_bbox, expected",
    [
        ([10, 80, 30, 100], [15, 100, 15, 80], True),
        ([15, 100, 15, 80], [10, 80, 30, 100], False),
    ],
)
def test_hand_inside_bbox_detected(bbox_detected: List[int], draw_bbox: List[int], expected: float) -> None:
    assert StartingClient.hand_inside_bbox_detected(bbox_detected, draw_bbox) == expected


def test_starting_layout_wait() -> None:
    # create a StartingClient object with dummy values
    begin_left = [0, 0]
    begin_right = [0, 0]
    left_hand = np.zeros((100, 100, 4), dtype=np.uint8)
    client = StartingClient(begin_left, begin_right, left_hand)

    # create a dummy image and hands list
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    hands = [
        {"bbox": [10, 10, 50, 50]},
        {"bbox": [200, 200, 50, 50]},
    ]

    # call the starting_layout method and check the output
    output = client.starting_layout(hands, img)
    assert isinstance(output, np.ndarray)
    assert isinstance(client.timeStart, float) or client.timeStart is None
    assert isinstance(client.waiting_for_start, bool)
    assert client.waiting_for_start is True
    assert client.timeStart is None


def test_starting_layout_ready() -> None:
    begin_left = [10, 10]
    begin_right = [150, 10]
    left_hand = np.zeros((20, 20, 4), dtype=np.uint8)
    client = StartingClient(begin_left, begin_right, left_hand)

    # create a dummy image and hands list
    img = np.zeros((400, 400, 3), dtype=np.uint8)
    hands = [
        {"bbox": [10, 10, 40, 40]},
        {"bbox": [150, 10, 40, 40]},
    ]

    # call the starting_layout method and check the output
    output = client.starting_layout(hands, img)

    assert isinstance(output, np.ndarray)
    assert isinstance(client.waiting_for_start, bool)
    assert client.waiting_for_start is False
    assert client.timeStart is not None
    # TODO: Check if the bbox are well printed


def test_starting_layout_reser() -> None:
    begin_left = [10, 10]
    begin_right = [150, 10]
    left_hand = np.zeros((20, 20, 4), dtype=np.uint8)
    client = StartingClient(begin_left, begin_right, left_hand)

    client.waiting_for_start = False
    client.timeStart = 100
    client.need_to_save = False

    client.reset_client()

    assert client.waiting_for_start == True
    assert client.timeStart is None
    assert client.need_to_save == True
