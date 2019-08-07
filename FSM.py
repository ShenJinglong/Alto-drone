# -*- coding: utf-8 -*-

import macro

from ModeSelector import mode_selector_fsm

from tl_status.tl_take_off import tl_take_off_fsm
from tl_status.tl_align_to_start_pole import tl_align_to_start_pole_fsm
from tl_status.tl_detect_bar_code import tl_detect_bar_code_fsm

class fsm_mgr(object):
    def __init__(self):
        self._fsms = {}

        self._fsms[macro.MODE_SELECTOR] = mode_selector_fsm()
        self._fsms[macro.TL_TAKE_OFF] = tl_take_off_fsm()
        self._fsms[macro.TL_ALIGN_TO_START_POLE] = tl_align_to_start_pole_fsm()
        self._fsms[macro.TL_DETECT_BAR_CODE] = tl_detect_bar_code_fsm()

    def get_fsm(self, state):
        return self._fsms[state]

    def frame(self, flight):
        if flight.next_state == flight.curr_state:
            flight.keep_state()
        else:
            flight.change_state(flight.next_state, self._fsms[flight.next_state])