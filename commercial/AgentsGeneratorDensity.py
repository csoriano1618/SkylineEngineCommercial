# -*- coding: utf-8 -*-
# Copyright 2014 Carlos Soriano Sánchez <carlos.soriano89@gmail.com>


import CityItemGenerator
import DensityStructure
import ToolsExt
import Agent

class AgentsGeneratorDensity(CityItemGenerator.CityItemGenerator):


    def __init__(self, city, densityDescriptorPath):
        super(AgentsGeneratorDensity, self).__init__(city)
        self.densityDescriptorPath = densityDescriptorPath


    def generate(self):
        agents = []

        self.densityStructure = DensityStructure.DensityStructure(self.city.getStreetsBoundingBox(),
                                                                  self.densityDescriptorPath)
        self.densityStructure.generatePoints()
        majorProgressStep = float(1) / self.densityStructure.getnGridDivisions() * 100
        majorProgress = 0
        print "Generating agents..."
        for indexGrid in range(self.densityStructure.getnGridDivisions()):
            # Progress
            majorProgress = float(indexGrid) / self.densityStructure.getnGridDivisions() * 100
            print str(int(majorProgress)) + "%"
            points = self.densityStructure.getGeneratedPointsForPolygon(indexGrid)
            minorProgress = 0
            # Convert points to agents
            for indexPoints in range(len(points)):
                point = points[indexPoints]
                currentMinorProgress = float(indexPoints) / len(points)
                if (currentMinorProgress - minorProgress > 0.1):
                    minorProgress = currentMinorProgress
                    majorProgressPlusMinorProgress = majorProgress + minorProgress * majorProgressStep
                    print str(int(majorProgressPlusMinorProgress)) + "%"
                try:
                    result = ToolsExt.addNodeToCloserStreetByPoint(self.city, point)
                    agent = Agent.Agent(self.city, result);
                    agents.append(agent)
                except ToolsExt.PointOutsideSegment as e:
                    self.densityStructure.densityPolygons[indexGrid].debugPoints.append([point, e.value])
                except Exception:
                    continue

        return agents
