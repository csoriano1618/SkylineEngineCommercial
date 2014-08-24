# -*- coding: utf-8 -*-
# Copyright 2014 Carlos Soriano Sánchez <carlos.soriano89@gmail.com>
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from commercial.BuildingFactoryMarket import BuildingFactoryMarket
from city import City
import Commercial
import ToolsExt
import Building
import random
import AgentsGeneratorRandom
import AgentsGeneratorDensity
import BuildingGeneratorRandom
import BuildingGeneratorCSV
import HuffModel
import UrbanDistanceModel
import copy
import CommercialVisualizer
from commercial.BuildingFactoryShop import BuildingFactoryShop
from parsers import CityToFile
import Vars


SMALL_BUILDING_AREA_RANGE = [10, 100]
LARGE_BUILDING_AREA_RANGE = [500, 1000]


def generateRandomBuildings(numberOfBuildings, city, areaRange=[10, 1000]):
    direct = city.streetNWAdm.getDirectEdges()
    buildings = []
    for _ in range(numberOfBuildings):
        randomNumber = random.randint(0, len(direct) - 1)
        randomEdge = direct[randomNumber]

        # Filter not highway ways and some unwanted highway ways
        if not city.isStreetWay(randomEdge[City.WAY]):
            continue

        nodeId = ToolsExt.generateRandomNodeInEdge(randomEdge, city)

        randomArea = random.randint(areaRange[0], areaRange[1])

        building = Building.Building(nodeId, randomArea, city.getNodeLat(nodeId), city.getNodeLon(nodeId))
        buildings.append(building)

    return buildings


class CommercialGenerator:
    def __init__(self, simulationModelNames, cityPaths, cityPrecomputedPaths = {}, cityBackgrounds = {},
                 densityDescriptorsPath = {}, buildingsDescriptorPath = {}, buildingsDescriptorPredatorPath = {},
                 numAgents = 0, numBuildings= 0, numPredatorBuildings = 0):
        # For templates
        self.simulationModelNames = simulationModelNames
        self.cityPaths = cityPaths
        self.precomputedCityPaths = cityPrecomputedPaths
        self.cityBackgrounds = cityBackgrounds
        self.densityDescriptorsPath = densityDescriptorsPath
        self.buildingsDescriptorPath = buildingsDescriptorPath
        self.buildingsDescriptorPredatorPath = buildingsDescriptorPredatorPath
        self.numAgents = numAgents
        self.numBuildings = numBuildings
        self.numPredatorBuildings = numPredatorBuildings
        self.commercialInstances = []


    def processSimulationTemplate(self):
        # Seems the __main__ scope is different for imported modules
        # so we need to define the debug support inside the runtime outside
        # __main__
        Vars.setDebug(True)

        simulationDatas = []
        for cityPath in self.cityPaths:
            # Use a cached map if it exists
            if (cityPath in self.precomputedCityPaths):
                print "Preloaded city " + cityPath
                city = CityToFile.loadPrecomputedMap(self.precomputedCityPaths.get(cityPath))
                print "Done preloaded"
            else:
                city = City.City(cityPath)
            # Create generator based on given data. If we have data in a CVS file
            # associated to the current city path, we use the CVS file
            # generator, if not, use random generator instead
            if (self.buildingsDescriptorPath.has_key(cityPath)):
                buildingGenerator = BuildingGeneratorCSV.BuildingGeneratorCSV(city,
                                                                              BuildingFactoryShop(),
                                                                              self.buildingsDescriptorPath.get(cityPath))
            else:
                buildingGenerator = BuildingGeneratorRandom.BuildingGeneratorRandom(city,
                                                                                    BuildingFactoryShop(),
                                                                                    self.numBuildings,
                                                                                    SMALL_BUILDING_AREA_RANGE)
            print "Generating buildings..."
            buildings = buildingGenerator.generate()
            print "Buildings generated"
            # Same for the predator case, if we have a CVS file we use it
            predatorBuildings = copy.deepcopy(buildings)
            if (self.buildingsDescriptorPredatorPath.has_key(cityPath)):
                buildingsPredatorGenerator = BuildingGeneratorCSV.BuildingGeneratorCSV(city,
                                                                                       BuildingFactoryMarket(),
                                                                                       self.buildingsDescriptorPredatorPath.get(cityPath))
                predatorBuildings.extend(buildingsPredatorGenerator.generate())
            else:
                buildingsPredatorGenerator = BuildingGeneratorRandom.BuildingGeneratorRandom(city,
                                                                                             BuildingFactoryMarket(),
                                                                                             self.numBuildings,
                                                                                             LARGE_BUILDING_AREA_RANGE)
                predatorBuildings.extend(buildingsPredatorGenerator.generate())
            # Create generator based on given data. If we have a density data
            # associated to the current city path, we use the density
            # generator, if not, use random generator instead
            if (self.densityDescriptorsPath.has_key(cityPath)):
                agentsGenerator = AgentsGeneratorDensity.AgentsGenerajorDensity(city, self.densityDescriptorsPath.get(cityPath))
            else:
                agentsGenerator = AgentsGeneratorRandom.AgentsGeneratorRandom(city, self.numAgents)
            agents = agentsGenerator.generate()

            # We need to acces this to display cells in the visualizer for debug.
            if hasattr(agentsGenerator, 'densityStructure'):
                densityPolygons = agentsGenerator.densityStructure.densityPolygons
            else:
                densityPolygons = None

            for simulationModelName in self.simulationModelNames:
                buildingsCopy = copy.deepcopy(buildings)
                predatorBuildingsCopy = copy.deepcopy(predatorBuildings)
                agentsCopy = copy.deepcopy(agents)
                predatorAgentsCopy = copy.deepcopy(agents)
                # The file name
                windowName = os.path.basename(cityPath)
                if simulationModelName == 'UrbanDistance':
                    simulationModel = UrbanDistanceModel.UrbanDistanceModel(city, buildingsCopy, agentsCopy)
                    simulationModelPredator = UrbanDistanceModel.UrbanDistanceModel(city, predatorBuildingsCopy,
                                                                                    predatorAgentsCopy,  buildingsCopy)
                    windowName += " - Urban distance"
                elif simulationModelName == 'Huff':
                    simulationModel = HuffModel.HuffModel(city, buildingsCopy, agentsCopy)
                    simulationModelPredator = HuffModel.HuffModel(city, predatorBuildingsCopy, predatorAgentsCopy,
                                                                  buildingsCopy)
                    windowName += " - Huff"

                cityBackground = self.cityBackgrounds.get(cityPath) if self.cityBackgrounds.has_key(cityPath) else None
                # Callback to calculate simulation
                callback = lambda simulationModel = simulationModel: simulationModel.calculate()
                callbackPredator = lambda simulationModelPredator = simulationModelPredator: simulationModelPredator.calculate()

                simulationData = { 'commercial': simulationModel,
                                   'cityBackground': cityBackground,
                                   'title': windowName,
                                   'callback': callback,
                                   'densityPolygons': densityPolygons }

                simulationDataPredator = { 'commercial': simulationModelPredator,
                                           'cityBackground': cityBackground,
                                           'title': windowName + ' - Predator',
                                           'callback': callbackPredator,
                                           'densityPolygons': densityPolygons }

                simulationDatas.append(simulationData)
                simulationDatas.append(simulationDataPredator)
                self.commercialInstances.append(Commercial.Commercial(cityPath,
                                                                      city,
                                                                      simulationModel))
                self.commercialInstances.append(Commercial.Commercial(cityPath,
                                                                      city,
                                                                      simulationModelPredator))

        cv = CommercialVisualizer.CommercialVisualizer(simulationDatas)


