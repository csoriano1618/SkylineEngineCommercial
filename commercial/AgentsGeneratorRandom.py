# -*- coding: utf-8 -*-
# Copyright 2014 Carlos Soriano Sánchez <carlos.soriano89@gmail.com>

import CityItemGenerator
import random
from city import City
import Agent
import ToolsExt


class AgentsGeneratorRandom(CityItemGenerator.CityItemGenerator):


    def __init__(self, city, numberOfAgents):
        super(AgentsGeneratorRandom, self).__init__(city)
        self.numberOfAgents = numberOfAgents


    def generate(self):
        direct = self.city.streetNWAdm.getDirectEdges()
        agents = []
        for _ in range(self.numberOfAgents):
            randomNumber = random.randint(0, len(direct) - 1)
            randomEdge = direct[randomNumber]

            # Filter not highway ways and some unwanted highway ways
            if (not self.city.isStreetWay(randomEdge[City.WAY])):
                continue
            try:
                nodeId = ToolsExt.generateRandomNodeInEdge(randomEdge, self.city)
            except Exception as e:
                continue

            agent = Agent.Agent(self.city, nodeId);
            agents.append(agent)

        return agents

