# -*- coding: utf-8 -*-
import sys

RECORD_VIDEO = True

IMAGE_WIDTH = 160
IMAGE_HEIGHT = 120
IMAGE_CENTER_X = IMAGE_WIDTH / 2
IMAGE_CENTER_Y = IMAGE_HEIGHT / 2

FLY_ANGLE_P = 110
FLY_ANGLE_N = 90

POINT_RECORD_NUM = 5
NUMBER_RECORD_NUM = 5

RASPBERRY_MODE = True if sys.platform == 'linux2' else False
USE_VD = True if sys.platform == 'linux2' else False

MODE_PIN_1 = 7
MODE_PIN_2 = 8
MODE_PIN_3 = 9
MODE_PIN_4 = 10

"""
CANNY_GRID_TH_MAX = 230    # 150   # 180 # 250                                       # Canny 梯度大阈值 # 200
CANNY_GRID_TH_MIN = 120    # 100                                                     # Canny 梯度小阈值 # 120

HOUGH_LINES_POINT_TH = 30  # 35 # 30                                                 # 霍夫直线检测阈值 # 35

TRACK_LINE_RIGHT_X = 160                                                             # 向右巡线时的固定横坐标
TRACK_LINE_UP_Y = 0                                                                  # 向上巡线时的固定纵坐标
TRACK_LINE_LEFT_X = 0                                                                # 向左巡线时的固定横坐标
TRACK_LINE_DOWN_Y = 120                                                              # 向下巡线时的固定纵坐标

ANGLE_CLASSIFIER_TH = 0.3                                                            # 角度分类阈值 # 0.2

RHO_VARIANCE_MIN = 10                                                                # 直线极径最小方差
RHO_VARIANCE_MAX = 100                                                               # 直线极径最大方差
"""

CANNY_GRID_TH_MIN = 65
CANNY_GRID_TH_MAX = 130

ANGLE_CLASSIFIER_TH = 0.3
RHO_CLASSIFIER_TH = 50

RHO_VARIANCE_MIN = 0
RHO_VARIANCE_MAX = 500