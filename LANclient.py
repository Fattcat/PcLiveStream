import socket
import time
from PIL import ImageGrab
from selenium import webdriver

# Adresa servera a portu
server_address = ("adresa_servera", 8080)

# Inicializácia webového prehliadača
driver = webdriver.Chrome()

def send_screenshot(sock):
    # Získanie screenshotu
    screenshot = ImageGrab.grab()
    
    # Uloženie screenshotu do dočasného súboru
    screenshot_path = "temp_screenshot.png"
    screenshot.save(screenshot_path)

    # Odoslanie screenshotu na server
    with open(screenshot_path, "rb") as img_file:
        img_data = img_file.read()
    sock.sendall(img_data)

    # Zatvorenie dočasného súboru
    sock.close()

    # Aktualizácia webovej stránky s screenshotom
    driver.refresh()

    # Čakanie 6 sekúnd pred ďalším odoslaním screenshotu
    time.sleep(6)

def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(server_address)
        while True:
            send_screenshot(s)

if __name__ == "__main__":
    start_client()
