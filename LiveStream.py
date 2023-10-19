import cv2
import pyautogui
from flask import Flask, Response, render_template_string
from datetime import datetime

app = Flask(__name__)

connected_users = []

def generate_frames():
    while True:
        screenshot = pyautogui.screenshot()
        frame = cv2.cvtColor(
            cv2.resize(
                cv2.cvtColor(
                    frame, 
                    cv2.COLOR_BGR2RGB
                ), 
                (800, 600)
            ), 
            cv2.COLOR_BGR2RGB
        )
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Live Stream</title>
    </head>
    <body>
        <img src="{{ url_for('video') }}" style="width: 100%; height: auto;">
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/connect')
def connect():
    client_address = request.remote_addr
    connected_users.append(client_address)
    log_connected_users(client_address)
    return "Connected to the stream!"

def log_connected_users(client_address):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('ConnectedUsers.txt', 'a') as file:
        file.write(f"{current_time}\nConnected User: {client_address}\n\n")
    print(f"{current_time}\nConnected User: {client_address}")

if __name__ == '__main__':
    app.run(host='192.168.56.1', port=5000, debug=True)
