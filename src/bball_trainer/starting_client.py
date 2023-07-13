import time
from typing import Any, List

import cv2
import numpy as np

from bball_trainer import logger
from bball_trainer.utils import incrustration


class StartingClient:
    """
    Client used to determine whether the game should start
    """

    def __init__(self, begin_left: List[int], begin_right: List[int], left_hand: np.ndarray):
        """
        Args:
            begin_left List[int]: top left coordinates of the left hand to display
            begin_right List[int]: top left coordinates of the right hand to display
            left_hand np.ndarray: left hand image in numpy array to display
        """
        self.begin_left: List[int] = begin_left
        self.begin_right: List[int] = begin_right

        self.left_hand: np.ndarray = left_hand
        self.right_hand: np.ndarray = cv2.flip(left_hand, 1)
        self.waiting_for_start: bool = True
        self.timeStart: Any = None
        self.need_to_save: bool = True
        logger.debug("Waiting for start...")

    def starting_layout(self, hands: List[dict], img: np.ndarray) -> np.ndarray:
        """
        Incruste hands and detect whether the game starts

        Args:
            hands (List[dict]): List of dict from HandDetector containing every hand detected
            img (np.ndarray): original image

        Returns:
            np.ndarray: return image with incrustations
        """
        self.ready: List[bool] = [False, False]
        # add left hand
        img, bbox_left = incrustration(self.left_hand, img, self.begin_left)

        # add right hand
        img, bbox_right = incrustration(self.right_hand, img, self.begin_right)

        for hand in hands:
            bbox: List[int] = hand["bbox"]
            cv2.rectangle(
                img,
                (bbox[0], bbox[1]),
                (bbox[0] + bbox[2], bbox[1] + bbox[3]),
                (255, 0, 255),
                3,
            )
            if self.hand_inside_bbox_detected(bbox, bbox_left):
                self.ready[0] = True
                cv2.rectangle(
                    img,
                    (bbox_left[0], bbox_left[1]),
                    (bbox_left[0] + bbox_left[2], bbox_left[1] + bbox_left[3]),
                    (0, 0, 255),
                    3,
                )

            elif self.hand_inside_bbox_detected(bbox, bbox_right):
                self.ready[1] = True
                cv2.rectangle(
                    img,
                    (bbox_right[0], bbox_right[1]),
                    (bbox_right[0] + bbox_right[2], bbox_right[1] + bbox_right[3]),
                    (0, 0, 255),
                    3,
                )
        if all(self.ready):
            self.timeStart = time.time()
            self.waiting_for_start = False
            logger.debug("Game should begin.")

        return img

    def reset_client(self) -> None:
        """used to reset some var"""
        self.waiting_for_start = True
        self.timeStart = None
        self.need_to_save = True
        logger.debug("Waiting for start...")

    @staticmethod
    def hand_inside_bbox_detected(bbox_detected: List[int], draw_bbox: tuple[int, int, int, int]) -> bool:
        """Check whether draw_bbox layout are inside bbox_detected hands

        Args:
            bbox_detected (List[int]): hands bboxes
            draw_bbox (tuple[int, int, int, int]): starting layout bboxes

        Returns:
            bool
        """
        value: bool = False
        if (
            bbox_detected[0] <= draw_bbox[0]
            and bbox_detected[1] <= draw_bbox[1]  # noqa
            and (  # noqa
                draw_bbox[0] + draw_bbox[2] <= bbox_detected[0] + bbox_detected[2]
                and draw_bbox[1] + draw_bbox[3] <= bbox_detected[1] + bbox_detected[3]  # noqa
            )
        ):
            value = True
        return value
