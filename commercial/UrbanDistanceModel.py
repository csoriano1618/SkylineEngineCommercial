# -*- coding: utf-8 -*-
# Copyright 2014 Carlos Soriano Sánchez <carlos.soriano89@gmail.com>

import sys,os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from commercial import SimulationModel
from tools import Astar
import Vars
import Profiler


class UrbanDistanceModel(SimulationModel.SimulationModel):


    def calculate(self):
        if (Vars.isDebug()):
            profiler = Profiler.Profiler('self.calculate_()', globals(), locals())
            profiler.profile()
            profiler.printStats()
        else:
            self.calculate_()


    def calculate_(self):
        for agent in self.agents:
            for building in self.buildings:
                buildingPathData = agent.distanceToBuildingAstar(building.getAssociatedNode())
                if (buildingPathData != None):
                    agent.addBuildingData(buildingPathData.getBuilding(), buildingPathData.getCost(), buildingPathData.getPath())

            # Get the sorthest path
            agentData = agent.getNearestbuildingData()
            if (agentData != None):
                nearestBuildingNode = agentData.getBuilding()
                for building in self.buildings:
                    if (building.associatedNode == nearestBuildingNode):
                        building.addAgent(agent)
                        break

        self.calculateBankruptcy()
