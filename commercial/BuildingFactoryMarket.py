# -*- coding: utf-8 -*-
# Copyright 2014 Carlos Soriano Sánchez <carlos.soriano89@gmail.com>

from commercial.Market import Market
import BuildingFactory

class BuildingFactoryMarket(BuildingFactory.BuildingFactory):

    def createBuilding(self, associatedNode = None, mass = None,  latitude = None,
                       longitude = None, streetName = None, owner = None):
        return Market(associatedNode, mass, latitude, longitude, streetName, owner)
