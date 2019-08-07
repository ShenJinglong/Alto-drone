# -*- coding: utf-8 -*-

import numpy as np
import cv2
import global_params


def image_pre_process(src_img):
    img = src_img.copy()
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    reduce_noise_img = cv2.GaussianBlur(gray_img, (5,5), 0, 0) # 9，9
    # equ = cv2.equalizeHist(reduce_noise_img)
    # ret, th_img = cv2.threshold(reduce_noise_img, 0, 255, cv2.THRESH_OTSU)
    # cadst = cv2.Canny(th_img, my_params.CANNY_GRID_TH_MIN, my_params.CANNY_GRID_TH_MAX)
    cadst = cv2.Canny(reduce_noise_img, global_params.CANNY_GRID_TH_MIN, global_params.CANNY_GRID_TH_MAX)
    # cv2.imshow('reduce_noise_img', reduce_noise_img)
    # cv2.imshow('cadst', cadst)
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
