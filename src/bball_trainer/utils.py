import math
from typing import List, Tuple

import cv2
import cvzone
import numpy as np


def getArea(box: List[int], points: bool = False) -> float:
    """compute area of a bbox

    Args:
        box List[int]: [x, y, w, h] or [x1, y1, w2,y2]
        points bool: Whether to compute area with 2 corner points of the bbox else wioth width and height.
                     Defaults to True.

    Returns:
        float: area
    """

    if points:
        return (box[2] - box[0]) * (box[3] - box[1])
    else:
        return box[2] * box[3]


def incrustration(
    foreground: np.ndarray, background: np.ndarray, begin_corner: List[int]
) -> Tuple[np.ndarray, Tuple[int, int, int, int]]:
    """
    return the original image with the incrusted foregound image in it

    Args:
        foreground (np.ndarray): image to incruste
        background (np.ndarray): background image
        begin_corner (List[int]): coordinates of the top left corner of the incrustation

    Returns:
        Tuple[np.ndarray, Tuple[int, int, int, int]]: background image with the foreground incrustation
    """
    size_x: int = foreground.shape[0]
    size_y: int = foreground.shape[1]
    background_crop: np.ndarray = background[
        begin_corner[1] : begin_corner[1] + size_x, begin_corner[0] : begin_corner[0] + size_y
    ]
    new_background: np.ndarray = np.where((foreground[..., 3] < 128)[..., None], background_crop, foreground[..., 0:3])

    # Change the region with the result
    background[begin_corner[1] : begin_corner[1] + size_x, begin_corner[0] : begin_corner[0] + size_y] = new_background
    x, y, w, h = [begin_corner[0], begin_corner[1], size_y, size_x]
    cv2.rectangle(background, (x, y), (x + w, y + h), (255, 0, 255), 3)
    return background, (x, y, w, h)


def points_distance_is_enough(x1: int, y1: int, x2: int, y2: int, minimal_distance: int = 300) -> bool:
    """
    Whether the distance between points is enough

    Args:
        x1 (int): x coord1
        y1 (int): y coord1
        x2 (int): x coord2
        y2 (int): y coord2
        minimal_distance (int, optional): Minimal distance. Defaults to 300.

    Returns:
        bool: whether the distance is greater than the minimal distance
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) <= minimal_distance


def end_layout(img: np.ndarray, score: int) -> np.ndarray:
    """
    Display the end layout

    Args:
        img (np.ndarray): image to add the end layout
        score (int): final score

    Returns:
        np.ndarray: img with end layout
    """
    cvzone.putTextRect(img, "Game Over", (400, 400), scale=5, offset=30, thickness=7)
    cvzone.putTextRect(img, f"Your Score: {score}", (450, 500), scale=3, offset=20)
    cvzone.putTextRect(img, "Press R to restart", (460, 575), scale=2, offset=10)

    return img
