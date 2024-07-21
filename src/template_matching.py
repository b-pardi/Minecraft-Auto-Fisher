import numpy as np
import cv2


def test_scales_for_template_matching(img, template, scales, threshold):
    found = None
    for scale in scales:
        resized_template = cv2.resize(template, (0, 0), fx=scale, fy=scale)
        #print(scale, template.shape, resized_template.shape, img.shape)
        h, w, _ = resized_template.shape
        res = cv2.matchTemplate(img, resized_template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            if found is None or res[pt[1], pt[0]] > found[0]: # update with BEST match of scales if mult scales
                found = (res[pt[1], pt[0]], pt, w, h, scale)
            break  # If found, break out of the loop

    if found:
        _, max_loc, w, h, scale = found
        return max_loc, w, h, scale
    return None, None, None, None

def template_matching(img, template, thresh):
    found = None
    h, w, _ = template.shape
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= thresh)
    for pt in zip(*loc[::-1]):
        if found is None or res[pt[1], pt[0]] > found[0]: # update with BEST match of scales if mult scales
            found = (res[pt[1], pt[0]], pt, w, h)
        break  # If found, break out of the loop

    if found:
        _, max_loc, w, h = found
        return max_loc, w, h
    return None, None, None

def find_template(frame, templates, thresh):
    for template in templates:
        pt, w, h = template_matching(frame, template, thresh)
        if pt:
            cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0,0,200), 1)
            return frame, True
        
    return frame, False