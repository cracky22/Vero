#!/usr/bin/python

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

window_width = 1280
window_height = 720

pip_width = 320
pip_height = 180

while True:
    ret, frame = cap.read()
    if not ret:
        break

    pip_frame = cv2.resize(frame, (pip_width, pip_height))
    canvas = np.zeros((window_height, window_width, 3), dtype=np.uint8)
    canvas[0:pip_height, 0:pip_width] = pip_frame

    cv2.imshow('Vero', canvas)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
