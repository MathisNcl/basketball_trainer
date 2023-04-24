import numpy as np
import cv2


class Detectors(object):
    def __init__(self):
        # To create the object for backgrounf subtraction from individual frames
        self.fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)

    def detectBall(self, img):
        # Convert RGB to Gray and apply background subtraction
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        fgmask = self.fgbg.apply(gray)

        # Detect all contours in the image
        contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # Find valid contours (radius greater than 10) and their minenclosing circles
        circles = []
        validContours = []
        for contour in contours:
            try:
                (x, y), radius = cv2.minEnclosingCircle(contour)
                if radius > 10:
                    circles.append([x, y, radius])
                    validContours.append(contour)
            except ZeroDivisionError:
                pass

        # Find convex hull of sets of neighbouring contours
        nb_circles = len(circles)
        sets = np.arange(1, nb_circles + 1, 1)
        circles = np.array(circles)
        validContours = np.concatenate(validContours)
        thresh = 25  # Distance threshold
        for i in range(0, nb_circles - 1, 1):
            for j in range(i + 1, nb_circles, 1):
                dist = np.linalg.norm(circles[i][0:2] - circles[j][0:2])
                if dist < thresh:
                    sets[j] = sets[i]

        convHull = []
        for i in np.unique(sets):
            idx = np.where(sets == i)
            cont = np.vstack(validContours[i] for i in idx[0])
            convHull.append(cv2.convexHull(cont))

        similarity = []
        centers = []
        for ch in convHull:
            try:
                (x, y), radius = cv2.minEnclosingCircle(ch)
                theta = np.arange(0, 2 * np.pi, 2 * np.pi / len(ch))
                theta = theta.reshape(len(theta), 1)
                xa = np.int32(x + radius * np.cos(theta))
                ya = np.int32(y + radius * np.sin(theta))
                circle = np.array([xa.T, ya.T]).T
                centers.append([x, y, radius])
                similarity.append(cv2.matchShapes(ch, circle, 1, 0.0) / len(ch))
            except ZeroDivisionError:
                pass

        # find the most similar convex hull and min enclosing circles
        try:
            index = np.argsort(similarity)[0]
            return centers[index]
        except IndexError:
            return None


def main():
    vid = cv2.VideoCapture(0)

    detector = Detectors()
    fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
    background = None
    cpt = 0
    while True:
        _, img = vid.read()
        cpt += 1
        if background is None:
            background = img
            moy = background.copy().astype("float32") / 255
        moy = moy + (img / 255)

        # bcenter = [int(coord) for coord in detector.detectBall(img)]
        # cv2.circle(img, (bcenter[0], bcenter[1]), 10, (0, 100, 100), 3)
        background = (moy / cpt) * 255
        background = background.astype("uint8")

        foreground = abs(img - background)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        fgmask = fgbg.apply(gray)
        contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for i, c in enumerate(contours):
            # draw the contour
            ((x, y), r) = cv2.minEnclosingCircle(c)
            if r > 20:
                # hull = cv2.ConvexHull(contour2)
                cv2.drawContours(img, [c], -1, (0, 255, 0), 2)

        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if key == ord("q"):
            break
    vid.release()
    cv2.destroyAllWindows()


main()
