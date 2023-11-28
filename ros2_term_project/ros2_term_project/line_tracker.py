import cv2
import numpy as np


class LineTracker:
    def __init__(self):
        self._delta = 0.0
        self._delta2 = 0.0

    def process(self, img: np.ndarray) -> None:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 30, 255])

        mask = cv2.inRange(hsv, lower_white, upper_white)

        h, w, d = img.shape
        mask[int(2.5 * h / 4):h, :] = 0
        M = cv2.moments(mask)
        if M['m00'] > 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.circle(img, (cx, cy), 20, (0, 0, 255), -1)
            err = cy - h / 2
            self._delta = err
        # cv2.imshow("mask", mask)
        # cv2.imshow("window", img)
        cv2.waitKey(3)

    def process2(self, img: np.ndarray) -> None:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 30, 255])

        mask = cv2.inRange(hsv, lower_white, upper_white)

        h, w, d = img.shape
        mask[int(2.7 * h / 4):h, :] = 0
        mask[0:int(h / 4), :] = 0
        M = cv2.moments(mask)
        if M['m00'] > 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.circle(img, (cx, cy), 20, (0, 0, 255), -1)
            err = cy - h / 2
            self._delta = err
        # cv2.imshow("mask", mask)
        # cv2.imshow("window", img)
        cv2.waitKey(3)

    def detect_stop_line(self, img: np.ndarray) -> int:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 30, 255])

        stop_line_mask = cv2.inRange(hsv, lower_white, upper_white)

        h, w, d = img.shape

        search_top = int(3.8 * h / 8)
        search_bot = int(4 * h / 8)
        search_left = int(w * 3 / 8)
        search_right = int(w * 5 / 8)

        stop_line_mask[0:search_top, 0:w] = 0
        stop_line_mask[search_bot:h, 0:w] = 0
        stop_line_mask[:, 0:search_left] = 0
        stop_line_mask[:, search_right:w] = 0

        M = cv2.moments(stop_line_mask)
        # cv2.imshow("window1", img)
        # cv2.imshow("stop_line_mask", stop_line_mask)
        cv2.waitKey(3)
        if M['m00'] > 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.circle(img, (cx, cy), 20, (0, 0, 255), -1)
            err = cy - h / 2
            self._delta = err
        return cv2.countNonZero(stop_line_mask)

    @property
    def delta(self):
        return self._delta


def main():
    tracker = LineTracker()
    import time
    for i in range(100):
        img = cv2.imread('/home/ros2/Ros2Projects/oom_ws/src/py_follower/worlds/sample.png')
    tracker.process(img)
    tracker.detect_stop_line(img)
    time.sleep(0.1)


if __name__ == "__main__":
    main()