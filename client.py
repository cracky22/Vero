import cv2
import numpy as np
import requests

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

    try:
        resp = requests.get('http://127.0.0.1:5000/frame', timeout=1)
        if resp.status_code == 200:
            jpg = np.frombuffer(resp.content, dtype=np.uint8)
            remote_frame = cv2.imdecode(jpg, cv2.IMREAD_COLOR)
            remote_frame = cv2.resize(remote_frame, (window_width, window_height))
            canvas = remote_frame
    except:
        pass

    canvas[0:pip_height, 0:pip_width] = pip_frame

    cv2.imshow('Vero Konferenz', canvas)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
