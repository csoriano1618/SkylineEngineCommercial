# -*- coding: utf-8 -*-
# Copyright 2014 Carlos Soriano Sánchez <carlos.soriano89@gmail.com>

import csv
import Building

# Constants to access parsed data
OWNER = 0
STREET_NAME = 1
MASS = 2
LAT = 3
LON = 4

class BuildingDataParser:
    '''
    Class to parse the building data from a csv file.
    The data should be formatted as follow:
    - First column: owner
    - Second column: street name as OSM has in its data base
    - Third column: mass value of the building. (it can be in m², money, importance, etc.)

    If some value of some row is empty, the entire row will be skipped.
    '''
    def __init__(self, filePath):
        self.filePath = filePath
        self.reader = csv.reader(file(filePath))

    def parseBuildings(self, factory):
        buildings = []
        for row in self.reader:
            if (row[OWNER] is not None and
                row[STREET_NAME] is not None and
                row[MASS] is not None):
                if (float(row[MASS]) < 800):
                    continue
                building = factory.createBuilding()
                building.setMass(float(row[MASS]))
                building.setStreetName(row[STREET_NAME] + ", barcelona, spain")
                building.setOwner(row[OWNER])
                if (len(row) > LON and row[LAT] and row[LON]):
                    building.setLatitude(float(row[LAT]))
                    building.setLongitude(float(row[LON]))
                buildings.append(building)

        return buildings

if __name__ == "__main__":
    import csv

    reader = csv.reader(file('/home/carlos/Documents/CSVSample.csv'))
    for row in reader:
        print row
