# -*- coding: utf-8 -*-

import macro

from ModeSelector import mode_selector_fsm

class fsm_mgr(object):
    def __init__(self):
        self._fsms = {}

        self._fsms[macro.MODE_SELECTOR] = mode_selector_fsm()

    def get_fsm(self, state):
        return self._fsms[state]

    def frame(self, flight):
        if flight.next_state == flight.curr_state:
            flight.keep_state()
        else:
            flight.change_state(flight.next_state, self._fsms[flight.next_state])