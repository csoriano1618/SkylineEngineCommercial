# -*- coding: utf-8 -*-
# Copyright 2014 Carlos Soriano Sánchez <carlos.soriano89@gmail.com

import ToolsExt
import math

EPSILON = 0.001

class DensityPolygon():

    def __init__(self, id, latLngPolygon, density):
        self.id = id
        self.latLngPolygon = latLngPolygon
        self.density = density
        self.generatedPoints = []
        self.debugPoints = []


    def generatePointsForDensity(self):
        # Avoid division by 0 or near 0 if the density is unreal.
        if (self.density <= EPSILON):
            return

        area = ToolsExt.rectangleArea(self.latLngPolygon)
        nPoints = int(math.floor(area * self.density))
        for point in range(nPoints):
            point = ToolsExt.getRandomPointInsideRect(self.latLngPolygon)
            self.generatedPoints.append(point)
