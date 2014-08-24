# -*- coding: utf-8 -*-
# Copyright 2014 Carlos Soriano Sánchez <carlos.soriano89@gmail.com>

import CityItemGenerator
import ToolsExt
from tools import GoogleMaps
import BuildingDataParser
import traceback

class BuildingGeneratorCSV(CityItemGenerator.CityItemGenerator):


    def __init__(self, city, factory, CSVFile):
        super(BuildingGeneratorCSV, self).__init__(city, factory)
        self.CSVFile = CSVFile


    def generate(self):
        buildingsDataParser = BuildingDataParser.BuildingDataParser(self.CSVFile)
        buildings = buildingsDataParser.parseBuildings(self.factory)
        acceptableBuildings = []

        for building in buildings:
            nodeId = None
            # If the building already contains a location, means that the user
            # provided the location in the input data. So we use that.
            if(building.getLatitude() == None or building.getLongitude() == None):
                latLng = GoogleMaps.latlngForAddress(building.getStreetName())
            else:
                latLng = [building.getLatitude(), building.getLongitude()]

            if (latLng is None):
                continue
            try:
                nodeId = ToolsExt.addNodeToCloserStreetByPoint(self.city, latLng)
            except Exception as e:
                continue

            if (nodeId != None):
                building.setAssociatedNode(nodeId)
                building.setLatitude(self.city.getNodeLat(nodeId))
                building.setLongitude(self.city.getNodeLon(nodeId))
                acceptableBuildings.append(building)

        print "Succesful buildings " + str(len(acceptableBuildings)) + " of " + str(len(buildings))
        return acceptableBuildings

