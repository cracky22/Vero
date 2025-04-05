from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Initialisiere die Kamera
cap = cv2.VideoCapture(0)

def generate_frame():
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Bild in RGB umwandeln
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Bild in JPEG komprimieren
        _, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()
        
        # Sende das Bild als HTTP-Response (Video-Stream)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))
