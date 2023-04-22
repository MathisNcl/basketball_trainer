import math
import random
import time

import cv2
import cvzone
import numpy as np
from cvzone.HandTrackingModule import HandDetector

from typing import Any, List, Tuple

from basketball_trainer.src.utils import incrustration, random_number

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
img_quart_h: int = int(1280 / 4)
img_quart_v: int = int(720 / 4)

# Hand Detector
detector: HandDetector = HandDetector(detectionCon=0.8, maxHands=2)

# Find Function
# x is the raw distance y is the value in cm
x: List[int] = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y: List[int] = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff: np.ndarray = np.polyfit(x, y, 2)  # y = Ax^2 + Bx + C

# Game Variables
cx: int = 250
cy: int = 250
color: Tuple[int] = (255, 0, 0)
counter: int = 0
score: int = 0
timeStart: time = time.time()
totalTime: int = 30
waiting_for_start: bool = True

left_hand: np.ndarray = cv2.imread("assets/left_hand.png", cv2.IMREAD_UNCHANGED)
size_y: int = 100
size_x: int = 150
left_hand = cv2.resize(left_hand, (size_y, size_x))
right_hand: np.ndarray = cv2.flip(left_hand, 1)


begin_left: List[int] = [int(img_quart_h - size_x / 2), int(img_quart_v - size_y / 2)]
begin_right: List[int] = [int(3 * img_quart_h - size_x / 2), int(img_quart_v - size_y / 2)]

# Loop
while True:
    success, img = cap.read()
    img: np.ndarray = cv2.flip(img, 1)

    hands: Any = detector.findHands(img, draw=False)
    if waiting_for_start:
        # add left hand
        img, bbox_left = incrustration(left_hand, img, begin_left)

        # add right hand
        img, bbox_right = incrustration(right_hand, img, begin_right)

        ready: List[bool] = [False, False]
        if hands:
            for hand in hands:
                bbox: List[int] = hand["bbox"]
                cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (255, 0, 255), 3)
                if bbox[0] <= bbox_left[0] and bbox[1] <= bbox_left[1]:
                    # If bottom-right inner box corner is inside the bounding box
                    if (
                        bbox_left[0] + bbox_left[2] <= bbox[0] + bbox[2]
                        and bbox_left[1] + bbox_left[3] <= bbox[1] + bbox[3]
                    ):
                        ready[0] = True
                        cv2.rectangle(
                            img,
                            (bbox_left[0], bbox_left[1]),
                            (bbox_left[0] + bbox_left[2], bbox_left[1] + bbox_left[3]),
                            (0, 0, 255),
                            3,
                        )

                elif bbox[0] < bbox_right[0] and bbox[1] < bbox_right[1]:
                    # If bottom-right inner box corner is inside the bounding box
                    if (
                        bbox_right[0] + bbox_right[2] <= bbox[0] + bbox[2]
                        and bbox_right[1] + bbox_right[3] <= bbox[1] + bbox[3]
                    ):
                        ready[1] = True
                        cv2.rectangle(
                            img,
                            (bbox_right[0], bbox_right[1]),
                            (bbox_right[0] + bbox_right[2], bbox_right[1] + bbox_right[3]),
                            (0, 0, 255),
                            3,
                        )
            if all(ready):
                timeStart = time.time()
                waiting_for_start = False
                print("Game should begin.")

    elif time.time() - timeStart < totalTime:
        if hands:
            for hand in hands:
                lmList = hand["lmList"]
                x, y, w, h = hand["bbox"]
                x1, y1 = lmList[5][:2]
                x2, y2 = lmList[17][:2]

                distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
                A, B, C = coff
                distanceCM = A * distance**2 + B * distance + C

                if distanceCM > 60:
                    if x < cx < x + w and y < cy < y + h:
                        counter = 1
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 3)
                cvzone.putTextRect(img, f"{int(distanceCM)} cm", (x + 5, y - 10))

        if counter:
            counter += 1
            if counter == 2:
                cx = random_number(50, img_quart_h * 2 - 100, img_quart_h * 2 + 100, 1150)
                cy = random.randint(50, 650)
                score += 1
                counter = 0

        # Draw Button
        cv2.circle(img, (cx, cy), 30, color, cv2.FILLED)
        cv2.circle(img, (cx, cy), 10, (255, 255, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 20, (255, 255, 255), 2)
        cv2.circle(img, (cx, cy), 30, (50, 50, 50), 2)

        # Game HUD
        cvzone.putTextRect(img, f"Time: {int(totalTime-(time.time()-timeStart))}", (1000, 75), scale=3, offset=20)
        cvzone.putTextRect(img, f"Score: {str(score).zfill(2)}", (60, 75), scale=3, offset=20)
    else:
        cvzone.putTextRect(img, "Game Over", (400, 400), scale=5, offset=30, thickness=7)
        cvzone.putTextRect(img, f"Your Score: {score}", (450, 500), scale=3, offset=20)
        cvzone.putTextRect(img, "Press R to restart", (460, 575), scale=2, offset=10)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == ord("r"):
        timeStart = time.time()
        score = 0
        waiting_for_start = True
    if key == ord("q"):
        break
