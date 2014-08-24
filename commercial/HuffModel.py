# -*- coding: utf-8 -*-
# Copyright 2014 Carlos Soriano Sánchez <carlos.soriano89@gmail.com>

import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from commercial import SimulationModel
from commercial import Agent
from tools import CDF
from tools import Astar
import Vars
import Profiler


class HuffModel(SimulationModel.SimulationModel):
    """
    Huff model calculates the probabilities that a consumer goes to
    a commercial area 'j' from origin 'i' with:

    P_i_j = \frac{S_j{^\alpha} T_i_j{^\beta}}{\sum_{k = 1}^{n} S_k{^\alpha} T_i_k{^\beta}}
    * Latex codification

    Where:
    P_i_j = Probability that a consumer goes from 'i' to 'j'
    S_j   = Area of evaluated commercial
    S_k   = Area of other commercials
    T_i_j = Travel time from origin to evaluated commercial
    T_i_k = Travel time from origin to other commercial
    alpha = Sensibility of the consumer to the commercial area
    beta  = Sensibility of consumer to time travel
    n     = Number of other commercials

    alpha is an empirical value, and normally it is 1
    beta is an empirical value, and normally it is -2
    """
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
                buildingPathData = agent.distanceToBuildingEuclidean(building.getAssociatedNode())
                if (buildingPathData != None):
                    agent.addBuildingData(buildingPathData.getBuilding(), buildingPathData.getCost(), buildingPathData.getPath())

            # Initialize Huff formula
            alpha = 1
            beta = -2
            cdfData = []

            # Calculate summatory
            sum = 0
            for building in self.buildings:
                buildingDist = agent.buildingDataByBuilding(building.getAssociatedNode())
                if (buildingDist == None):
                    continue

                T_i_k = buildingDist.getCost()
                T_i_k_pow_beta = pow(T_i_k, beta)
                S_k = building.getMass()
                S_k_pow_alpha = pow(S_k, alpha)
                sum += S_k_pow_alpha * T_i_k_pow_beta

            # Calculate probability for each building
            for building in self.buildings:
                S_j = building.mass
                S_j_pow_alpha = pow(S_j, alpha)

                buildingDist = agent.buildingDataByBuilding(building.getAssociatedNode())
                if (buildingDist == None):
                    continue

                T_i_j = buildingDist.getCost()
                T_i_k_pow_beta = pow(T_i_j, beta)

                P_i_j = (S_j_pow_alpha * T_i_k_pow_beta) / sum

                # Probabilities are better shown if we truncate some decimals
                # Five decimals sounds enough
                P_i_j = round(P_i_j, 5)

                # Store calculated data for further selection with a CDF
                cdfData.append([P_i_j, building.getAssociatedNode()])

            # Select a building using a CDF
            selectedBuilding = CDF.CDF.cdf(cdfData)
            if (selectedBuilding != None):
                for building in self.buildings:
                    if (building.getAssociatedNode() == selectedBuilding):
                        building.addAgent(agent)
                        break

        self.calculateBankruptcy()
