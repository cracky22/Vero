from flask import Flask, render_template, Response, request
import threading

app = Flask(__name__)
laptop_frame = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_laptop', methods=['POST'])
def upload_laptop():
    global laptop_frame
    file = request.files['frame']
    laptop_frame = file.read()
    return "OK", 200

def generate_laptop_stream():
    global laptop_frame
    while True:
        if laptop_frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + laptop_frame + b'\r\n')

@app.route('/laptop_feed')
def laptop_feed():
    return Response(generate_laptop_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))
