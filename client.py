import cv2
import threading
import requests
import numpy as np
from urllib3.exceptions import InsecureRequestWarning
import urllib3

urllib3.disable_warnings(InsecureRequestWarning)

REMOTE_URL = 'https://localhost:5000/laptop_feed'

remote_frame = None
frame_lock = threading.Lock()

def fetch_remote_stream():
    global remote_frame
    stream = requests.get(REMOTE_URL, stream=True, verify=False)
    bytes_ = b''
    for chunk in stream.iter_content(chunk_size=1024):
        bytes_ += chunk
        a = bytes_.find(b'\xff\xd8')
        b = bytes_.find(b'\xff\xd9')
        if a != -1 and b != -1 and b > a:
            jpg = bytes_[a:b+2]
            bytes_ = bytes_[b+2:]
            img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            with frame_lock:
                remote_frame = img

# Starte Remote-Stream in separatem Thread
threading.Thread(target=fetch_remote_stream, daemon=True).start()

# Lokale Kamera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 35)

while True:
    ret, local = cap.read()
    if not ret:
        break

    with frame_lock:
        remote = remote_frame.copy() if remote_frame is not None else None

    if remote is not None:
        # Lokales Bild klein einblenden
        h, w = remote.shape[:2]
        overlay = cv2.resize(local, (int(w * 0.25), int(h * 0.25)))
        remote[20:20+overlay.shape[0], 20:20+overlay.shape[1]] = overlay
        cv2.imshow('Videokonferenz', remote)
    else:
        cv2.imshow('Videokonferenz', local)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
