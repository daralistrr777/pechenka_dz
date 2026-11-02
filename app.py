import pyautogui
import cv2
import numpy as np
from ultralytics import YOLO
import time
import keyboard

model = YOLO('best.pt')


try:
    template_ad = cv2.imread('close_ad.png', 0)
except:
    template_ad = None

def find_template(screenshot_np, template, threshold=0.8):
    if template is None: return False
    gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val >= threshold:
        h, w = template.shape
        pyautogui.click(max_loc[0] + w // 2, max_loc[1] + h // 2)
        print(f"клик по рекламе. уверенность: {max_val:.2f}")
        return True
    return False

def find_cookie(screenshot_np):
    results = model(screenshot_np, verbose=False)
    for result in results:
        for box in result.boxes:
            if box.conf[0] > 0.6:
                x1, y1, x2, y2 = box.xyxy[0]
                center_x, center_y = (x1 + x2) / 2, (y1 + y2) / 2
                for _ in range(20):
                    pyautogui.click(center_x, center_y)
                    time.sleep(0.005)
                return True
    return False

# мои координаты
UPGRADES = [
    (1611, 267),  # курсор
    (1607, 309),  # бабка
    (1606, 364),  # ферма
    (1606, 413),  # шахта
    (1606, 467),  # хз
    (1606, 515)   # хз
]

BONUS_X, BONUS_Y = 500, 400  

last_upgrade_time = time.time()
last_bonus_time = time.time()

print("esc для выхода.")
while True:
    if keyboard.is_pressed('esc'): break
        
    screenshot = pyautogui.screenshot()
    screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    if find_template(screenshot_np, template_ad, threshold=0.8): 
        time.sleep(1)
        continue
        time.sleep(1)
        continue

    find_cookie(screenshot_np)

    if time.time() - last_upgrade_time > 10:
        for x, y in UPGRADES:
            pyautogui.click(x, y)
            time.sleep(0.05) 
        last_upgrade_time = time.time()
        print("Проверил все улучшения")

    if time.time() - last_bonus_time > 15:
        pyautogui.click(BONUS_X, BONUS_Y)
        print("кликнул по бонусу")
        last_bonus_time = time.time()

    time.sleep(0.1)