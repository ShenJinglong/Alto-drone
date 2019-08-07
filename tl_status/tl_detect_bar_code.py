# -*- coding: utf-8 -*-

import cv2
import numpy as np

from BaseFSM import base_fsm

from tools import img_tools
from tools import math_tools

import global_params
from tl_status import tl_params

if global_params.USE_VD:
    import V_Display as vd

class tl_detect_bar_code_fsm(base_fsm):
    def enter_state(self, flight):
        flight.median_filter.refresh()

    def exec_state(self, flight):
        tl_detect_bar_code(flight)

    def exit_state(self, flight):
        pass

tl_detect_bar_code_counter = 0

def tl_detect_bar_code(flight):
    global tl_detect_bar_code_counter

    ret, frame = flight.read_camera()
    if not ret: return

    r = frame[:, :, 2]
    g = frame[:, :, 1]
    b = frame[:, :, 0]
    r_b = cv2.subtract(r, b)
    g_b = cv2.subtract(g, b)

    ret, r_b_th = cv2.threshold(r_b, 40, 255, cv2.THRESH_BINARY)
    ret, g_b_th = cv2.threshold(g_b, 40, 255, cv2.THRESH_BINARY)

    dst1 = cv2.bitwise_and(r_b_th, g_b_th)

    kernel = np.ones((5, 5), np.uint8)
    after_dilate = cv2.dilate(dst1, kernel, iterations = 2)
    ret_img, contours, hierarchy = cv2.findContours(after_dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    rects = []
    for contour in contours:
        rect = cv2.minAreaRect(contour)
        w = rect[1][0]
        h = rect[1][1]
        w_h_ratio = max([w, h]) / min([w, h])
        if w * h > 1000 and w_h_ratio > 1.3:
            rects.append(rect)
    img_tools.draw_rotated_rects(frame, rects)

    if len(rects) == 1:
        tl_detect_bar_code_counter += 1
    else:
        tl_detect_bar_code_counter = 0

    data_to_send = {
        'mode': 'go'
    }
    flight.send(data_to_send)

    if global_params.USE_VD:
        vd.show(frame)
    else:
        cv2.imshow('frame', frame)

    if tl_detect_bar_code_counter == tl_params.TL_DETECT_BAR_CODE_NUM:
        tl_detect_bar_code_counter = 0