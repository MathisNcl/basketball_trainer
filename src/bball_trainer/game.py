import time
from typing import List, Optional, Tuple

import cv2
import cvzone
import numpy as np
import requests
import yaml

from bball_trainer import settings
from bball_trainer.hand_game import HandsDetectorBasketball
from bball_trainer.random_point import RandomPoint
from bball_trainer.starting_client import StartingClient
from bball_trainer.utils import end_layout, points_distance_is_enough


class GamingClient:
    """GamingClient with 2 methods: start and stop

    Configured by config.yaml
    """

    def __init__(self, total_time: int, difficulty: str, hand_constraint: bool, user_id: int):
        with open("src/bball_trainer/config.yaml") as f:
            self.config = yaml.safe_load(f)
        # Webcam
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, self.config["cam"]["h"])
        self.cap.set(4, self.config["cam"]["v"])
        self.img_quart_h: int = int(self.config["cam"]["h"] / 4)
        self.img_quart_v: int = int(self.config["cam"]["v"] / 4)

        # Hand Detector
        self.detector: HandsDetectorBasketball = HandsDetectorBasketball(
            detectionCon=self.config["hand_detector"]["detectionCon"], maxHands=self.config["hand_detector"]["maxHands"]
        )

        # Game Variables
        self.config_point = self.config["config_point"]
        self.point: RandomPoint = RandomPoint(**self.config_point)
        self.color: Tuple[int, int, int] = self.config["color"]
        self.counter: int = 0
        self.score: int = 0
        self.totalTime: int = total_time

        # Starting Client
        left_hand: np.ndarray = cv2.imread(self.config["left_hand"]["path"], cv2.IMREAD_UNCHANGED)
        size_y: int = self.config["left_hand"]["size_y"]
        size_x: int = self.config["left_hand"]["size_x"]
        left_hand = cv2.resize(left_hand, (size_y, size_x))

        begin_left: List[int] = [int(self.img_quart_h - size_x / 2), int(self.img_quart_v - size_y / 2)]
        begin_right: List[int] = [int(3 * self.img_quart_h - size_x / 2), int(self.img_quart_v - size_y / 2)]

        self.starting_client: StartingClient = StartingClient(begin_left, begin_right, left_hand)

        # init constructor
        self.difficulty: str = difficulty
        self.hand_constraint: bool = hand_constraint
        self.user_id: int = user_id

    def start(self, testing_nb: Optional[bool] = None) -> None:
        """Start the game by reading camera output"""
        # Loop
        nb_img: int = 0
        while True:
            _, img = self.cap.read()
            nb_img += 1
            img: np.ndarray = cv2.flip(img, 1)  # type: ignore

            hands: List[dict] = self.detector.findHands(img, draw=False, flipType=False)
            if self.starting_client.waiting_for_start:
                img = self.starting_client.starting_layout(hands, img)

            elif time.time() - self.starting_client.timeStart < self.totalTime:
                if hands:
                    for hand in hands:
                        distanceCM = self.detector.compute_distance(hand=hand)

                        if distanceCM > 60:
                            if self.point.in_bbox(hand, hand_constraint=self.hand_constraint):  # type: ignore
                                self.counter = 1
                        self.detector.print_hand(img, hand, distanceCM)

                if self.counter:
                    self.counter += 1
                    if self.counter == 2:
                        too_close: bool = True
                        while too_close:
                            candidate_point: RandomPoint = RandomPoint(**self.config_point)

                            too_close = points_distance_is_enough(
                                candidate_point.cx, candidate_point.cy, self.point.cx, self.point.cy
                            )

                        self.point = candidate_point
                        self.score += 1
                        self.counter = 0

                # Game HUD
                cvzone.putTextRect(
                    img,
                    f"Time: {int(self.totalTime-(time.time()-self.starting_client.timeStart))}",
                    (1000, 75),
                    scale=3,
                    offset=20,
                )
                cvzone.putTextRect(img, f"Score: {str(self.score).zfill(2)}", (60, 75), scale=3, offset=20)

                # Draw Button
                self.point.draw_circle(img, self.color)
            else:
                # End game
                if self.starting_client.need_to_save:
                    # save info
                    # TODO: set a logger
                    requests.post(
                        url=f"{settings.URL}/game_record/", json={"score": self.score, "user_id": int(self.user_id)}
                    )
                    print("SAVED")

                    self.starting_client.need_to_save = False
                img = end_layout(img, self.score)

            cv2.imshow("Image", img)
            key = cv2.waitKey(1)

            if key == ord("r"):
                self.score = 0
                self.starting_client.reset_client()
            if key == ord("q") or testing_nb is not None and testing_nb == nb_img:
                break
        self.stop()

    def stop(self) -> None:
        """Stop camera getter"""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Basketball game", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-u", "--user-id", help="User id", default=1)
    parser.add_argument("-t", "--total-time", help="Game time", default=30)
    parser.add_argument(
        "-d", "--difficulty", help="Game difficulty", default="Easy", choices=["Easy", "Medium", "Hard"]
    )
    parser.add_argument("-hc", "--hand-constraint", help="Whether activate hand constraint or not", default=False)

    args = parser.parse_args()
    config_args = vars(args)

    game = GamingClient(
        int(config_args["total_time"]),
        config_args["difficulty"],
        bool(config_args["hand_constraint"]),
        int(config_args["user_id"]),
    )  # pragma: nocover
    game.start()
