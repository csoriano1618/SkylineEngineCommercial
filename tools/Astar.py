# -*- coding: utf-8 -*-
import sys,os.path
if not os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) in sys.path:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy
import math
from city import City

# Required constants for Astar
TIMES_PATH_HAS_BEEN_PROCESSED = 0
PATH_NODES = 1
SHORTEST_PATH_COST = 2

class Astar:
    
    def __init__(self, city, startsGoals_l,  directedGraph=False, distFunc=None):
        """
        This class will process an A* algorithm over the city streets network.
        It gets as input:
        - the city
        - a list of tuples (startNode, goalNode)
        - could get also a distance function defined out of this class. This function will always have node1 and node2 as first two parameters.
          if there is no distance function as parameter, it will apply the euclidean distance from a node to the other.
        It returns a list with a tuple for each (startNode, goalNode) pair. Each of these tuples have three elements:
        - times this path it has been processed (if a pair of startN and goalN was repeated in the input list)
        - the list of nodes defining the shortest path to go from a start to a goal
        - the cost of this the shortest path
        """
        self.city = city
        self.aggregateResults_d = {}
        # After all startsGoals_l are processed:
        # Key = nodeVisited: Value = [(OneNeigNode, ProbabilityToOneNeigNode)
        self.probabilities = {}
        # !!! Attributes of the current startGoal tuple: !!!
        self.result = []
        self.resultCost = 0.0
        self.start = None
        self.goal = None
        if distFunc==None:
            distFunc = self.euclideanDist
        
        nodeCount_d = {}
        for i, [start,  goal] in enumerate(startsGoals_l):
            # COMPUTE current StartGoal tuple PATH ( No need to repeat an already computed path :) )
            if (start, goal) in self.aggregateResults_d:
                # copy already computed path result
                self.result = self.aggregateResults_d[start, goal][1]
                self.resultCost = self.aggregateResults_d[start, goal][2]
            else:
                # process new path result
                self.process(start, goal, directedGraph, distFunc)
    
            # UPDATE aggregateResults_d with current StartGoal tuple:
            if (start, goal) in self.aggregateResults_d:
                self.aggregateResults_d[start, goal] = [self.aggregateResults_d[start, goal][0] + 1,  self.result, self.resultCost] 
            else:
                self.aggregateResults_d[start, goal] = [1, self.result, self.resultCost] 
                
            # COMPUTE NODECOUNT_D for final probabilities dictionary
            for i, node in enumerate(self.result):
                if (i + 1) < len(self.result):
                    next = self.result[i +1]
                    if (node) in nodeCount_d:
                        if next in nodeCount_d[node]:
                            nodeCount_d[node][next] = nodeCount_d[node][next] + 1.0
                        else:
                            nodeCount_d[node][next] = 1.0
                    else:
                        nodeCount_d[node] = {next : 1.0}
    
        # Normalize for probabilities dictionary:
        for startNode_k, startNode_d in nodeCount_d.iteritems():
            sumValues = sum([i for i in startNode_d.values()])
#            max = float(startNode_d[self.dictMax(startNode_d)])
            for endNode,  endValue in startNode_d.iteritems():
                startNode_d[endNode] = endValue / sumValues
        self.probabilities = nodeCount_d
        
    
    def getProbabilities(self):
        return self.probabilities
    
    
    def getResults_d(self):
        return self.aggregateResults_d
    

    def process(self, start, goal,  directedGraph, distFunc):
        """
        Process the path the minimal path to go from start node to goal node of the city.
        """
        self.result = []
        self.start = int(start)
        self.goal = int(goal)
        #the set of nodes already evaluated
        closedSet = []
        #the set of tentative nodes to be evaluated
        openSet = []
        openSet.append(int(self.start))
        #the map of navigated nodes
        cameFrom = {}
        #distance from start along optimal path
        gScore = {}
        gScore[self.start] = 0.0
        #euclidean distance between current node and goal (estimated distance)
        hScore = {}
        hScore[self.start] = distFunc(self.start, self.goal)
        #estimated total cost from start to goal through 'current' node
        fScore = {}        
        fScore[self.start] = gScore[self.start] + hScore[self.start]
        
        while len(openSet) > 0:
            # get the node in openset having the lowest f_score[] value
            x = self.dictMin(fScore)
            # we arrived to the goal?
            if x == self.goal:
                self.reconstructPath(cameFrom, cameFrom[self.goal])
                break
            # take node out of openSet and add it to closedSet
            openSet.remove(x)
            closedSet.append(x)
            # get x neighbor nodes
            if directedGraph:
                neighbors = self.city.getNodeFollowingNodes(x)
            else:
                neighbors = self.city.getNodeNeigNodes(x)
            for y in neighbors:
                yNeig = y[0]
                yWay = y[1]
                # if neighbor yNeig is in closedSet, next iteration of the loop
                if yNeig in closedSet:
                    continue
                # get neighbor yNeig tentativeGScore, is this score better than last stored gScore?
                tentativeGScore = gScore[x] + distFunc(x, yNeig)
                if yNeig not in openSet:
                    openSet.append(yNeig)
                    tentativeIsBetter = True
                elif tentativeGScore < gScore[yNeig]:
                    tentativeIsBetter = True
                else:
                    tentativeIsBetter = False
                # if neighbor yNeig has better gScore now we update g,h,fScores of yNeig and add yNeig to cameFrom map of navigated nodes
                if tentativeIsBetter:
                    cameFrom[yNeig] = x
                    gScore[yNeig] = tentativeGScore
                    hScore[yNeig] = distFunc(yNeig, goal)
                    fScore[yNeig] = gScore[yNeig] + hScore[yNeig]
            # delete previous node distance values
            del gScore[x]
            del hScore[x]
            del fScore[x]
        # add to result the goal node (reconstructPath didn't do it)
        self.result.append(int(goal))
        # store the cost of the resulting minimal path
        if self.goal in gScore:
            self.resultCost = gScore[self.goal]
        else:
            self.resultCost = None
