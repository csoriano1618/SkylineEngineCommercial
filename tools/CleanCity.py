'''
Created on 01/10/2013

@author: oriol
'''
import sys,os.path
if not os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) in sys.path:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from city import City
from copy import *
import random
import operator

class CleanCity:
    
    def __init__(self, city):
        """
        This class will clean the city. What did 'clean' mean?
        1. It will found intersections between segments and add there a new node
           (adding this node to the intersecting ways in the corresponding place)
        ========== TO DO!!! ==========
        2. It will remove repeated segments.
           (If this cause different fragments of the way, it create new ways, one for each fragment)
        """
        
        self.cleanedCity = deepcopy(city)
        self.addedNodes_d = {}
        
        self.addIntersections()
        #========== TO DO!!! ==========
        #self.removeRepeatedSegments()
        
    def addIntersections(self):
        """
        This method will found all the ways intersections without an explicit node in it.
        If founds any intersection, it will add in the corresponding point a node an will add it at each way intersecting
        """
        nInt = 0
        streets = self.cleanedCity.getStreetWays()
        # for each street:
        for w in streets:
            # get segments and all nodes (extra nodes included) in each segment
            wNodes = self.cleanedCity.getWayNodes(w)
            wExtraNodes = self.cleanedCity.getWayExtraNodes(w)
            iSegment = 0
            wSegLen = len(wExtraNodes)
            while iSegment < wSegLen:
                iSegInts_l = []
                segNodes_l = [wNodes[iSegment]]
                segNodes_l.extend(wExtraNodes[iSegment])
                segNodes_l.append(wNodes[iSegment+1])
                # for each segment node (extra included) search near nodes set
                nearSegNs_s = set()
                for segN in segNodes_l:
                    nearSegNs_l = self.cleanedCity.getPointNodesCloserThan(self.cleanedCity.getNodeLat(segN), self.cleanedCity.getNodeLon(segN), extraNodes=True)
                    nearSegNs_s |= set(nearSegNs_l)
                # for each near node, find the segment candidate to make intersection it belongs to
                nearSegs_l = []
                nearSegsWay_l = []
                for nearN in nearSegNs_s:
                    if nearN<0:
                        # it's an extra node. Get segment it belongs to and add it if is not in near segments list
                        (nearSW, nearS) = self.cleanedCity.getExtraNodeOSMPrimitives(nearN)
                        if (nearS not in nearSegs_l) and ((nearS[1],nearS[0]) not in nearSegs_l):
                            nearSegs_l.append(nearS)
                            nearSegsWay_l.append(nearSW)
                    else:
                        # it's a real node. Get neighbor nodes and for each one add the segment they make and add it if is not in near segments list
                        nearNNeigs_l = self.cleanedCity.getNodeNeigNodes(nearN)
                        for neig in nearNNeigs_l:
                            nearS = (nearN,neig[0])
                            nearSW = neig[1]
                            if (nearS not in nearSegs_l) and ((nearS[1],nearS[0]) not in nearSegs_l):
                                nearSegs_l.append(nearS)
                                nearSegsWay_l.append(nearSW)
                # for each near segment, check if it intersects with the evaluated city segment
                pSeg1 = ( self.cleanedCity.getNodeLat(segNodes_l[0]), self.cleanedCity.getNodeLon(segNodes_l[0]) )
                pSeg2 = ( self.cleanedCity.getNodeLat(segNodes_l[-1]), self.cleanedCity.getNodeLon(segNodes_l[-1]) )
                intersections_l = []
                for nearS, nearSW in zip(nearSegs_l, nearSegsWay_l):
                    if (nearS[0] is not segNodes_l[0]) and (nearS[0] is not segNodes_l[-1]) and (nearS[1] is not segNodes_l[0]) and (nearS[1] is not segNodes_l[-1]):
                        pNeig1 = ( self.cleanedCity.getNodeLat(nearS[0]), self.cleanedCity.getNodeLon(nearS[0]) )
                        pNeig2 = ( self.cleanedCity.getNodeLat(nearS[1]), self.cleanedCity.getNodeLon(nearS[1]) )
                        if self.intersection(pSeg1[0], pSeg1[1], pSeg2[0], pSeg2[1], pNeig1[0], pNeig1[1], pNeig2[0], pNeig2[1]):
                            # Two segments intersects
                            # Create a new node with the intersection point lat and lon and add this node to the ways that intersect
                            nInt += 1
                            pInt = self.intersectionPoint(pSeg1[0], pSeg1[1], pSeg2[0], pSeg2[1], pNeig1[0], pNeig1[1], pNeig2[0], pNeig2[1])
                            #search a non existing id
                            nId = int(str(random.randint(0,99999999)))
                            while nId in self.cleanedCity.getNodes_d():
                                nId = int(str(random.randint(0,99999999)))
                            self.cleanedCity.addNode(nId, pInt[0], pInt[1])
                            # Many intersections on the same segment could cause a loop caos. We will store the intersections to add on a list so lets
                            # get distance from first iSegment node to new node (to get intersections on segment ordered) and add them properly late.
                            intDist = self.cleanedCity.nodesDist(wNodes[iSegment],nId)
                            iSegInts_l.append((nId,intDist))
                            # Add intersection node to the intersecting segment way position
                            nearSWNodes_l = self.cleanedCity.getWayNodes(nearSW)
                            pos1 = [i for i,x in enumerate(nearSWNodes_l) if x==nearS[0]][0]
                            pos2 = [i for i,x in enumerate(nearSWNodes_l) if x==nearS[1]][0]
                            # Careful if the street is a closed way with same node in the first and the last node
                            if (pos1==0) and (nearSWNodes_l[0]==nearSWNodes_l[-1]):
                                if pos2==len(nearSWNodes_l)-2:
                                    pos1=len(nearSWNodes_l)-1   
                                else:
                                    # pos2==1
                                    pass     
                            if (pos2==0) and (nearSWNodes_l[0]==nearSWNodes_l[-1]):
                                if pos1==len(nearSWNodes_l)-2:
                                    pos2=len(nearSWNodes_l)-1   
                                else:
                                    # pos1==1
                                    pass
                            if pos1<pos2:
                                # add node to intersecting way segment
                                self.cleanedCity.addWayNode(nearSW, nId, pos1+1)
                                self.addedNodes_d[nId] = ((w,nearSW))
                            else:
                                # add node to intersecting way segment
                                self.cleanedCity.addWayNode(nearSW, nId, pos2+1)
                                self.addedNodes_d[nId] = ((w,nearSW))
                if len(iSegInts_l)>0:
                    # Add all intersections of the segment in distance to first iSegment node order
                    iSegInts_l.sort(key=operator.itemgetter(1))
                    for intersection in iSegInts_l:
                        self.cleanedCity.addWayNode(w,intersection[0],iSegment+1)
                        wSegLen += 1 
                        iSegment += 1
                    # update way node lists because new segment appeared adding intersection nodes and changing all extra nodes.
                    wNodes = self.cleanedCity.getWayNodes(w)
                    wExtraNodes = self.cleanedCity.getWayExtraNodes(w)       
                iSegment += 1
                
        print 'Num of intersections found: ', nInt
                            
                    
    def getCleanedCity(self):
        """
        This method returns the city with new intersection nodes and repeated segments removed
        """
        return self.cleanedCity
    
    def getAddedNodes(self):
        """
        This method returns the new intersection nodes added to the cleaned city
        """
        return self.addedNodes_d
        
        
    """ INTERSECTIONS METHODS -----------------------------------------------------------------------"""
    def side(self,x1,y1,x2,y2,x3,y3,x4,y4):
        """
        Returns a value depending on the relative positions between them
        """         
        dx = x2-x1
        dy = y2-y1
        dx1 = x3-x1
        dy1 = y3-y1
        dx2 = x4-x2
        dy2 = y4-y2
        side = (dx*dy1-dy*dx1)*(dx*dy2-dy*dx2)
        
        return side
    
    def intersection(self,x1,y1,x2,y2,x3,y3,x4,y4):
        """
        Returns True if segments (x1,y1)--(x2,y2) and (x3,y3)--(x4,y4) intersect
        """      
        int1 = self.side(x1,y1,x2,y2,x3,y3,x4,y4)
        int2 = self.side(x3,y3,x4,y4,x1,y1,x2,y2)
                
        return (int1<0) & (int2<0)
    
    def intersectionPoint(self, x1, y1, x2, y2, x3, y3, x4, y4):
        """
        Returns the intersection point between segments (x1,y1)--(x2,y2) and (x3,y3)--(x4,y4)
        """               
        pointx = ( (x1*y2-y1*x2)*(x3-x4) - (x1-x2)*(x3*y4-y3*x4) ) / ( (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4) )
        pointy = ( (x1*y2-y1*x2)*(y3-y4) - (y1-y2)*(x3*y4-y3*x4) ) / ( (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4) )
        
        return pointx, pointy
    
    
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
    import parsers.CityToFile
    
    path = parent + '/osmFiles/firenze/firenze_center_impSelect.osm'         
    #path = parent + '/osmFiles/firenze/firenze_center.osm'
