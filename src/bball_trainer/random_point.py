import random

import cv2
import numpy as np


class RandomPoint:
    """
    Args:
        from1 (int): lower bound coord1
        to1 (int): upper bound coord1
        from2 (int): lower bound coord2
        to2 (int): upper bound coord2
    """

    def __init__(self, xfrom1: int, xto1: int, xfrom2: int, xto2: int, yfrom: int, yto: int):
        self.xfrom1: int = xfrom1
        self.xto1: int = xto1
        self.xfrom2: int = xfrom2
        self.xto2: int = xto2
        self.cx = self.random_coordinates_x()
        self.cy = random.randint(yfrom, yto)

        self.side: str = self.get_side()

    def random_coordinates_x(self) -> int:
        """
        give two coordinates number in the range [from1, to1] or [from2, to2]

        Returns:
            int: random coordinates
        """
        arr1: int = np.random.randint(self.xfrom1, self.xto1)
        arr2: int = np.random.randint(self.xfrom2, self.xto2)
        out: np.ndarray = np.stack((arr1, arr2))
        return np.random.choice(out)

    def get_side(self) -> str:
        if self.cx <= self.xto1:
            return "Left"
        else:
            return "Right"

    def in_bbox(self, hand: dict, hand_constraint: bool = False) -> bool:
        """
        Check whether the point is inside the hand bbox

        Args:
            hand (dict): dict from HandDetector containing hand detected infos

        Returns:
            bool: true if inside else false
        """
        inside: bool = False
        x, y, w, h = hand["bbox"]

        if x < self.cx < x + w and y < self.cy < y + h:
            inside = True

        if inside and hand_constraint:
            inside = hand["type"] == self.side

        return inside

    def draw_circle(self, img: np.ndarray, color: tuple) -> None:
        """
        draw a nice circle

        Args:
            img (np.ndarray): img to add a circle
            color (tuple): color to display the point
        """
        cv2.circle(img, (self.cx, self.cy), 30, color, cv2.FILLED)
        cv2.circle(img, (self.cx, self.cy), 10, (255, 255, 255), cv2.FILLED)
        cv2.circle(img, (self.cx, self.cy), 20, (255, 255, 255), 2)
        cv2.circle(img, (self.cx, self.cy), 30, (50, 50, 50), 2)
