# -*- coding: utf-8 -*-

from BaseFSM import base_fsm

class tl_take_off_fsm(base_fsm):
    def enter_state(self, flight):
        flight.median_filter.refresh()

    def exec_state(self, flight):
        tl_take_off(flight)

    def exit_state(self, flight):
        pass

def tl_take_off(flight):
    ret, frame = flight.read_camera()
    if not ret: return

    
