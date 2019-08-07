# -*- coding: utf-8 -*-

from multiprocessing import Process
import cv2
import numpy as np
import time
import math

import global_params

class DenseFlow(Process):
    def __init__(self, frameQueue, flowXY):
        super(DenseFlow, self).__init__()
        self.__frameQueue = frameQueue
        self.__flowXY = flowXY

    def run(self):
        fps_counter = 0
        fps = 0
        start_time = time.time()
        first_frame_flag = True
        flowX = 0
        flowY = 0
        step = 10

        _x = 0.0
        _y = 0.0

        while True:
            if not self.__frameQueue.empty():
                frame = self.__frameQueue.get()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if first_frame_flag:
                    old_gray = gray
                    first_frame_flag = False
                else:
                    flow = cv2.calcOpticalFlowFarneback(old_gray, gray, None, 0.5, 3, 20, 3, 5, 1.1, 0)
                    old_gray = gray
                    h, w = gray.shape[:2]
                    y, x = np.mgrid[step / 2 : h : step, step / 2 : w : step].reshape(2, -1).astype('int64')
                    fx, fy = flow[y, x].T
                    cnt = len(fx)
                    speed = np.zeros((cnt - 1, 3))
                    for i in range(0, cnt - 1):
                        speed[i][0] = fx[i]
                        speed[i][1] = fy[i]
                        speed[i][2] = math.sqrt(speed[i][0] * speed[i][0] + speed[i][1] * speed[i][1])
                    speed = speed[np.lexsort(-speed.T)]
                    for i in range(1, cnt - 1):
                        if (speed[i][2] <= speed[i - 1][2] * 0.95):
                            speed = np.delete(speed, 0, 0)
                        else:
                            break
                    try:
                        speed = speed[speed[:, 2] >= (max(speed[:, 2]) * 0.8)]
                        flowX = int(np.mean(speed[:, 0]) * fps * 20)
                        flowY = int(np.mean(speed[:, 1]) * fps * 20)
                    except:
                        print('error')
                    
                    try:
                        self.__flowXY.put((flowX, flowY), False)
                    except:
                        pass

                    if not global_params.RASPBERRY_MODE:
                        lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
                        lines = np.int32(lines + 3)
                        vis = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
                        cv2.polylines(vis, lines, 0, (0, 0, 255))
                        for (x1, y1), (x2, y2) in lines:
                            cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
                        cv2.imshow('DenseFlow', vis)
                cv2.waitKey(1)
                fps_counter += 1
                if (time.time() - start_time) > 1:
                    fps = fps_counter / (time.time() - start_time)
                    # print('FPS: %.1f' % (fps))
                    fps_counter = 0
                    start_time = time.time()