#    city = City.City(path)          
    
    city = City.City(centerPos=(3,3),proxCellSize=1)
    city.addNode(1,4.,6.)
    city.addNode(2,1.,4.)
    city.addNode(3,5.,0.)
    city.addWay(3, wNodes_l=[1,2,3], wTags_d = {'highway':'primary'})
    city.addNode(4,6.,2.)
    city.addWay(2, wNodes_l=[4,2], wTags_d={'highway':'primary'})
    city.addNode(5,1.,1.)
    city.addNode(6,3.,6.)
    city.addWay(1, wNodes_l=[5,6], wTags_d={'highway':'primary'})
    
    cC = CleanCity(city)
    cleanCity = cC.getCleanedCity()   
    print 'Added intersection nodes: ', cC.getAddedNodes()
    
    if not os.path.isdir(parent + '/../skylineengineTestOutputs'):
        os.mkdir(parent + '/../skylineengineTestOutputs')
    if not os.path.isdir(parent + '/../skylineengineTestOutputs/ToolsTests'):
        os.mkdir(parent + '/../skylineengineTestOutputs/ToolsTests')
    #cleanCity.toOSM(parent + '/../skylineengineTestOutputs/ToolsTests/firenze_center_impSelect_CleanCity_TEST')
    #cleanCity.toOSM(parent + '/../skylineengineTestOutputs/ToolsTests/firenze_center_CleanCity_TEST')
    cleanCity.toOSM(parent + '/../skylineengineTestOutputs/ToolsTests/test_CleanCity_TEST')
    
    print
    print 'DONE'
      
    
    
