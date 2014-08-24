'''
Created on 06/03/2013

@author: oriol
'''
import sys,os.path
if not os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) in sys.path:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from city import City
from tools import BoundCity as BC
from copy import *
import random
import math

class ClosedMinimalCircuits:
    
    def __init__(self, city, boundingCircuit=False):
        """
        This class __init__ method will crate a new city where:
        - Nodes are the same as the street network of the input city plus the four nodes describing the effective bounding box
        - Ways are each one a closed minimal circuit, a block
        If boundingCircuit=False it won't add the circuit drawing the full city bounding box, otherwise will add it as one more circuit.
        """
        # Create the new blocks city, initially empty.
        streetsBB = city.getStreetsBoundingBox()
        c = ( streetsBB[0]+((streetsBB[2]-streetsBB[0])/2) , streetsBB[1]+((streetsBB[3]-streetsBB[1])/2) )
        self.blocksCity = City.City( centerPos=c )
        
        # Create a copy of the input city adding the bounding box as ways
        bc = BC.BoundCity(city) 
        boundedCity = bc.getBoundCity()
        
        # Create a dictionary of intersection nodes circuits already found.
        # For each intersection node Id (dictionary key) it stores a list of circuit ways passing through it already found
        self.intNodeCircuitsFound_d = {}
        intNodes = boundedCity.getIntersectionNodes()
        for intN in intNodes:
            # get intersection nodes neighbors (just nodes)
            intNeigs = boundedCity.getNodeNeigNodes(intN)            
            intNeigNs = [ x[0] for x in intNeigs ]
            # remove duplicates
            intNeigSet = set(intNeigNs)
            if len(intNeigSet)>2:
                self.intNodeCircuitsFound_d[intN]=[]
                
        # For each intersection node:
        for intN in self.intNodeCircuitsFound_d.keys():
            # Get intersection node circuits already found
            intCircuitsFound = self.getIntCircuitsFound(intN,boundedCity)
            # Get new circuits from intersection node, not the found before
            intNCircuits = self.getIntCircuits(intN,boundedCity,intCircuitsFound)
            # Add circuits as ways in blocksCity and also to the intNodeCircuitsFound_d
            self.addCircuits(intNCircuits,boundedCity)       
        
        if not boundingCircuit:
        # We have to delete the circuit drawing the full city bounding box.
            # Get four bounding box corner nodes:
            cornerBLn = self.blocksCity.getPointNearestNodeCloserThan(streetsBB[0],streetsBB[1])
            cornerBRn = self.blocksCity.getPointNearestNodeCloserThan(streetsBB[0],streetsBB[3])
            cornerTLn = self.blocksCity.getPointNearestNodeCloserThan(streetsBB[2],streetsBB[1])
            cornerTRn = self.blocksCity.getPointNearestNodeCloserThan(streetsBB[2],streetsBB[3])            
            # Remove that way (circuit) that passes through all bounding box corners.
            bbFound = False
            i = 0
            ways_l = self.blocksCity.getWays_d().keys()
            while (not bbFound) and (i<len(ways_l)):
                if (cornerBLn in self.blocksCity.getWayNodes(ways_l[i])) and (cornerBRn in self.blocksCity.getWayNodes(ways_l[i])) and (cornerTLn in self.blocksCity.getWayNodes(ways_l[i])) and (cornerTRn in self.blocksCity.getWayNodes(ways_l[i])):
                    bbFound = True
                    self.blocksCity.removeWay(ways_l[i])
                else:
                    pass
                i += 1
   
    def getIntCircuitsFound(self,intN,originalCity):
        """
        This method return a list of tuples, where each tuple is the neighbor node and the way of the circuits passing through intN node already found.
        """
        circuitsFound=[]
        if len(self.intNodeCircuitsFound_d[intN])>0:
            for (neigNode,neigWay) in originalCity.getNodeNeigNodes(intN):
                for intNFoundC in self.intNodeCircuitsFound_d[intN]:
                    circuitNodes = self.blocksCity.getWayNodes(intNFoundC)
                    intNPos = circuitNodes.index(intN)
                    if circuitNodes[intNPos+1]==neigNode:
                        circuitsFound.append((neigNode,neigWay))
            return circuitsFound
        else:
            return []
                    
        
    def getIntCircuits(self,intN,city,exceptCircuit_l=[]):
        """
        This method returns the circuits from the intN intersection node (clockwise).
        If exceptCircuit_l is different to None, it returns just the circuits not in exceptCircuit_l list.
        """
        circuits = []
        for (neigN, neigW) in city.getNodeNeigNodes(intN):
            if (neigN, neigW) not in exceptCircuit_l:
                path = [intN,neigN]
                lastN = intN
                actN = neigN
                while actN!=intN:
                    actNeigs_l = city.getNodeNeigNodes(actN)
                    minAngle = 500.
                    for (actNeig,actNeigW) in actNeigs_l:
                        if actNeig != lastN:
                            xLast = city.getNodeLon(lastN)-city.getNodeLon(actN)
                            yLast = city.getNodeLat(lastN)-city.getNodeLat(actN)
                            xNext = city.getNodeLon(actNeig)-city.getNodeLon(actN)
                            yNext = city.getNodeLat(actNeig)-city.getNodeLat(actN)
                            lastAngle = math.atan2(yLast, xLast)*180./math.pi
                            nextAngle = math.atan2(yNext, xNext)*180./math.pi
                            if lastAngle>=0 and nextAngle>=0:
                                if nextAngle>lastAngle:
                                    angle = nextAngle-lastAngle
                                else:
                                    angle = 360 + nextAngle-lastAngle
                            elif lastAngle<0 and nextAngle<0:
                                if -lastAngle>-nextAngle:
                                    angle = (-lastAngle)-(-nextAngle)
                                else:
                                    angle = 360 + (-lastAngle)-(-nextAngle)
                            else:
                                if lastAngle>=0:
                                    angle = (180-lastAngle)+(180-(-nextAngle))
                                else:
                                    angle = -lastAngle+nextAngle
                            if angle < minAngle:
                                minNeig = actNeig
                                minAngle = angle
                    path.append(minNeig)
                    lastN = actN
                    actN = minNeig
                circuits.append(path)
        return circuits                
         
    def addCircuits(self,circuits_l,city):
        """
        this method add circuits_l circuits to the blocksCity as ways.
        It also add those circuits to intNodeCircuitsFound_d dictionary if they pass through them
        """
        for c in circuits_l:
            # did this circuit way already exist? (a segment could be of just two circuits so:)
            exist = False
            if c[0] in self.blocksCity.getNodes_d() and c[1] in self.blocksCity.getNodes_d():
                if len(self.blocksCity.getNodesDirectConnectingWays(c[0],c[1]))==2:
                    exist = True
                else:
                    pass
            else:
                pass
            if not exist:
                # search a non existing id
                wId = int(str(random.randint(0,99999999)))
                while wId in self.blocksCity.getWays_d():
                    wId = int(str(random.randint(0,99999999)))
                # add way nodes to blocksCity:
                for nK in c:
                    if nK not in self.blocksCity.getNodes_d():
                        nLat = city.getNodeLat(nK)
                        nLon = city.getNodeLon(nK)
                        nHInf = city.getNodeHeaderInf_d(nK)
                        nTags = city.getNodeTags_d(nK)
                        self.blocksCity.addNode(nK,nLat,nLon,nHInf,nTags)
                    # add circuit to intNodeCircuitsFound_d dictionary:
                    if (nK in self.intNodeCircuitsFound_d.keys()) and (wId not in self.intNodeCircuitsFound_d[nK]):
                        self.intNodeCircuitsFound_d[nK].append(wId)
                # add way to blocksCity:
                self.blocksCity.addWay(wId, {'version':1,'visible':'true','user':'skylineEngine.City'},c,{'highway':'unclassified','place':'city block'})
            else:
                pass
        
    def getBlocksCity(self):
        """
        This method returns the blocks city
        """
        return self.blocksCity
    
          
