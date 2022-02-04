import cv2
import numpy as np

class Tracking:
    def __init__(self, frame, box):
        self.frame = frame
        self.box = box
        self.mask = np.zeros(frame.shape, dtype=np.uint8)
        self.mask[box[1]:box[3], box[0]:box[2]] = 255
        self.mask = cv2.bitwise_and(self.mask, self.mask, mask=self.mask)
        self.mask = cv2.cvtColor(self.mask, cv2.COLOR_BGR2GRAY)
        self.mask = cv2.GaussianBlur(self.mask, (21, 21), 0)
        self.mask = cv2.threshold(self.mask, 0, 255, cv2.THRESH_BINARY)[1]
        self.mask = cv2.dilate(self.mask, None, iterations=2)
        self.mask = cv2.erode(self.mask, None, iterations=2)
        self.mask = cv2.GaussianBlur(self.mask, (21, 21), 0)
        self.mask = cv2.threshold(self.mask, 0, 255, cv2.THRESH_BINARY)[1]
        self.mask = cv2.dilate(self.mask, None, iterations=2)
        self.mask = cv2.erode(self.mask, None, iterations=2)
        self.mask = cv2.GaussianBlur(self.mask, (21, 21), 0)
        self.mask = cv2.threshold(self.mask, 0, 255, cv2.THRESH_BINARY)[1]
        self.mask = cv2.dilate(self.mask, None, iterations=2)
        self.mask = cv2.erode(self.mask, None, iterations=2)
        self.mask = cv2.GaussianBlur(self.mask, (21, 21), 0)