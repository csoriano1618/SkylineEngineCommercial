# -*- coding: utf-8 -*-
# Copyright 2014 Carlos Soriano Sánchez <carlos.soriano89@gmail.com>

import sys,os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Constants
EXPECTED_MIN_AREA = 10   # m²
EXPECTED_MAX_AREA = 1000 # m²
import Building

class Market(Building.Building):

    def __str__(self):
        string = "Market\n"
        string = string + super(Market, self).__str__()

        return string

    __repr__ = __str__