if __name__ == "__main__":
    from commercial import CommercialGenerator
    import Profiler
    import Vars


    Vars.setDebug(True)

    parent = os.path.join(os.path.dirname(__file__), '..')

    pathFirence = parent + '/osmFiles/firenze/firenze_00.osm'
    pathVenice = parent + '/osmFiles/venice/venice_0.osm'
    pathBarcelona = parent + '/../BigOsmFiles/Barcelona/BarcelonaMercats.osm'
    pathGirona = parent + '/osmFiles/girona/gironaCarme.osm'

    pathPrecomputedCities = { pathFirence: parent +
                                           '/osmFiles/firenze/firenze_00',
                              pathVenice: parent +
                                          '/osmFiles/venice/venice_0',
                              pathGirona: parent +
                                          '/osmFiles/girona/gironaCarme',
                              pathBarcelona: parent +
                                             '/../BigOsmFiles/Barcelona/BarcelonaMercats'}
    pathDensityDescriptor = { pathFirence: parent +
                                           '/osmFiles/firenze/firenze_density.xml',
                              pathVenice: parent +
                                          '/osmFiles/venice/venice_density.xml',
                              pathGirona: parent +
                                          '/osmFiles/girona/girona_density.xml'}
    pathBuildingsDescriptor = { pathVenice: parent +
                                           '/osmFiles/venice/venice_buildings.csv',
                                pathGirona: parent +
                                           '/osmFiles/girona/girona_buildings.csv',
                                pathBarcelona:  parent + '/../BigOsmFiles/Barcelona/Tiendas.csv'}
    pathBuildingsDescriptorPredator = { pathVenice: parent +
                                                    '/osmFiles/venice/venice_buildings_predator.csv',
                                        pathGirona: parent +
                                                    '/osmFiles/girona/girona_buildings_predator.csv',
                                        pathBarcelona:  parent + '/../BigOsmFiles/Barcelona/Mercados.csv'}
    pathCityBackground = { pathBarcelona: parent + '/../BigOsmFiles/Barcelona/background.gif' }
    commercialGenerator = CommercialGenerator.CommercialGenerator(['Huff',
                                                                   'UrbanDistance'],
                                                                  [pathBarcelona],
                                                                  pathPrecomputedCities,
                                                                  pathCityBackground,
                                                                  pathDensityDescriptor,
                                                                  pathBuildingsDescriptor,
                                                                  pathBuildingsDescriptorPredator,
                                                                  5000, # number of agents
                                                                  1, # number of buildins
                                                                  1) # number of predator buildings

    if (Vars.isDebug()):
        profiler = Profiler.Profiler('commercialGenerator.processSimulationTemplate()', globals(), locals())
        profiler.profile()
        profiler.printStats()
    else:
        commercialGenerator.processSimulationTemplate()