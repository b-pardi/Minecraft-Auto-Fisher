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

        roi_scalar = 0.2 

        roi_width = int(width * roi_scalar)
        roi_height = int(height * roi_scalar)
        roi_left = left + (width - roi_width) // 2
        roi_top = top + (height - roi_height) // 2

        roi = {
            'top': roi_top,
            'left': roi_left,
            'width': roi_width,
            'height': roi_height
        }

        img = sct.grab(roi)
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        return frame