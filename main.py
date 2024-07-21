import cv2
import pyautogui
import numpy as np
import json
import time
import sys

from src.window_cap import *
from src.template_matching import *
from src.find_ideal_scale import find_ideal_scale




def main():
    window_handler = get_minecraft_window()
    if window_handler is None:
        sys.exit()

    with open('res/optimal_template_scales.json', 'r') as templates_file:
        bobber_templates_dict = json.load(templates_file)

    bobber_templates = []
    for image_fn, scale in bobber_templates_dict.items():
        img = cv2.imread(image_fn)
        img_scaled = cv2.resize(img, (0,0), fx=scale, fy=scale)
        bobber_templates.append(img_scaled)

    thresh = 0.545 # matching threshold
    bobber_last_seen = time.time()
    last_cast_time = time.time()
    bobber_missing_duration = 0.18  # time threshold to detect bobber missing
    fishing_rod_cast_time = 1  # time after which to cast the fishing rod back
    recast_delay = 4 # give a few seconds for object detection to find the bobber again
                    
    while True:
        frame = capture_window_frame(window_handler)
        if frame is not None:
            frame, found = find_template(frame, bobber_templates, thresh)
            current_time = time.time()

            if found:
                bobber_last_seen = current_time
            else:
                if current_time - bobber_last_seen >= bobber_missing_duration and current_time - last_cast_time >= recast_delay:
                    window_handler.activate() # bring focus back to minecraft
                    pyautogui.click(button='right') # pull fishing rod out when bobber missing
                    time.sleep(fishing_rod_cast_time)
                    pyautogui.click(button='right') # recast fishing rod after catch
                    print("Caught!")
                    last_cast_time = current_time  
                    bobber_last_seen = current_time            

            cv2.imshow('Minecraft Bobboer ROI', frame)

            if cv2.waitKey(1) & 0xFF == 27: # close on escape key
                cv2.destroyAllWindows()
                sys.exit()


if __name__ == '__main__':
    main()
    #find_ideal_scale(0.5)