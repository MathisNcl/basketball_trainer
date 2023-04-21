from typing import List, Tuple

import cv2
import numpy as np


# TODO
def iou(bboxA, bboxB):
    return


def incrustration(
    foreground: np.ndarray, background: np.ndarray, begin_corner: List[int]
) -> Tuple[np.ndarray, Tuple[int]]:
    """
    return an the original image with the incrusted foregound image in it
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


def random_number(from1: int, to1: int, from2: int, to2: int):
    """
    give a number in the range [from1, to1] or [from2, to2]
    """
    arr1: int = np.random.randint(from1, to1)
    arr2: int = np.random.randint(from2, to2)
    out: np.ndarray = np.stack((arr1, arr2))
    out: int = np.random.choice(out)
    return out
