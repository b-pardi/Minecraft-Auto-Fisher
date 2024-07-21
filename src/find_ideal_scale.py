import cv2
import numpy as np
import time
import json
from collections import Counter

from src.window_cap import *
from src.template_matching import *


def find_ideal_scale(thresh):
    window_handler = get_minecraft_window()

    scales = np.arange(0.5, 3, 0.2)
    bobber_templates = [
        [cv2.imread('res/bobber.png'), 'res/bobber.png', -1],
        [cv2.imread('res/bobber_bubbles.png'), 'res/bobber_bubbles.png', -1],
        [cv2.imread('res/bobber_bubbles2.png'), 'res/bobber_bubbles2.png', -1],
    ]

    start_time = time.time()
    cur_time = time.time()
    scale_counts = {template[1]: [] for template in bobber_templates}

    while cur_time - start_time < 60: # run for 1 minute
        cur_time = time.time()
        frame = capture_window_frame(window_handler)
        if frame is not None:
            for template in bobber_templates:
                _, _, _, scale = test_scales_for_template_matching(frame, template[0], scales, thresh)
                if scale:
                    scale_counts[template[1]].append(scale)

    optimal_scales = {}
    for template, scales in scale_counts.items():
        if scales:
            most_common_scale = Counter(scales).most_common(1)[0][0]
        else:
            most_common_scale = None
        optimal_scales[template] = most_common_scale

    with open('res/optimal_template_scales.json', 'w') as f:
        json.dump(optimal_scales, f, indent=4)