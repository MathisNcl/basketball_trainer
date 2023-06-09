import math
from typing import Any

import cv2
import cvzone
import numpy as np
from cvzone.HandTrackingModule import HandDetector

x: list[int] = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y: list[int] = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff: np.ndarray = np.polyfit(x, y, 2)


class HandsDetectorBasketball(HandDetector):
    A, B, C = coff

    def __init__(self, detectionCon: float = 0.8, maxHands: int = 2):
        super().__init__(detectionCon, maxHands)

    def compute_distance(self, hand: dict) -> float:
        """
        Compute the distance from the webcam to the hand

        Args:
            hand (dict): dict from HandDetector containing hand detected infos

        Returns:
            float: distance in cm
        """
        lmList = hand["lmList"]

        x1, y1 = lmList[5][:2]
        x2, y2 = lmList[17][:2]

        distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
        return self.A * distance**2 + self.B * distance + self.C

    @staticmethod
    def point_in_bbox(hand: dict, point: tuple[int, int]) -> bool:
        """
        Check whether the point is inside the hand bbox

        Args:
            hands (dict): dict from HandDetector containing hand detected infos
            point (tuple[int]): point to touch

        Returns:
            bool: true if inside else false
        """
        inside: bool = False
        cx, cy = point
        x, y, w, h = hand["bbox"]
        if x < cx < x + w and y < cy < y + h:
            inside = True
        return inside

    @staticmethod
    def print_hand(
        img: np.ndarray, hand: dict[str, Any], distanceCM: float, color: tuple[int, int, int] = (255, 0, 255)
    ) -> None:
        """
        Print detected hand on img array

        Args:
            img (np.ndarray): original image
            hands (dict): dict from HandDetector containing hand detected infos
            distanceCM (flaot): hand distance from camera to print
            color (tuple[int]): color for the box

        Returns:
            _: None
        """
        x, y, w, h = hand["bbox"]
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
        cvzone.putTextRect(img, f"{int(distanceCM)} cm", (x + 5, y - 10))  # type: ignore
