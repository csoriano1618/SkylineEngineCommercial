'''
Created on 19/09/2013

@author: oriol
'''
import sys,os.path
if not os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) in sys.path:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
      
from city import City
from copy import *
import random
 
class BoundCity:
    
    def __init__(self, city):
        """
        This class __init__ method will create a new city with a new way drawing the streets bounding box.
        """
        self.boundCity = deepcopy(city)
        
        streetsBB = city.getStreetsBoundingBox()
        minLatN_l = []
        minLonN_l = []
        maxLatN_l = []
        maxLonN_l = []
        for nK,nV in self.boundCity.getNodes_d().iteritems():
            if self.boundCity.getNodeLat(nK)==streetsBB[0]:
                minLatN_l.append(nK)
            elif self.boundCity.getNodeLat(nK)==streetsBB[2]:
                maxLatN_l.append(nK)
            else:
                pass
            if self.boundCity.getNodeLon(nK)==streetsBB[1]:
                minLonN_l.append(nK)
            elif self.boundCity.getNodeLon(nK)==streetsBB[3]:
                maxLonN_l.append(nK)
            else:
                pass
        # Create the bounding box way
        boundingWayNodes = []
        # down-left corner node
        minLatN = minLatN_l[0]
        for n in minLatN_l[1:]:
            if self.boundCity.getNodeLon(n)<self.boundCity.getNodeLon(minLatN):
                minLatN = n
        minLonN = minLonN_l[0]
        for n in minLonN_l[1:]:
            if self.boundCity.getNodeLat(n)<self.boundCity.getNodeLat(minLonN):
                minLonN = n
        if self.boundCity.getNodeLon(minLatN)!=streetsBB[1] and self.boundCity.getNodeLat(minLonN)!=streetsBB[0]:
            mmId = int(str(random.randint(0,99999999)))
            while mmId in self.boundCity.getNodes_d():
                mmId = int(str(random.randint(0,99999999)))
            self.boundCity.addNode(mmId, streetsBB[0], streetsBB[1], nHeaderInf_d={'version':1}, nTags_d={})
        else:
            if self.boundCity.getNodeLon(minLatN)==streetsBB[1]:
                mmId = minLatN
            else:
                mmId = minLonN
        # down-right corner node
        minLatN = minLatN_l[0]
        for n in minLatN_l[1:]:
            if self.boundCity.getNodeLon(n)>self.boundCity.getNodeLon(minLatN):
                minLatN = n
        maxLonN = maxLonN_l[0]
        for n in maxLonN_l[1:]:
            if self.boundCity.getNodeLat(n)<self.boundCity.getNodeLat(maxLonN):
                maxLonN = n
        if self.boundCity.getNodeLat(maxLonN)!=streetsBB[0] and self.boundCity.getNodeLon(minLatN)!=streetsBB[3]:
            mMId = int(str(random.randint(0,99999999)))
            while mMId in self.boundCity.getNodes_d():
                mMId = int(str(random.randint(0,99999999)))
            self.boundCity.addNode(mMId, streetsBB[0], streetsBB[3], nHeaderInf_d={'version':1}, nTags_d={})
        else:
            if self.boundCity.getNodeLat(maxLonN)==streetsBB[0]:
                mMId = maxLonN
            else:
                mMId = minLatN
        # up-right corner node
        maxLatN = maxLatN_l[0]
        for n in maxLatN_l[1:]:
            if self.boundCity.getNodeLon(n)>self.boundCity.getNodeLon(maxLatN):
                maxLatN = n
        maxLonN = maxLonN_l[0]
        for n in maxLonN_l[1:]:
            if self.boundCity.getNodeLat(n)>self.boundCity.getNodeLat(maxLonN):
                maxLonN = n
        if self.boundCity.getNodeLon(maxLatN)!=streetsBB[3] and self.boundCity.getNodeLat(maxLonN)!=streetsBB[2]:
            MMId = int(str(random.randint(0,99999999)))
            while MMId in self.boundCity.getNodes_d():
                MMId = int(str(random.randint(0,99999999)))
            self.boundCity.addNode(MMId, streetsBB[2], streetsBB[3], nHeaderInf_d={'version':1}, nTags_d={})
        else:
            if self.boundCity.getNodeLon(maxLatN)==streetsBB[3]:
                MMId = maxLatN
            else:
                MMId = maxLonN
        # up-left corner node
        maxLatN = maxLatN_l[0]
        for n in maxLatN_l[1:]:
            if self.boundCity.getNodeLon(n)<self.boundCity.getNodeLon(maxLatN):
                maxLatN = n
        minLonN = minLonN_l[0]
        for n in minLonN_l[1:]:
            if self.boundCity.getNodeLat(n)>self.boundCity.getNodeLat(minLonN):
                minLonN = n
        if self.boundCity.getNodeLat(minLonN)!=streetsBB[2] and self.boundCity.getNodeLon(maxLatN)!=streetsBB[1]:
            MmId = int(str(random.randint(0,99999999)))
            while MmId in self.boundCity.getNodes_d():
                MmId = int(str(random.randint(0,99999999)))
            self.boundCity.addNode(MmId, streetsBB[2], streetsBB[1], nHeaderInf_d={'version':1}, nTags_d={})
        else:
            if self.boundCity.getNodeLat(minLonN)==streetsBB[2]:
                MmId = minLonN
            else:
                MmId = maxLatN
        # add bounding box way nodes:
        boundingWayNodes.append(mmId)
        if minLatN!=mmId and minLatN!=mMId:
            boundingWayNodes.append(minLatN)
        boundingWayNodes.append(mMId)
        if maxLonN!=mMId and maxLonN!=MMId:
            boundingWayNodes.append(maxLonN)
        boundingWayNodes.append(MMId)
        if maxLatN!=MMId and maxLatN!=MmId:
            boundingWayNodes.append(maxLatN)
        boundingWayNodes.append(MmId)
        if minLonN!=MmId and minLonN!=mmId:
            boundingWayNodes.append(minLonN)
        boundingWayNodes.append(mmId)
        # add bounding box way to city if is not existing yet:
        found = False
        ways_l = self.boundCity.getWays_d().keys()
        i = 0
        while (not found) and (i < len(ways_l)):
            wNodes = self.boundCity.getWayNodes(ways_l[i])
            if (wNodes.count(mmId)==2) and (mMId in wNodes) and (MmId in wNodes) and (MMId in wNodes):
                found = True
            else:
                i += 1
        if not found:
            self.boundCity.addWay( None, wHeaderInf_d={'version': 1}, wNodes_l=boundingWayNodes, wTags_d = {'highway':'primary','boundingBoxWay':'True'})
                       
        
    def getBoundCity(self):
        """
        This method returns the city with a bounding box of the streets as a new way
        """
        return self.boundCity
    
    
    