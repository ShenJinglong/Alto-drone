# -*- coding: utf-8 -*-

import numpy as np
import cv2
import global_params

def image_pre_process(src_img):
    img = src_img.copy()
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    reduce_noise_img = cv2.GaussianBlur(gray_img, (5,5), 0, 0) # 9，9
    edges = cv2.Canny(reduce_noise_img, 45, 90, apertureSize = 3)

    kernel = np.ones((5, 5), np.uint8)
    dilation = cv2.dilate(edges, kernel, iterations = 1)
#     closing = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
#     opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)

    cadst = cv2.Canny(dilation, 100, 200)
#     cv2.imshow('eee', cadst)
#     cv2.imshow('rrr', edges)
#     cv2.imshow('yyy', closing)
#     cv2.imshow('ttt', opening)
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