import argparse
import time
from typing import List, Tuple

import cv2
import cvzone
import numpy as np
import yaml

from bball_trainer.hand_game import HandsDetectorBasketball
from bball_trainer.random_point import RandomPoint
from bball_trainer.starting_client import StartingClient
from bball_trainer.utils import end_layout, points_distance_is_enough

with open("src/bball_trainer/config.yaml") as f:
    config = yaml.safe_load(f)

parser = argparse.ArgumentParser(description="Basketball game", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-t", "--total-time", help="Game time", default=30)
parser.add_argument("-d", "--difficulty", help="Game difficulty", default="Easy", choices=["Easy", "Medium", "Hard"])
parser.add_argument("-hc", "--hand-constraint", help="Whether activate hand constraint or not", default=False)

args = parser.parse_args()
config_args = vars(args)
config_args["total_time"] = int(config_args["total_time"])
config_args["hand_constraint"] = bool(config_args["hand_constraint"])
config.update(config_args)

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, config["cam"]["h"])
cap.set(4, config["cam"]["v"])
img_quart_h: int = int(config["cam"]["h"] / 4)
img_quart_v: int = int(config["cam"]["v"] / 4)

# Hand Detector

detector: HandsDetectorBasketball = HandsDetectorBasketball(
    detectionCon=config["hand_detector"]["detectionCon"], maxHands=config["hand_detector"]["maxHands"]
)

# Game Variables
config_point = config["config_point"]
point: RandomPoint = RandomPoint(**config_point)
color: Tuple[int, int, int] = config["color"]
counter: int = 0
score: int = 0
totalTime: int = config["total_time"]
waiting_for_start: bool = True

left_hand: np.ndarray = cv2.imread(config["left_hand"]["path"], cv2.IMREAD_UNCHANGED)
size_y: int = config["left_hand"]["size_y"]
size_x: int = config["left_hand"]["size_x"]
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
            # TODO: set a logger
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
