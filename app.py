from flask import Flask, render_template, Response, request
import cv2
import base64

app = Flask(__name__)
latest_frame = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    global latest_frame
    data_url = request.form['frame']
    header, encoded = data_url.split(',', 1)
    latest_frame = base64.b64decode(encoded)
    return '', 204

@app.route('/frame')
def frame():
    global latest_frame
    if latest_frame:
        return Response(latest_frame, mimetype='image/jpeg')
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))