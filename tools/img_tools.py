# -*- coding: utf-8 -*-

import numpy as np
import cv2
import global_params

def image_pre_process(src_img):
    img = src_img.copy()
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    reduce_noise_img = cv2.GaussianBlur(gray_img, (5,5), 0, 0) # 9，9
    cadst = cv2.Canny(reduce_noise_img, global_params.CANNY_GRID_TH_MIN, global_params.CANNY_GRID_TH_MAX)
#     cv2.imshow('eee', cadst)
    return cadst

def drawHoughLine(_inputArray, singleLine, color):
    rho = singleLine[0]
    theta = singleLine[1]
    
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    
    cv2.line(_inputArray, (x1, y1), (x2, y2), color, 2)

def draw_rotated_rect(frame, rect):
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(frame, [box], -1, (0, 0, 255), 2)

def draw_rotated_rects(frame, rects):
    for rect in rects:
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(frame, [box], -1, (0, 0, 255), 2)