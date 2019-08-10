# -*- coding: utf-8 -*-

import cv2
import numpy as np

from BaseFSM import base_fsm
import global_params
from stop_status import stop_params

if global_params.USE_VD:
    import V_Display as vd

class stop_to_circle_fsm(base_fsm):
    def enter_state(self, flight):
        flight.median_filter.refresh()

    def exec_state(self, flight):
        stop_to_circle(flight)

    def exit_state(self, flight):
        pass

params = cv2.SimpleBlobDetector_Params()
params.minThreshold = 20
params.maxThreshold = 200
params.filterByColor = True
params.blobColor = 0
ver = (cv2.__version__).split('.')
if int(ver[0]) < 3 :
    detector = cv2.SimpleBlobDetector(params)
else :
    detector = cv2.SimpleBlobDetector_create(params)

stop_to_circle_counter = 0

def stop_to_circle(flight):
    global stop_to_circle_counter

    ret, frame = flight.read_camera()
    if not ret: return

    keypoints = detector.detect(frame)
    if(keypoints):
        for i in range (0, len(keypoints)):
            x = keypoints[i].pt[0]
            y = keypoints[i].pt[1]
            Postion_x = int(x)
            Postion_y = int(y)
        if len(keypoints) == 1:
            stop_to_circle_counter += 1
    else:
        Postion_x = 80
        Postion_y = 60

    data_to_send = {
        'mode': 'stop_tp',
        'dst_point_x': Postion_x,
        'dst_point_y': Postion_y,
        'speed_x': 0,
        'speed_y': 0
    }
    flight.send(data_to_send)
    im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (255,255,255), cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
    if global_params.USE_VD:
        vd.show(im_with_keypoints)
    else:
        cv2.imshow('frame', im_with_keypoints)
    
    if stop_to_circle_counter == stop_params.STOP_TO_CIRCLE_NUM:
        stop_to_circle_counter = 0
        flight.next_state = macro.STOP_LAND
        print('>>> [!] STOP_TO_CIRCLE -> STOP_LAND')