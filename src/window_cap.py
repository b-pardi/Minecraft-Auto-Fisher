import mss
import pygetwindow as gw
import numpy as np
import cv2


def get_minecraft_window():
    wins = gw.getWindowsWithTitle('Minecraft')
    if wins: # multiple windows may have minecraft in the name
        print("Found Minecraft windows:")
        for i, window in enumerate(wins):
            print(f"{i + 1}: {window.title} (ID: {window._hWnd})")

        choice = int(input("Enter the number of the window you want to capture: ")) - 1
        if choice < 0 or choice >= len(wins):
            print("Invalid choice")
            return None

    return wins[choice]

def capture_window_frame(window_handler):
    with mss.mss() as sct: # init screen capture tool akin to file opening object
        left, right, top, bottom = window_handler.left, window_handler.right, window_handler.top, window_handler.bottom
        width = right - left
        height = bottom - top

        roi = {
            'top': top + (height // 3),
            'left': left + (width // 3),
            'width': width // 3,
            'height': height // 3
        }

        img = sct.grab(roi)
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        return frame