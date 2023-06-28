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
    """GamingClient with many methods to implement the basketball handle game

    Configured by config.yaml
    """

    def __init__(self, total_time: int, difficulty: str, hand_constraint: bool, user_id: int):
        with open("src/bball_trainer/config.yaml") as f:
            self.config = yaml.safe_load(f)
        self.img_quart_h: int = int(self.config["cam"]["h"] / 4)
        self.img_quart_v: int = int(self.config["cam"]["v"] / 4)
        self.nb_img: int = 0

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
        self.difficulty_time: Optional[int] = self.config["difficulty_time"][self.difficulty]
        self.hand_constraint: bool = hand_constraint
        self.user_id: int = user_id

    def turn_on_camera(self) -> None:
        """Only tu turn on camera instead of doing it in contstructor"""
        # Webcam
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, self.config["cam"]["h"])
        self.cap.set(4, self.config["cam"]["v"])

    def start(self, testing_nb: Optional[bool] = None) -> None:
        """Start the game by reading camera output"""

        self.turn_on_camera()
        # Loop
        while True:
            _, img = self.cap.read()
            self.nb_img += 1
            img: np.ndarray = cv2.flip(img, 1)  # type: ignore

            hands: List[dict] = self.detector.findHands(img, draw=False, flipType=False)
            if self.starting_client.waiting_for_start:
                img = self.starting_client.starting_layout(hands, img)

            elif time.time() - self.starting_client.timeStart < self.totalTime:
                self.hand_handler(hands, img)

                self.counter_difficulty_handler()

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
                    # TODO: set a logger and a check for status code == 201
                    requests.post(
                        url=f"{settings.URL}/game_record/",
                        json={
                            "score": self.score,
                            "user_id": int(self.user_id),
                            "time": self.totalTime,
                            "difficulty": self.difficulty,
                        },
                    )
                    print("SAVED")

                    self.starting_client.need_to_save = False
                img = end_layout(img, self.score)

            if testing_nb is not None:  # only for gitub tests :(
                cv2.imshow("Image", img)
            key = cv2.waitKey(1)

            if key == ord("r"):
                self.score = 0
                self.starting_client.reset_client()
            if key == ord("q") or testing_nb is not None and testing_nb == self.nb_img:
                break
        self.stop()

    def hand_handler(self, hands: List[dict], img: np.ndarray) -> None:
        """Print hands in img and detect whether the counter should be incremented

        Args:
            hands (List[dict]): List of detected hands
            img (np.ndarray): Image from the camera
        """
        if hands:
            for hand in hands:
                distanceCM = self.detector.compute_distance(hand=hand)

                if distanceCM > 60:
                    if self.point.in_bbox(hand, hand_constraint=self.hand_constraint):  # type: ignore
                        self.counter = 1
                self.detector.print_hand(img, hand, distanceCM)

    def counter_difficulty_handler(self) -> None:
        """Increment score if counter is equal to 1 (ie a point is inside a hand) and change the location of the point
        When difficulty is different then Easy, the point is automatically changed after x number of images red by
        the webcam device
        """
        if self.counter:
            self.determine_new_point()
            self.score += 1
            self.counter = 0
            self.nb_img = 0
        # Change point if difficulty
        elif self.difficulty_time is not None and self.nb_img + 1 >= int(self.difficulty_time):
            self.determine_new_point()
            self.nb_img = 0

    def determine_new_point(self) -> None:
        """Methods which compute a new random point"""
        too_close: bool = True
        while too_close:
            candidate_point: RandomPoint = RandomPoint(**self.config_point)

            too_close = points_distance_is_enough(candidate_point.cx, candidate_point.cy, self.point.cx, self.point.cy)

        self.point = candidate_point

    def stop(self) -> None:
        """Stop camera getter"""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":  # pragma: nocover
    import argparse

    parser = argparse.ArgumentParser(
        description="Basketball game", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-u", "--user-id", help="User id", default=1)
    parser.add_argument("-t", "--total-time", help="Game time", default=30)
    parser.add_argument(
        "-d", "--difficulty", help="Game difficulty", default="Hard", choices=["Easy", "Medium", "Hard"]
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
