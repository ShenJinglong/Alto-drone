# -*- coding: utf-8 -*-
import cv2
import time
import multiprocessing

import global_params

from Filter import MedianFilter
from OpticalFlow import OpticalFlow
# from DenseFlow import DenseFlow

if global_params.RASPBERRY_MODE:
    import V_UCom as com

if global_params.USE_VD:
    import V_Display as vd

class Flight(object):
    def __init__(self):
        self.__cap = cv2.VideoCapture(0)
        # self.__cap = cv2.VideoCapture('../videos/2019-07-20 01-18-11.avi')
        # self.__cap = cv2.VideoCapture('../videos/2019-07-26 08-14-59.avi')
        # self.__cap = cv2.VideoCapture('../videos/2019-08-07 23-52-32.avi')

        self.median_filter = MedianFilter()
        self.main_mode = 0x70

        if global_params.RASPBERRY_MODE:
            com.init(mode = 2)
        if global_params.USE_VD:
            vd.init()

        if global_params.RECORD_VIDEO:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.__video_recorder = cv2.VideoWriter('../../Videos/' + time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time())) + '.avi', fourcc, 20.0, (160, 120))

        self.__frame_queue = multiprocessing.Queue(maxsize = 1)
        self.__flow_xy = multiprocessing.Queue(maxsize = 1)
        self.__optical_flow = OpticalFlow(self.__frame_queue, self.__flow_xy)
        self.__optical_flow.start()
        # self.__frame_queue_dense = multiprocessing.Queue(maxsize = 1)
        # self.__flow_xy_dense = multiprocessing.Queue(maxsize = 1)
        # self.__dense_flow = DenseFlow(self.__frame_queue_dense, self.__flow_xy_dense)
        # self.__dense_flow.start()

    def read_camera(self):
        ret, frame = self.__cap.read()
        if ret:
            frame = cv2.resize(frame, (global_params.IMAGE_WIDTH, global_params.IMAGE_HEIGHT))
            try:
                self.__frame_queue.put(frame.copy(), False)
            except:
                pass
            if global_params.RECORD_VIDEO:
                self.__video_recorder.write(frame)
        return ret, frame

    def destroy(self):
        self.__cap.release()
        """
        if self.__optical_flow.is_alive():
            self.__optical_flow.terminate()
            self.__optical_flow.join()
        """
        if self.__optical_flow.is_alive():
            self.__optical_flow.terminate()
            self.__optical_flow.join()

    def send(self, uart_buff):
        # get_bytearray(uart_buff, self)
        if global_params.RASPBERRY_MODE:
            if type(uart_buff) == dict:
                com.send(get_bytearray(uart_buff, self))
            else:
                com.send(uart_buff)

    def get_speed(self):
        x_speed, y_speed = 0, 0
        if not self.__flow_xy.empty():
            x_speed, y_speed = self.__flow_xy.get()
        return (x_speed, y_speed)

    def attach_fsm(self, state, fsm):
        self.__fsm = fsm
        self.curr_state = state
        self.next_state = state

    def change_state(self, new_state, new_fsm):
        self.curr_state = new_state
        self.__fsm.exit_state(self)
        self.__fsm = new_fsm
        self.__fsm.enter_state(self)
        self.__fsm.exec_state(self)

    def keep_state(self):
        self.__fsm.exec_state(self)

def get_bytearray(data_dict, flight):
    if data_dict['mode'] == 'stop_tp':
        dst_point_x = int(data_dict['dst_point_x'])
        flight_mode = flight.main_mode + 0x00
        print('dst_point_x:', dst_point_x)
        return bytearray([0x55, 0xAA, flight_mode, dst_point_x & 0xff,
                          0x00, 0x00, 0x00,        0x00,
                          0x00, 0x00, 0x00,        0xAA               ])
    elif data_dict['mode'] == 'go':
        flight_mode = flight.main_mode + 0x02
        return bytearray([0x55, 0xAA, flight_mode, 0x00,
                          0x00, 0x00, 0x00,        0x00,
                          0x00, 0x00, 0x00,        0xAA ])
    elif data_dict['mode'] == 'go_x':
        flight_angle = int(data_dict['flight_angle'])
        dst_point_y = int(data_dict['dst_point_y'])
        speed_x = int(data_dict['speed_x'])
        speed_y = int(data_dict['speed_y'])
        path_angle = int(data_dict['path_angle'])
        flight_mode = flight.main_mode + 0x02
        print('go_x:', 'f_a:', flight_angle, 'y:', dst_point_y, 's_x:', speed_x, 's_y:', speed_y, 'p_a:', path_angle, 'mo:', flight_mode)
        return bytearray([0x55,               0xAA,                  flight_mode,           flight_angle & 0xff,
                          dst_point_y & 0xff, (speed_x >> 8) & 0xff, speed_x & 0xff, (speed_y >> 8) & 0xff, 
                          speed_y & 0xff,     path_angle & 0xff,     0x00,           0xAA                  ])

        