#=================================================================
#=================================================================
#=================================================================

if __name__=="__main__":
    import sys,os.path
    parent = os.path.join(os.path.dirname(__file__), '..')
    
    print '-----------------'
    print '| __main__ TEST |'
    print '-----------------'
    
    from city import City
    import CleanFringePaths
    
    path = parent + '/osmFiles/firenze/firenze_00.osm'
    c = City.City(path)
    
    bc = BC.BoundCity(c)
    boundedCity = bc.getBoundCity()
    if not os.path.isdir(parent + '/../skylineengineTestOutputs'):
        os.mkdir(parent + '/../skylineengineTestOutputs')
    if not os.path.isdir(parent + '/../skylineengineTestOutputs/ToolsTests'):
        os.mkdir(parent + '/../skylineengineTestOutputs/ToolsTests')
    boundedCity.toOSM(parent + '/../skylineengineTestOutputs/ToolsTests/firenze_00_ClosedMinimalCircuits_TEST_BOUNDED')
    
    cfp = CleanFringePaths.CleanFringePaths(boundedCity)
    cleanCity = cfp.getCleanCity()
    if not os.path.isdir(parent + '/../skylineengineTestOutputs'):
        os.mkdir(parent + '/../skylineengineTestOutputs')
    if not os.path.isdir(parent + '/../skylineengineTestOutputs/ToolsTests'):
        os.mkdir(parent + '/../skylineengineTestOutputs/ToolsTests')
    cleanCity.toOSM(parent + '/../skylineengineTestOutputs/ToolsTests/firenze_00_ClosedMinimalCircuits_TEST_Clean_PREBOUND')
    
    cmc = ClosedMinimalCircuits(cleanCity)
    blocksCity = cmc.getBlocksCity()
    if not os.path.isdir(parent + '/../skylineengineTestOutputs'):
        os.mkdir(parent + '/../skylineengineTestOutputs')
    if not os.path.isdir(parent + '/../skylineengineTestOutputs/ToolsTests'):
        os.mkdir(parent + '/../skylineengineTestOutputs/ToolsTests')
    blocksCity.toOSM(parent + '/../skylineengineTestOutputs/ToolsTests/firenze_00_ClosedMinimalCircuits_TEST_Blocks_PREBOUND')
    
    
    
    print
    print 'DONE'
      