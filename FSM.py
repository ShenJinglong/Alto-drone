# -*- coding: utf-8 -*-

import macro

from test_status.rect_test import rect_test_fsm

from ModeSelector import mode_selector_fsm

from tl_status.tl_take_off import tl_take_off_fsm
from tl_status.tl_align_to_start_pole import tl_align_to_start_pole_fsm
from tl_status.tl_detect_bar_code import tl_detect_bar_code_fsm

from alto_status.alto_go import alto_go_fsm
from alto_status.alto_brake_right import alto_brake_right_fsm
from alto_status.alto_stop_to_target_pole import alto_stop_to_target_pole_fsm
from alto_status.alto_detect_first_corner import alto_detect_first_corner_fsm
from alto_status.alto_stop_to_first_corner import alto_stop_to_first_corner_fsm
from alto_status.alto_detect_second_corner import alto_detect_second_corner_fsm
from alto_status.alto_stop_to_second_corner import alto_stop_to_second_corner_fsm
from alto_status.alto_back import alto_back_fsm
from alto_status.alto_detect_end_pole import alto_detect_end_pole_fsm
from alto_status.alto_brake_left import alto_brake_left_fsm
from alto_status.alto_land import alto_land_fsm


from alto_status.alto_turn_1 import alto_turn_1_fsm
from alto_status.alto_brake_1 import alto_brake_1_fsm
from alto_status.alto_turn_2 import alto_turn_2_fsm
from alto_status.alto_brake_2 import alto_brake_2_fsm

class fsm_mgr(object):
    def __init__(self):
        self._fsms = {}

        self._fsms[macro.RECT_TEST] = rect_test_fsm()

        self._fsms[macro.MODE_SELECTOR] = mode_selector_fsm()
        self._fsms[macro.TL_TAKE_OFF] = tl_take_off_fsm()
        self._fsms[macro.TL_ALIGN_TO_START_POLE] = tl_align_to_start_pole_fsm()
        self._fsms[macro.TL_DETECT_BAR_CODE] = tl_detect_bar_code_fsm()

        self._fsms[macro.ALTO_GO] = alto_go_fsm()
        self._fsms[macro.ALTO_BRAKE_RIGHT] = alto_brake_right_fsm()
        self._fsms[macro.ALTO_STOP_TO_TARGET_POLE] = alto_stop_to_target_pole_fsm()
        self._fsms[macro.ALTO_DETECT_FIRST_CORNER] = alto_detect_first_corner_fsm()
        self._fsms[macro.ALTO_STOP_TO_FIRST_CORNER] = alto_stop_to_first_corner_fsm()
        self._fsms[macro.ALTO_DETECT_SECOND_CORNER] = alto_detect_second_corner_fsm()
        self._fsms[macro.ALTO_STOP_TO_SECOND_CORNER] = alto_stop_to_second_corner_fsm()
        self._fsms[macro.ALTO_BACK] = alto_back_fsm()
        self._fsms[macro.ALTO_DETECT_END_POLE] = alto_detect_end_pole_fsm()
        self._fsms[macro.ALTO_BREAK_LEFT] = alto_brake_left_fsm()
        self._fsms[macro.ALTO_LAND] = alto_land_fsm()

        self._fsms[macro.ALTO_TURN_1] = alto_turn_1_fsm()
        self._fsms[macro.ALTO_BREAK_1] = alto_brake_1_fsm()
        self._fsms[macro.ALTO_TURN_2] = alto_turn_2_fsm()
        self._fsms[macro.ALTO_BREAK_2] = alto_brake_2_fsm()

    def get_fsm(self, state):
        return self._fsms[state]

    def frame(self, flight):
        if flight.next_state == flight.curr_state:
            flight.keep_state()
        else:
            flight.change_state(flight.next_state, self._fsms[flight.next_state])