import pyautogui
import cv2
import numpy as np
from ultralytics import YOLO
import time
import keyboard 

model = YOLO('best.pt')

def find_and_click():
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)
    screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

    results = model(screenshot_np, verbose=False)

    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            confidence = box.conf[0]

            if confidence > 0.5:
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2

                for _ in range(10):
                    pyautogui.click(center_x, center_y)
                    time.sleep(0.05)
                print(f"Кликнул по {center_x}, {center_y}")
                return True
    return False

print("Работаю... Нажми ESC, чтобы остановить.")
try:
    while True:
        if keyboard.is_pressed('esc'):  # Проверка на Esc
            print("остановлено по Esc!")
            break
        if find_and_click():
            time.sleep(0.5)
        else:
            time.sleep(0.5)
except KeyboardInterrupt:
    print("остановлено вручную.")