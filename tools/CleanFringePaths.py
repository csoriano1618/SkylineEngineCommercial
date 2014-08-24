'''
Created on 06/03/2013

@author: oriol
'''
import sys,os.path
if not os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) in sys.path:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from city import City
from copy import *
import random

class CleanFringePaths:
    
    def __init__(self, city):
        """
        This class __init__ method will create a new city without any way fringe path.
        A way fringe path is a set of way segments going from an intersection to a way ending node with just one neighbor node,
        without crossing any other intersection.
        """
        self.cleanCity = deepcopy(city)
        
        removeWays_l = []
        # until there is no change
        change = True
        while change:
            change = False
            # for each way:
            for wK in self.cleanCity.getWays_d():
                wInitialNodes = self.cleanCity.getWayNodes(wK)
                # get ending nodes
                firstN = wInitialNodes[0]
                lastN = wInitialNodes[-1]
                # if an ending node has just one neighbor, we delete it and we do it again if neighbor node is also 
                # from fringe path, until arrives to a non fringe path node, a node with more than one neighbor.
                i=0
                # way node neighbors without repeated elements.
                firstNNeigs_l = self.cleanCity.getNodeNeigNodes(firstN)
                # get not repeated neighbor nodes (maybe two ways duplicate the same segment)
                firstNNeigs_lNoRep = list(set( [ x[0] for x in firstNNeigs_l ] ))
                # go deleting node by node if it has just one neighbor 
                while (len(firstNNeigs_lNoRep) == 1) and (len(self.cleanCity.getWayNodes(wK)) > 1):
                    change = True
                    for neig in firstNNeigs_l:
                        self.cleanCity.removeWayNode(neig[1],firstN)
                    if len(self.cleanCity.getNodeWays(firstN))<1:
                        self.cleanCity.removeNode(firstN)
                    i=i+1
                    firstN = wInitialNodes[i]
                    firstNNeigs_l = self.cleanCity.getNodeNeigNodes(firstN)
                    firstNNeigs_lNoRep = list(set( [ x[0] for x in firstNNeigs_l ] ))
                if len(self.cleanCity.getWayNodes(wK)) > 1:
                    i=-1
                    # way node neighbors without repeated elements.
                    lastNNeigs_l = self.cleanCity.getNodeNeigNodes(lastN)
                    lastNNeigs_lNoRep = list(set( [ x[0] for x in lastNNeigs_l ] ))
                    while (len(lastNNeigs_lNoRep) == 1) and (len(self.cleanCity.getWayNodes(wK)) > 1):
                        change = True
                        for neig in lastNNeigs_l:
                            self.cleanCity.removeWayNode(neig[1],lastN)
                        if len(self.cleanCity.getNodeWays(lastN))<1:
                            self.cleanCity.removeNode(lastN)
                        i=i-1
                        lastN = wInitialNodes[i]
                        lastNNeigs_l = self.cleanCity.getNodeNeigNodes(lastN)
                        lastNNeigs_lNoRep = list(set( [ x[0] for x in lastNNeigs_l ] ))
                if (len(self.cleanCity.getWayNodes(wK)) < 2) and (wK not in removeWays_l):
                    removeWays_l.append(wK)
                    change = True
                
        for i in range(len(removeWays_l)):
            if removeWays_l[i] in self.cleanCity.getWays_d().keys():
                self.cleanCity.removeWay(removeWays_l[i],removeNodes=True)   
            
        
    def getCleanCity(self):
        """
        This method returns the city without way fringe paths
        """
        return self.cleanCity
    
          
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
    
    path = parent + '/osmFiles/firenze/firenze_00.osm'
    c = City.City(path)
    cfp = CleanFringePaths(c)
    cleanCity = cfp.getCleanCity()
    
    if not os.path.isdir(parent + '/../skylineengineTestOutputs'):
        os.mkdir(parent + '/../skylineengineTestOutputs')
    if not os.path.isdir(parent + '/../skylineengineTestOutputs/ToolsTests'):
        os.mkdir(parent + '/../skylineengineTestOutputs/ToolsTests')
    cleanCity.toOSM(parent + '/../skylineengineTestOutputs/ToolsTests/firenze_00_CleanFringePath_TEST')
    
    print
    print 'DONE'
      