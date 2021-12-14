import pyautogui
import mss
import mss.tools
import cv2
import matplotlib.pyplot as plt
import keyboard
import numpy as np
import time
from win32api import GetSystemMetrics

pyautogui.PAUSE = 0.05

while True:
    if keyboard.is_pressed('backspace'):
        raise KeyboardInterrupt("Keyboard interrupt")
    if keyboard.is_pressed('space'):
        time.sleep(1)
        break

# масштаб текста и других элементов в системе компьютера
scale = 1.5
# размеры игры в браузере
game_block_height = 235
game_width = 600
game_height = 150
browser_top_bar_height = 70
padding = 18
top = browser_top_bar_height + padding + game_block_height - game_height

# высчитываем координаты
top = int((browser_top_bar_height + padding + game_block_height - game_height) * scale)
left = int((GetSystemMetrics(1)/2 - game_width/2) * scale)
width = int(game_width * scale)
height = int(game_height * scale)

with mss.mss() as sct:
    monitor = {"top": top, "left": left, "width": width, "height": height}
    is_obstacle = False
    key = True
    offset = 0 
    start_time  = time.time()
    diff = 10
    while key:
        if keyboard.is_pressed('backspace'):
            print('programm stopped')
            break
        if offset < 770 and time.time() - start_time > diff:
            start_time = time.time()
            diff -= 0.25
            offset += 7
        img = np.array(sct.grab(monitor))
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        mid_line = gray[185, 110:120+offset]
        high_line = gray[150, 110:120+offset]
        if is_obstacle:
            is_obstacle = False
            under_line = gray[195, 5:80]
            while True:
                if not np.all(under_line[:20] == under_line[0]) and np.all(under_line[-10:] == under_line[-10]):
                    pyautogui.keyDown('down')
                    print('down')
                    while np.all(gray[195, 40:70] == gray[195, 0]):
                        img = np.array(sct.grab(monitor))
                        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                    pyautogui.keyUp('down')
                    print('up')
                    break
                img = np.array(sct.grab(monitor))
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                under_line = gray[195, 5:70]
        else:
            if not np.all(mid_line == mid_line[0]):
                pyautogui.press('space')
                print('space pressed')
                is_obstacle = True
            elif not np.all(high_line == high_line[0]):
                pyautogui.keyDown('down')
                print('down')
                while not np.all(high_line == high_line[0]):
                    img = np.array(sct.grab(monitor))
                    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                    high_line = gray[150, 40:120+offset]
                pyautogui.keyUp('down')
                print('up')