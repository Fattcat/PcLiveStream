import socket
import base64
from PIL import Image
from io import BytesIO
from http.server import SimpleHTTPRequestHandler, HTTPServer

# Nastavenie servera na localhost a port 8080
host, port = "0.0.0.0", 8080
server_address = (host, port)

# Adresa pre obrazové súbory
image_path = "screenshot.png"

class ScreenshotHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/screenshot":
            try:
                # Načítanie posledného screenshotu
                with open(image_path, "rb") as img_file:
                    img_data = img_file.read()
                self.send_response(200)
                self.send_header("Content-type", "image/png")
                self.end_headers()
                self.wfile.write(img_data)
            except FileNotFoundError:
                self.send_error(404, "Screenshot not found")

def start_server():
    httpd = HTTPServer(server_address, ScreenshotHandler)
    print(f"Server is running at http://{host}:{port}/screenshot")
    httpd.serve_forever()

if __name__ == "__main__":
    start_server()
