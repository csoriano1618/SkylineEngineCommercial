# -*- coding: utf-8 -*-
# Copyright 2014 Carlos Soriano Sánchez <carlos.soriano89@gmail.com>

import CityItemGenerator
import random
from city import City
import ToolsExt
import Building


class BuildingGeneratorRandom(CityItemGenerator.CityItemGenerator):


    def __init__(self, city, factory, numberOfBuildings, areaRange=[10, 1000]):
        super(BuildingGeneratorRandom, self).__init__(city, factory)
        self.areaRange = areaRange
        self.numberOfBuildings = numberOfBuildings


    def generate(self):
        direct = self.city.streetNWAdm.getDirectEdges()
        buildings = []
        for _ in range(self.numberOfBuildings):
            randomNumber = random.randint(0, len(direct) - 1)
            randomEdge = direct[randomNumber]

            # Filter not highway ways and some unwanted highway ways
            if not self.city.isStreetWay(randomEdge[City.WAY]):
                continue

            nodeId = ToolsExt.generateRandomNodeInEdge(randomEdge, self.city)

            randomArea = random.randint(self.areaRange[0], self.areaRange[1])

            building = self.factory.createBuilding(nodeId, randomArea, self.city.getNodeLat(nodeId), self.city.getNodeLon(nodeId))
            buildings.append(building)

        return buildings