#            raise Exception('!!!Astar.process ERROR!!!\nOptimal Path can not arrive to the goal ',self.goal,'.\nCould be because of: goal node doesn\'t exist, graph is unconnected, graph is directed...')
        

    def reconstructPath(self, cameFrom, currentNode):
        self.result = [self.start]
        if currentNode in cameFrom:
            p = [self.reconstructPath(cameFrom, cameFrom[currentNode])]
            self.result.append(currentNode)
            return p
        else:
            return currentNode
        

    def dictMin(self, d):
        #need to invert the dictionary
        inv = dict(map(lambda item: (item[1], item[0]), d.items()))
        return inv[min(inv.keys())]
    
        
    def dictMax(self, d):
        #need to invert the dictionary
        inv = dict(map(lambda item: (item[1], item[0]), d.items()))
        return inv[max(inv.keys())]
    
    
    # ========== DIFERENT DISTANCE FUNCTIONS ==========
     
    def euclideanDist(self, node1, node2):
        start = self.city.getNode(int(node1))
        goal = self.city.getNode(int(node2))
#        return abs(numpy.sqrt((numpy.square((float(start[0][0]) - float(goal[0][0])) + (numpy.square(float(start[0][1]) - float(goal[0][1])))))))
        return math.fabs(math.sqrt( ((float(start[0][0])-float(goal[0][0]))*(float(start[0][0])-float(goal[0][0]))) + ((float(start[0][1])-float(goal[0][1]))*(float(start[0][1])-float(goal[0][1]))) ) )

#    def appearWeightsDist(self, node1, node2, ...):


if __name__ == '__main__':
    from city import City
    import parsers.CityToFile
    
    def xDist(x,y,n):
        return n
    parent = os.path.join(os.path.dirname(__file__), '..')
    path = parent + '/osmFiles/firenze/firenze_00.osm'
    city = City.City(path)
#    astar = Astar( city,  [(u'867230075',  u'266938723')])
#    astar = Astar( city,  [(u'867230075',  u'266938723'), (u'867230075',  u'82591707')])
    astar = Astar( city,  [(u'867230075',  u'266938723'), (u'867230075',  u'82591707'), (u'867230075',  u'249264782'), (u'867230075',  u'249264782')])
    print ('========== Astar (default euclidean distance) ==========')
    for k, v in astar.aggregateResults_d.iteritems():
        print k, (': '), v
    print
    print
    
    n=1
    distF = lambda x,y: xDist(x,y,n)
    astar = Astar( city,  [(u'867230075',  u'266938723'), (u'867230075',  u'82591707'), (u'867230075',  u'249264782'), (u'867230075',  u'249264782')], distF)
    print ('========== Astar (different distance function (n1 to n2 = 1 always) ==========')
    for k, v in astar.aggregateResults_d.iteritems():
        print k, (': '), v
    print
    print
    
    
    
#    print '========================'
#    print 'PROVA PER JORDI ESCOBAR:'
#    print '========================'
#    bcnPath = parent + '/osmFiles/barcelona/BCN_eixample.osm'
#    bcn = City.City(bcnPath)
#    astarBCN = Astar( bcn , [(218912194,1400747742),(1400747742,240949599),(240949599,30238421),(30238421,1362900007),(1362900007,1499890030),(1499890030,1480282267),(1480282267,152839674),(152839674,30884388),(30884388,798927010),(798927010,1404025853),(1404025853,218912194)])
#    astarBCN = Astar( bcn , [(218912194,1400747742),(1400747742,240949599),(240949599,30238421),(30238421,1362900007),(1362900007,1499890030),(1499890030,1480282267),(1480282267,152839674),(152839674,30884388),(30884388,798927010),(798927010,1404025853),(1404025853,218912194)], True)
#    print ('========== Astar (Barcelona) ==========')
#    for k, v in astarBCN.aggregateResults_d.iteritems():
#        print k, (': '), v
#    print
#    print
    
    print("test finished!")
