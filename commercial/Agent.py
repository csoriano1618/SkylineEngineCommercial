# -*- coding: utf-8 -*-
# Copyright 2014 Carlos Soriano Sánchez <carlos.soriano89@gmail.com>

import sys,os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from tools import Astar
DIST_AGENT_BUILDINGS = 0

class Agent(object):


    def __init__(self, city, associatedNode):
        self.associatedNode = associatedNode
        self.buildingsPathsData = {}
        self.city = city


    def getNearestbuildingData(self):
        if (len(self.buildingsPathsData) == 0):
            print "There's still not data for buildings"
            return None

        # Some ways are inconexed, so if the agent remains inside one of them
        # it's impossible to calculate a path. Also, the problem can be that
        # some building remains on one inconexed way. So iterate trough the
        # building data to find at least some connected path to some building.
        connectedToSomeBuilding = False
        for data in self.buildingsPathsData.values():
            if (data.getCost() != None):
                connectedToSomeBuilding = True
                break
        if (not connectedToSomeBuilding):
            return None

        nearestBuildingData = self.buildingsPathsData.values()[0]
        for data in self.buildingsPathsData.values():
            # Check if data has valid path and less cost than nearestBuilding, and
            # check if nearestBuilding has invalid data and that evaluates as
            # None < integer = True, which we want to prevent and just use the
            # one in data variable. data variable can be also invalid, but since
            # there's sure at least one data with valid value, just overrides current
            # nearestBuilding and iterate to next data value until the data is not None
            if (data.getCost() < nearestBuildingData.getCost() and
                data.getCost() != None or
                nearestBuildingData.getCost() == None):
                nearestBuildingData = data

        return nearestBuildingData


    def getLatitude(self):
        return self.city.getNodeLat(self.associatedNode)


    def getLongitude(self):
        return self.city.getNodeLon(self.associatedNode)


    def __str__(self):
        string = "Agent\n"

        string = string + "Associated node: " + str(self.associatedNode) + "\n"
        if (len(self.buildingsPathsData) != 0):
            if (self.getNearestbuildingData() != None):
                string = string + "Nearest building: \n"
                shortestPath = self.getNearestbuildingData().path()
                string = string + str(shortestPath[len(shortestPath) - 1]) + "\n"
            else:
                string = string + "No nearest building\n"
            string = string + "Buildings path data: \n"
            string = string + str(self.buildingsPathsData) + "\n"
        else:
            string = string + "There's still not data for buildings\n"

        return string


    def addBuildingData(self, building, cost, path):
        self.buildingsPathsData[building] = BuildingPathData(building, cost, path)


    def buildingDataByBuilding(self, building):
        return self.buildingsPathsData.get(building)


    def distanceToBuildingAstar(self, buildingId):
        # Astar expect a list of goals
        data = Astar.Astar(self.city, [[self.associatedNode, buildingId]]).aggregateResults_d

        if (data.values()[0] != None and data.values()[0][Astar.SHORTEST_PATH_COST] != None):
            return BuildingPathData(buildingId, data.values()[0][Astar.SHORTEST_PATH_COST], data.values()[0][Astar.PATH_NODES])
        else:
           return None


    def distanceToBuildingEuclidean(self, buildingId):
        cost = self.city.nodesDist(self.associatedNode, buildingId)
        return BuildingPathData(buildingId, cost, None)


class BuildingPathData(object):


    def __init__(self, building, cost, path):
        self.building = building
        self.cost = cost
        self.path = path


    def getBuilding(self):
        return self.building


    def getCost(self):
        return self.cost


    def getPath(self):
        return self.path


    def __str__(self):
        string = ""
        string = string + "Building: " + str(self.building) + "\n"
        string = string + "Cost: " + str(self.cost) + "\n"
        string = string + "Path: " + str(self.path) + "\n"

        return string

    __repr__ = __str__
