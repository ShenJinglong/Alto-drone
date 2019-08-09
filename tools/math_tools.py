# -*- coding: utf-8 -*-
import numpy as np

import global_params

def make_point_safe(point):
    __x = point[0]
    __y = point[1]
    if __x > global_params.IMAGE_WIDTH:
        __x = global_params.IMAGE_WIDTH
    elif __x < 0:
        __x = 0

    if __y > global_params.IMAGE_HEIGHT:
        __y = global_params.IMAGE_HEIGHT
    elif __y < 0:
        __y = 0

    return (__x, __y)

def get_average_point(point_buff):
    if len(point_buff) > 0:
        return (np.mean([point[0] for point in point_buff]), np.mean([point[1] for point in point_buff]))
    else:
        return (global_params.IMAGE_WIDTH / 2, global_params.IMAGE_HEIGHT / 2)

def get_average_number(number_buff):
    return np.mean(number_buff)

def lineClassifier(lines):
    linesClass = []
    linesList = []
    try:
        for line in lines:
            if line[0][0] < 0:
                linesList.append([-line[0][0], line[0][1] - np.pi])
            else:
                linesList.append([line[0][0], line[0][1]])
    except TypeError:
        return linesClass    

    linesList.sort(key = lambda x: x[1])
    flag_indexs = []
    if len(linesList) > 1:
        for i in range(1, len(linesList)):
            if linesList[i][1] - linesList[i - 1][1] > global_params.ANGLE_CLASSIFIER_TH:
                flag_indexs.append(i)
    flag_indexs.insert(0, 0)
    flag_indexs.append(len(linesList))
    for i in range(len(flag_indexs) - 1):
        linesClass.append(linesList[flag_indexs[i]:flag_indexs[i + 1]])
    # print(linesClass)

    __ss_class = []  
    for ss_class in linesClass:
        ss_class.sort(key = lambda x: x[0])
        # print(ss_class)
        flag_indexs = []
        if len(ss_class) > 1:
            for i in range(1, len(ss_class)):
                if ss_class[i][0] - ss_class[i - 1][0] > global_params.RHO_CLASSIFIER_TH:
                    flag_indexs.append(i)
        flag_indexs.insert(0, 0)
        flag_indexs.append(len(ss_class))
        for i in range(len(flag_indexs) - 1):
            __ss_class.append(ss_class[flag_indexs[i]:flag_indexs[i + 1]])
    # print(__ss_class)
    __linesClass = []
    for __class in __ss_class:
        variance = np.var([line[0] for line in __class])
        # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>', variance)
        # print(__class)
        if variance >= global_params.RHO_VARIANCE_MIN and variance <= global_params.RHO_VARIANCE_MAX:
            __linesClass.append(__class)
    return __linesClass

def get_average_per_class(src_lines_class):
    lines_sample = []
    for __class in src_lines_class:
        rhoSample = np.mean([line[0] for line in __class])
        thetaSample = np.mean([line[1] for line in __class])
        lines_sample.append([rhoSample, thetaSample])
    return lines_sample

def lineFit(srcLinesClass):
    linesSample = get_average_per_class(srcLinesClass)
    # print(linesSample)
    indexCollector = set()
    linesRemain = []
    for i in range(len(linesSample)):
        for j in range(i + 1, len(linesSample)):
            if linesSample[i][0] + linesSample[j][0] < 15 \
                and abs(linesSample[i][1] - linesSample[j][1]) < 3.19 \
                and abs(linesSample[i][1] - linesSample[j][1]) > 3.09:
                    indexCollector.add(i)
                    indexCollector.add(j)
                    linesRemain.append(linesSample[i])
    # print(indexCollector)
    _linesSample = []
    for i in range(len(linesSample)):
        if i not in indexCollector:
            _linesSample.append(linesSample[i])
    for line in linesRemain:
        _linesSample.append(line)
    return _linesSample

def findCrossPoint(lines):
    common_form_lines = []
    for line in lines:
        common_form_lines.append([np.cos(line[1]), np.sin(line[1]), line[0]])
    cross_points = []
    for i in range(len(common_form_lines)):
        for j in range(i + 1, len(common_form_lines)):
            A = np.array([common_form_lines[i][:2],
                          common_form_lines[j][:2]])
            b = np.array([common_form_lines[i][2], common_form_lines[j][2]])
            try:
                cross_point = np.linalg.solve(A, b).tolist()
                cross_point = [int(t) for t in cross_point]
                cross_points.append(cross_point)
            except np.linalg.LinAlgError:
                pass
    return [tuple(cross_point) for cross_point in cross_points if 0 < cross_point[0] and cross_point[0] < global_params.IMAGE_WIDTH and 0 < cross_point[1] and cross_point[1] < global_params.IMAGE_HEIGHT]


def getLineWithX(line, asix_x):
    try:
        rho, theta = line[0], line[1]
        if theta == np.pi / 2:
            return (int(asix_x), int(rho))
        else:
            k = -(np.cos(theta) / np.sin(theta))
            b = rho / np.sin(theta)
            y_r = k * asix_x + b
            return (int(asix_x), int(y_r))
    except ValueError:
        return (int(asix_x), int(global_params.IMAGE_HEIGHT / 2))

def getLineWithY(line, asix_y):
    try:
        rho, theta = line[0], line[1]
        if theta == 0:
            return (int(rho), int(asix_y))
        else:
            k = -(np.cos(theta) / np.sin(theta))
            b = rho / np.sin(theta)
            x_r = (asix_y - b) / k
            return (int(x_r), int(asix_y))
    except:
        return (int(global_params.IMAGE_WIDTH / 2), int(asix_y))

def getLineAngleX(line):
    return -int((np.pi/2 - line[1]) * 180 / np.pi)

def getLineAngleY(line):
    return int(line[1] * 180 / np.pi)

def remove_horizontal_line(path_params):
    return [path for path in path_params if path[1] < 0.2 and path[1] > -0.2]

def remove_vertical_line(path_params):
    return [path for path in path_params if path[1] < 1.8 and path[1] > 1.2]
