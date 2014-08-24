# -*- coding: utf-8 -*-
# Copyright 2014 Carlos Soriano Sánchez <carlos.soriano89@gmail.com>

import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class Commercial:


    def __init__(self, cityPath, city, simulationModel):
        # For templates
        self.cityPath = cityPath
        self.city = city
        self.simulationModel = simulationModel
