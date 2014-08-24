import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def toFile(city, outputName):
    
    f = open((outputName + '.py'), 'w')
    
    f.write("from city.City import *\n\n")
    
    f.write("def getCity():\n\n")
    #city object
    f.write("\tcity = City()\n")
    f.write("\tcity.boundingBox = " + str(city.getBoundingBox())+ "\n")
    f.write("\tcity.effectiveBoundingBox = " + str(city.getEffectiveBoundingBox()) + "\n")
    f.write("\tcity.nodes_d = " + str(city.getNodes_d()) + "\n")
    f.write("\tcity.ways_d = " + str(city.getWays_d()) + "\n\n")
    #street bounding box
    f.write("\tcity.streetNWAdm.streetsBoundingBox = " + str(city.streetNWAdm.getStreetsBoundingBox()) + "\n")
    #direct graph
    f.write("\tcity.streetNWAdm.directG.edges_l = " + str(city.streetNWAdm.getDirectEdges()) + "\n")
    #dual graph
    f.write("\tcity.streetNWAdm.dualG.edges_l = " + str(city.streetNWAdm.getDualEdges()) + "\n")
    #intersection accelerator
    f.write("\tcity.streetNWAdm.intAcc.intersections_d = " + str(city.streetNWAdm.getIntAcc()) + "\n")
    #proximity accelerator
    f.write("\tcity.streetNWAdm.proxAcc._ProximityAccelerator__cellSize = " + str(city.streetNWAdm.proxAcc.getCellSize()) + "\n")
    f.write("\tcity.streetNWAdm.proxAcc._ProximityAccelerator__gridBB = " + str(city.streetNWAdm.proxAcc.getGridBB()) + "\n")
    f.write("\tcity.streetNWAdm.proxAcc._ProximityAccelerator__gridSize = " + str(city.streetNWAdm.proxAcc.getGridSize()) + "\n")
    f.write("\tcity.streetNWAdm.proxAcc.nodesGrid_m = " + str(city.streetNWAdm.getProxAcc_m()) + "\n")
    f.write("\tcity.streetNWAdm.proxAcc.extraNodes_d = " + str(city.streetNWAdm.getProxAcc().getExtraNodes_d()) + "\n")
    
    f.write("\treturn city")
    
def loadPrecomputedMap(mapName):
    elems = mapName.split('/')
    path = '/'.join(elems[:-1])
    name = elems[-1]
    import sys
    sys.path.append(path)
    map = __import__(name)

    return map.getCity()
    
if __name__ == '__main__':
    import os
    from city.City import *

    parent = os.path.join(os.path.dirname(__file__), '..')
    pathFirence = parent + '/osmFiles/girona/gironaCarme.osm'
    pathBarcelona = parent + '/../BigOsmFiles/Barcelona/BarcelonaMercats.osm'

    
    toFile(City(pathBarcelona), parent + '/../BigOsmFiles/Barcelona/BarcelonaMercats')
