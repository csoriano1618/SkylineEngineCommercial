# -*- coding: utf-8 -*-
# Copyright 2014 Carlos Soriano Sánchez <carlos.soriano89@gmail.com


import XMLDensityParser
import DensityPolygon
import math


class DensityStructure:
    '''
    Structure for pupulation density definition.
    The density information is given from a xml file in the form of a divided
    grid with:
    id: the id of the cell
    density: population for each square meter

    The class will divide the bounding box of the city who is passed as a
    parameter and assigned each cell in the divided grid the density specified
    in the xml file. The grid will be divided as follows:

    +--------+---------+---------+
    |        |         |         |
    |   3    |    6    |    9    |
    |        |         |         |
    |--------|---------+---------+
    |        |         |         |
    |   2    |    5    |    8    |
    |        |         |         |
    |--------|---------+---------+
    |        |         |         |
    |   1    |    4    |    7    |
    |        |         |         |
    +--------+---------+---------+

    and the xml file should look like:
    <?xml version="1.0" ?>
    <densityDescriptor>
        <cell>
            <id>0</id>
            <density>0</density>
        </cell>

        <cell>
            <id>1</id>
            <density>0</density>
        </cell>
        ...
        <cell>
            <id>8</id>
            <density>0</density>
        </cell>
    </densityDescriptor>
    '''

    def __init__(self, boundingBox, descriptorFile):
        self.boundingBox = boundingBox
        self.descriptorFile = descriptorFile
        self.densityPolygons = []
        self.generateFromFile(descriptorFile)


    def generateFromFile(self, xmlFilePath):
        xmlParser = XMLDensityParser.XMLDensityParser(xmlFilePath)
        xmlCells = xmlParser.getAllCells()
        self.gridDivisions = xmlParser.getDivisions()

        latDistance = math.fabs(self.boundingBox[0] - self.boundingBox[2])
        lonDistance = math.fabs(self.boundingBox[1] - self.boundingBox[3])

        # We assume a perfect swaure matrix as number of divisions
        latDivisions = math.sqrt(self.gridDivisions)
        lonDivisions = math.sqrt(self.gridDivisions)
        latLength = latDistance / latDivisions
        lonLength = lonDistance / lonDivisions

        # Make a dict of ids and xml nodes to a easy proccesing
        cellIds = { int(xmlParser.getCellId(cell)) : cell for cell in xmlCells }

        for id in range(self.gridDivisions):
            if (id in cellIds):
                density = float(xmlParser.getCellDensity(cellIds[id]))
            else:
                density = 0.
            # i position in the matrix
            i = math.fmod(id, latDivisions)
            lat = i * latDistance / latDivisions
            # j position in the matrix
            j = math.floor(id / latDivisions)
            lon = j * lonDistance / lonDivisions
            point1 = [self.boundingBox[0] + lat, self.boundingBox[1] + lon]
            point2 = [self.boundingBox[0] + lat + latLength,  self.boundingBox[1] + lon]
            point3 = [self.boundingBox[0] + lat + latLength,  self.boundingBox[1] + lon + lonLength]
            point4 = [self.boundingBox[0] + lat,  self.boundingBox[1] + lon + lonLength]
            densityPolygon = DensityPolygon.DensityPolygon(id, [point1, point2, point3, point4], density)
            self.densityPolygons.append(densityPolygon)

        # Sort by id
        self.densityPolygons = sorted(self.densityPolygons, key = lambda polygon: polygon.id)


    def generatePoints(self):
        for polygon in self.densityPolygons:
            polygon.generatePointsForDensity()


    def getGeneratedPointsForPolygon(self, id):
        return self.densityPolygons[id].generatedPoints


    def getnGridDivisions(self):
        return self.gridDivisions
