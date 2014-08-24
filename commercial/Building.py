# -*- coding: utf-8 -*-
# Copyright 2014 Carlos Soriano Sánchez <carlos.soriano89@gmail.com>

import sys,os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Constants
EXPECTED_MIN_AREA = 100   # m²
EXPECTED_MAX_AREA = 30000 # m²

class Building(object):


    def __init__(self, associatedNode = None, mass = None,  latitude = None,
                 longitude = None, streetName = None, owner = None):
        self.associatedNode = associatedNode
        self.agents = []
        self.mass = mass
        self.streetName = streetName
        self.owner = owner
        self.longitude = longitude
        self.latitude = latitude
        self.bankruptcy = False


    def nAgents(self):
        return len(self.agents)


    def setBankruptcy(self, bankruptcy):
        self.bankruptcy = bankruptcy


    def isBankruptcy(self):
        return self.bankruptcy


    def addAgent(self, agent):
        self.agents.append(agent)


    def getLatitude(self):
        return self.latitude


    def getLongitude(self):
        return self.longitude


    def getNumberAgents(self):
        return len(self.agents)


    def getStreetName(self):
        return self.streetName


    def getMass(self):
        return self.mass


    def setAssociatedNode(self, node):
        self.associatedNode = node


    def getAssociatedNode(self):
        return self.associatedNode


    def setLatitude(self, latitude):
        self.latitude = latitude


    def setLongitude(self, longitude):
        self.longitude = longitude


    def setMass(self, mass):
        self.mass = mass


    def setStreetName(self, streetName):
        self.streetName = streetName


    def setOwner(self, owner):
        self.owner = owner


    def getOwner(self):
        return self.owner


    def __str__(self):
        string = "Building\n"

        string = string + "Associated node: " + str(self.associatedNode) + "\n"
        string = string + "Area: " + str(self.mass) + "\n"
        string = string + "Street name: " + str(self.streetName) + "\n"
        string = string + "Owner: " + str(self.owner) + "\n"
        string = string + "Bankruptcy: " + str(self.bankruptcy)

        return string

    __repr__ = __str__
