from flask import Flask, render_template, Response, request
from threading import Lock
import time

app = Flask(__name__)

# Shared frame storage
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
    target_delay = 1 / 60  # 60 FPS
    while True:
        start = time.time()
        with lock:
            frame = get_frame_func()
        if frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        elapsed = time.time() - start
        sleep_time = max(0, target_delay - elapsed)
        time.sleep(sleep_time)

@app.route('/laptop_feed')
def laptop_feed():
    return Response(generate_stream(lambda: laptop_frame, laptop_lock),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/phone_feed')
def phone_feed():
    return Response(generate_stream(lambda: phone_frame, phone_lock),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    from multiprocessing import cpu_count
    from ssl import SSLContext, PROTOCOL_TLSv1_2
    from OpenSSL import SSL
    # Create SSL context
    context = SSLContext(PROTOCOL_TLSv1_2)
    context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')
    
    # Flask run with SSL enabled
    app.run(host='0.0.0.0', port=5000, ssl_context=context, threaded=True)
