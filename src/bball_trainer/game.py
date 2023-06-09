import time
from typing import List, Tuple

import cv2
import cvzone
import numpy as np

from bball_trainer.hand_game import HandsDetectorBasketball
from bball_trainer.random_point import RandomPoint
from bball_trainer.starting_client import StartingClient
from bball_trainer.utils import end_layout, points_distance_is_enough

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
img_quart_h: int = int(1280 / 4)
img_quart_v: int = int(720 / 4)

# Hand Detector
detector: HandsDetectorBasketball = HandsDetectorBasketball(detectionCon=0.8, maxHands=2)

# Game Variables
config_point = {
    "xfrom1": 150,
    "xto1": img_quart_h * 2 - 100,
    "xfrom2": img_quart_h * 2 + 100,
    "xto2": 1150,
    "yfrom": 50,
    "yto": 650,
}
point: RandomPoint = RandomPoint(**config_point)
color: Tuple[int, int, int] = (255, 0, 0)
counter: int = 0
score: int = 0
totalTime: int = 5
waiting_for_start: bool = True

left_hand: np.ndarray = cv2.imread("assets/left_hand.png", cv2.IMREAD_UNCHANGED)
size_y: int = 100
size_x: int = 150
left_hand = cv2.resize(left_hand, (size_y, size_x))

begin_left: List[int] = [int(img_quart_h - size_x / 2), int(img_quart_v - size_y / 2)]
begin_right: List[int] = [int(3 * img_quart_h - size_x / 2), int(img_quart_v - size_y / 2)]

starting_client: StartingClient = StartingClient(begin_left, begin_right, left_hand)

# Loop
while True:
    success, img = cap.read()
    img: np.ndarray = cv2.flip(img, 1)  # type: ignore

    hands: List[dict] = detector.findHands(img, draw=False)
    if starting_client.waiting_for_start:
        img = starting_client.starting_layout(hands, img)

    elif time.time() - starting_client.timeStart < totalTime:
        if hands:
            for hand in hands:
                distanceCM = detector.compute_distance(hand=hand)

                if distanceCM > 60:
                    if point.in_bbox(hand):  # type: ignore
                        counter = 1
                detector.print_hand(img, hand, distanceCM)

        if counter:
            counter += 1
            if counter == 2:
                too_close: bool = True
                while too_close:
                    candidate_point: RandomPoint = RandomPoint(**config_point)

                    too_close = points_distance_is_enough(candidate_point.cx, candidate_point.cy, point.cx, point.cy)

                point = candidate_point
                score += 1
                counter = 0

        # Draw Button
        point.draw_circle(img, color)

        # Game HUD
        cvzone.putTextRect(
            img, f"Time: {int(totalTime-(time.time()-starting_client.timeStart))}", (1000, 75), scale=3, offset=20
        )
        cvzone.putTextRect(img, f"Score: {str(score).zfill(2)}", (60, 75), scale=3, offset=20)
    else:
        # End game
        if starting_client.need_to_save:
            # save info
            print("SAVING")
            starting_client.need_to_save = False
        img = end_layout(img, score)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == ord("r"):
        score = 0
        waiting_for_start = True
        starting_client.reset_client()
    if key == ord("q"):
        break
