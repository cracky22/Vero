import cv2
import requests

cap = cv2.VideoCapture(0)
url = 'https://localhost:5000/upload_laptop'

while True:
    ret, frame = cap.read()
    if not ret:
        break

    _, img_encoded = cv2.imencode('.jpg', frame)
    try:
        requests.post(url, files={'frame': img_encoded.tobytes()}, verify=False)
    except:
        pass

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
