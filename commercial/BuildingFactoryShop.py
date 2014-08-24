# -*- coding: utf-8 -*-
# Copyright 2014 Carlos Soriano Sánchez <carlos.soriano89@gmail.com>

from commercial.Shop import Shop

class BuildingFactoryShop():

    def createBuilding(self, associatedNode = None, mass = None,  latitude = None,
                       longitude = None, streetName = None, owner = None):
        return Shop(associatedNode, mass, latitude, longitude, streetName, owner)
