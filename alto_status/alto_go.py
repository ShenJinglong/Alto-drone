# -*- coding: utf-8 -*-

import cv2
import numpy as np

from BaseFSM import base_fsm

from tools import img_tools
from tools import math_tools

import global_params
from alto_status import alto_params
import macro

if global_params.USE_VD:
    import V_Display as vd

class alto_go_fsm(base_fsm):
    def enter_state(self, flight):
        flight.median_filter.refresh()

    def exec_state(self, flight):
        alto_go(flight)

    def exit_state(self, flight):
        pass

alto_go_counter = 0

def alto_go(flight):
    global alto_go_counter

    ret, src_frame = flight.read_camera()
    if not ret: return
    frame = src_frame.copy()

    after_process_img = img_tools.image_pre_process(frame)
    lines = cv2.HoughLines(after_process_img, 1, np.pi / 180, 50, 0, 0)
    lines_class = math_tools.lineClassifier(lines)
    lines_params = math_tools.lineFit(lines_class)
    lines_params = math_tools.remove_vertical_line(lines_params)
    for line in lines_params: img_tools.drawHoughLine(frame, line, (0, 0, 255))

    if len(lines_params) == 1:
        flight.median_filter.add_number_c1(math_tools.getLineWithX(lines_params[0], 0)[1])
        flight.median_filter.add_number_c2(math_tools.getLineAngleX(lines_params[0]))
    else:
        flight.median_filter.add_number_c1(global_params.IMAGE_CENTER_Y - 25)
        flight.median_filter.add_number_c2(0)

    # flight_angle = global_params.FLY_ANGLE_N
    flight_angle = 95
    dst_point_y = flight.median_filter.get_result_number_c1() + 25
    path_angle = flight.median_filter.get_result_number_c2() + 100
    speed_x, speed_y = flight.get_speed()
    data_to_send = {
        'mode': 'go_x',
        'flight_angle': flight_angle,
        'dst_point_y': dst_point_y,
        'speed_x': speed_x,
        'speed_y': speed_y,
        'path_angle': path_angle
    }
    flight.send(data_to_send)
    print('go: %d, %d' % (speed_x, speed_y))

    cv2.circle(frame, (0, int(dst_point_y)), 5, (255, 255, 0), -1)

    pole_buttom_roi = cv2.cvtColor(src_frame[int(global_params.IMAGE_CENTER_Y):int(global_params.IMAGE_HEIGHT), :], cv2.COLOR_BGR2GRAY)
    ret, pole_buttom_roi_th = cv2.threshold(pole_buttom_roi, 40, 255, cv2.THRESH_BINARY_INV)
    # cv2.imshow('fff', pole_buttom_roi_th)

    ret_img, contours, hierarchy = cv2.findContours(pole_buttom_roi_th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    try:
        rects = []
        for contour in contours:
            rect = cv2.minAreaRect(contour)
            w = rect[1][0]
            h = rect[1][1]
            w_h_ratio = max([w, h]) / min([w, h])
            # print(w * h)
            if w * h < 2500 and w * h >  50:
                rects.append(rect)
        img_tools.draw_rotated_rects(frame[int(global_params.IMAGE_CENTER_Y):int(global_params.IMAGE_HEIGHT), :], rects)
    except ZeroDivisionError:
        pass

    if len(rects) == 1:
        alto_go_counter += 1
    else:
        alto_go_counter = 0
    
    # cv2.imshow('ss', pole_buttom_roi_th)
    if global_params.USE_VD:
        vd.show(frame)
    else:
        cv2.imshow('frame', frame)

    if alto_go_counter == alto_params.ALTO_GO_NUM:
        alto_go_counter = 0
        flight.next_state = macro.ALTO_BRAKE_RIGHT
        print('>>> [!] ALTO_GO -> ALTO_BRAKE_RIGHT')

