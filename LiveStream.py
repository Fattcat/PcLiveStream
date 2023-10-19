import cv2
import pyautogui
import datetime
import os
from flask import Flask, Response, send_from_directory

app = Flask(__name__)
screenshot_directory = "screenshots"

if not os.path.exists(screenshot_directory):
    os.makedirs(screenshot_directory)

@app.route('/current_screenshot')
def current_screenshot():
    capture_and_save_screenshot()  # Zachyti a uloží aktuálny screenshot
    latest_screenshot = get_latest_screenshot()
    if latest_screenshot:
        return send_from_directory(screenshot_directory, latest_screenshot)
    else:
        return "No screenshots available."

def get_latest_screenshot():
    screenshot_files = os.listdir(screenshot_directory)
    screenshot_files.sort()
    if screenshot_files:
        latest_screenshot = screenshot_files[-1]
        return latest_screenshot
    else:
        return None

def capture_and_save_screenshot():
    screenshot = pyautogui.screenshot()
    current_time = datetime.datetime.now()
    screenshot_filename = os.path.join(screenshot_directory, f"screenshot_{current_time.strftime('%Y%m%d%H%M%S')}.png")
    screenshot.save(screenshot_filename)

@app.route('/')
def index():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Live Screen</title>
        <style>
            body {
                background-color: red;
                text-align: center;
            }
            #screenshot {
                border: 6px solid black;
                border-radius: 2%;  /* Zaoblenie rohov */
                max-width: 100%;
            }
        </style>
    </head>
    <body>
        <button onclick="loadScreenshot()">Load New Screenshot</button>
        <br>
        <img id="screenshot" src="/current_screenshot" alt="Current Screenshot" style="width: 1200px; height: 800px; display: block; margin: 0 auto; margin-top: 200px;">
        <script>
            function loadScreenshot() {
                var screenshotElement = document.getElementById('screenshot');
                screenshotElement.src = "/current_screenshot?" + new Date().getTime();
            }
        </script>
    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    app.run(host='192.168.56.1', port=5000, debug=True)
