import cv2
import requests
import threading
import numpy as np
from urllib3.exceptions import InsecureRequestWarning
import urllib3

# Deaktiviere SSL-Warnungen
urllib3.disable_warnings(InsecureRequestWarning)

# URL für den Server
UPLOAD_URL = 'https://localhost:5000/upload_laptop'
VIEW_URL = 'https://localhost:5000/phone_feed'

phone_frame = None
frame_lock = threading.Lock()

# Funktion zum Abrufen des Phone-Streams
def fetch_phone_stream():
    global phone_frame
    stream = requests.get(VIEW_URL, stream=True, verify=False)
    bytes_ = b''
    for chunk in stream.iter_content(chunk_size=1024):
        bytes_ += chunk
        a = bytes_.find(b'\xff\xd8')
        b = bytes_.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes_[a:b+2]
            bytes_ = bytes_[b+2:]
            img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            with frame_lock:
                phone_frame = img

# Starte den Streaming-Thread für den Empfang
threading.Thread(target=fetch_phone_stream, daemon=True).start()

# Öffne die Kamera des Laptops
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 60)  # Ziel FPS auf 60 setzen

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Frame an Server senden
    _, jpeg = cv2.imencode('.jpg', frame)
    try:
        requests.post(UPLOAD_URL, files={'frame': jpeg.tobytes()}, verify=False, timeout=0.5)
    except:
        pass

    # Remote-Feed anzeigen
    with frame_lock:
        remote = phone_frame.copy() if phone_frame is not None else None

    if remote is not None:
        h, w = remote.shape[:2]
        small = cv2.resize(frame, (int(w * 0.25), int(h * 0.25)))
        remote[20:20+small.shape[0], 20:20+small.shape[1]] = small
        cv2.imshow('Konferenz', remote)
    else:
        cv2.imshow('Konferenz', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
