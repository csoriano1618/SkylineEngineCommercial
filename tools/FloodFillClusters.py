'''
Created on 15/02/2012

@author: oriol
'''
import sys,os.path
if not os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) in sys.path:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from city import City

class FloodFillClusters:
    
    def __init__(self, city):
        """
        This class __init__ method will return a list with all disconnected clusters of a city.
        Each cluster is a list of the street ways connected themselves.
        !!! ATENTION !!!
        It considers the city streets network as a UNDIRECTED GRAPH!!!
        """
        self.clusters = []
        # We get all city street network nodes:
        allNodes = city.getStreetNodes()
        # When a node is added to a cluster, we eliminate it from the allNodes list.
        # So we go adding nodes to a cluster while allNodes list is not empty.
        while len(allNodes)!=0:
            # Initialize a new cluster:
            openSet = []
            closeSet = []
            actCluster = []
            openSet.append(allNodes[0])
            # The actual cluster grows adding neighbors of the nodes belonging to it.
            # When the actual node neighbors are added to the openSet, the actual node is eliminated from openSet and added to closeSet
            # So we go adding nodes to the actCluster while openSet is not empty.
            while len(openSet)!=0:
                # First openSet node, get neighbors.
                neig = city.getNodeNeigNodes(openSet[0])
                # Add first openSet node neighbors to the openSet.
                if neig!=None:
                    for n in neig:
                        # Each n is a tuple (neigNode, wayToGetNeigNode).
                        # Add neighbor node to openSet if is not already in it:
                        if (n[0] not in openSet) and (n[0] not in closeSet):
                            openSet.append(n[0])
                        # Add way to get to the neighbor node to the actCluster if is not already in it:
                        if n[1] not in actCluster:
                            actCluster.append(n[1])
                # When actual node has been added to the cluster:
                # we add it to the closeSet
                closeSet.append(openSet[0])
                # and we eliminate it form allNodes and openSet lists
                allNodes.remove(openSet[0])
                del openSet[0]
            # A cluster is completed, no more neighbors
            self.clusters.append(actCluster)
        # No nodes on allNodes_l, so all clusters found
        
        
    def getClusters(self):
        """
        This method returns the clusters found
        """
        return self.clusters
    
          
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
    c.addNode(1, 43.7717, 11.2615)
    c.addNode(2, 43.7727, 11.2615)
    c.addNode(3, 43.7737, 11.2615)
    c.addNode(4, 43.7747, 11.2615)
    c.addNode(5, 43.7737, 11.2625)
    c.addWay(1, wNodes_l=[1,2,3,4])
    c.addWay(2, wNodes_l=[5,3])
    ffClust = FloodFillClusters(c)
    clusters = ffClust.getClusters()
    for cl in clusters:
        print cl
    
    print
    print 'DONE'
        