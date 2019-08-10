# -*- coding: utf-8 -*-

from BaseFSM import base_fsm

import global_params

if global_params.USE_VD:
    import V_Display as vd

class stop_land_fsm(base_fsm):
    def enter_state(self, flight):
        flight.median_filter.refresh()

    def exec_state(self, flight):
        stop_land(flight)

    def exit_state(self, flight):
        pass

def stop_land(flight):
    ret, frame = flight.read_camera()
    if not ret: return

    data_to_send = {
        'mode': 'land'
    }
    flight.send(data_to_send)

    if global_params.USE_VD:
        vd.show(frame)
    else:
        cv2.imshow('frame', frame)
