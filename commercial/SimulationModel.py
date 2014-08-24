# -*- coding: utf-8 -*-
# Copyright 2014 Carlos Soriano Sánchez <carlos.soriano89@gmail.com>

import sys,os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Required constants for A* results
AGENT = 0
BUILDING = 1
BANKRUPTCY_THRESHOLD = 40 # Percent of total clients from before


class SimulationModel(object):

    '''
    Interface for simulations models for commercial.
    Params:
        - city: The city instance for which the buildings belongs. The city will not be modified
        - buildings: The buildings for the simulation. It assumes the buildings are inside the graph of
                     streets of the city. Data is modified. Make a copy before if don't want prior data to not be lose.
        - agents: The simulated people for the simulation. It assumes the agents are inside the graph of streets
                  of the city. Data is modified. Make a copy before if don't want prior data to not be lose.
        - previousPredatorBuildings: Parameter of buildings that has been calculated in previous simulations
                                     so the simulation can predict if the building will bankrupt in the new
                                     simulation. This data is only for read.
                                     Also, this is a reference for the list of buildings, so the user can give
                                     the reference to the list in the constructor although is not calculated yet.
                                     But it needs to be calculated before the current simulation is calculated, so just
                                     run the no-predator simulation before this simulation and make sure the list of
                                     buildings is the good one. i.e.:

                                     simulationModel = UrbanDistanceModel.UrbanDistanceModel(city,
                                                                                            buildings,
                                                                                            agents)
                                     simulationModelPredator = UrbanDistanceModel.UrbanDistanceModel(city,
                                                                                                     predatorBuildings,
                                                                                                     agents,
                                                                                                     buildings)
    '''
    def __init__(self, city, buildings, agents, previousPredatorBuildings = []):
        self.city = city

        self.buildings = buildings
        self.agents = agents
        self.previousPredatorBuildings = previousPredatorBuildings


    def calculate(self):
        '''
        The function will apply a model simulation to buildings and agents
        '''
        pass


    def calculateBankruptcy(self):
        for previousPredatorBuilding in self.previousPredatorBuildings:
            currentBuilding = self.searchBuildingByNode(previousPredatorBuilding.getAssociatedNode())
            numAgentsOld = previousPredatorBuilding.nAgents()
            numAgentsCurrent = currentBuilding.nAgents()

            # Just skip if old number of agents were 0
            if (numAgentsOld == 0):
                continue

            if (numAgentsCurrent / float(numAgentsOld) * 100 <= BANKRUPTCY_THRESHOLD):
                currentBuilding.setBankruptcy(True)


    def searchBuildingByNode(self, node):
        buildings = filter(lambda item: item.getAssociatedNode() == node, self.buildings)
        if (len(buildings) > 1):
            raise Exception("Duplicated buildings: " + str(buildings))

        return buildings[0] if len(buildings) == 1 else None