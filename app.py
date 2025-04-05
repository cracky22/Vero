from flask import Flask, render_template, Response, request
from threading import Lock
import time

app = Flask(__name__)

# Speicher für beide Streams
laptop_frame = None
phone_frame = None
laptop_lock = Lock()
phone_lock = Lock()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_laptop', methods=['POST'])
def upload_laptop():
    global laptop_frame
    file = request.files['frame']
    with laptop_lock:
        laptop_frame = file.read()
    return "OK", 200

@app.route('/upload_phone', methods=['POST'])
def upload_phone():
    global phone_frame
    file = request.files['frame']
    with phone_lock:
        phone_frame = file.read()
    return "OK", 200

def generate_stream(get_frame_func, lock):
    while True:
        with lock:
            frame = get_frame_func()
        if frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(1 / 35)  # Ziel: 35 FPS

@app.route('/laptop_feed')
def laptop_feed():
    return Response(generate_stream(lambda: laptop_frame, laptop_lock),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/phone_feed')
def phone_feed():
    return Response(generate_stream(lambda: phone_frame, phone_lock),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, ssl_context=('cert.pem', 'key.pem'))
