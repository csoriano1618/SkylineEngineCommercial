# -*- coding: utf-8 -*-
# Copyright 2014 Carlos Soriano Sánchez <carlos.soriano89@gmail.com>

from city import City
from tools import PointInPolygon
import numpy
import random
import math
import difflib
import traceback

EPSILON = 0.00001
EARTH_RADIUS = 6371009 # meters
# 1 should be enough for cover all the city of any city
POXIMITY_ACCELERATOR_RADIUS = 0.02

SUCCESS = True
NO_SUCCESS = False

def findTwoClosestNodes(city, closestStreet, point):
    streetNodes = city.getWayNodes(closestStreet)
    # Find the two nodes closer to the point, so we can project to
    # a segment of the street
    # Find the closer node
    closestNode = streetNodes[0]
    nodeLocation = [city.getNodeLat(closestNode),
                    city.getNodeLon(closestNode)]
    minorDistance = vecModule(vecSub(nodeLocation, point))
    for streetNode in streetNodes:
        nodeLocation = [city.getNodeLat(streetNode),
                        city.getNodeLon(streetNode)]
        distanceNodePoint = vecModule(vecSub(nodeLocation, point))
        if (distanceNodePoint < minorDistance):
            closestNode = streetNode
            minorDistance = distanceNodePoint

    # Filter nodes which remains in the closer street for further
    # calculation of the second closer node
    streetNeigNodes = []
    neighbourNodes = city.getNodeNeigNodes(closestNode)
    for neighbourNode in neighbourNodes:
        if (neighbourNode[City.WAY] == closestStreet):
            streetNeigNodes.append(neighbourNode)

    # Extract the actual nodes from the data to work easier with this
    # list further on
    streetNeigNodes = [streetNeigNode[City.NODES] for streetNeigNode in
                       streetNeigNodes]
    # Find the second closer node
    secondClosestNode = streetNeigNodes[0]
    nodeLocation = [city.getNodeLat(secondClosestNode),
                    city.getNodeLon(secondClosestNode)]
    minorDistance = vecModule(vecSub(nodeLocation, point))
    for neighbourNode in streetNeigNodes:
        nodeLocation = [city.getNodeLat(neighbourNode),
                        city.getNodeLon(neighbourNode)]
        distanceNodePoint = vecModule(vecSub(nodeLocation, point))
        if (distanceNodePoint < minorDistance):
            secondClosestNode = neighbourNode
            minorDistance = distanceNodePoint

    return closestNode, secondClosestNode


def findProjectableLine(city, closestStreet, point):
    streetNodes = city.getWayNodes(closestStreet)

    for index in range(len(streetNodes)):
        if (index == len(streetNodes) - 1):
            break
        currentNode = streetNodes[index]
        nextNode = streetNodes[index + 1]
        # Project point to one street line of the street
        line = [[city.getNodeLat(currentNode), city.getNodeLon(currentNode)],
                [city.getNodeLat(nextNode), city.getNodeLon(nextNode)]]
        projectedPoint = projectionOnLine(point, line)
        # If the point is projectable in that line, just use that nodes
        if (pointInSegment(line[0], line[1], projectedPoint)):
            break

    # If didn't find any line to project the point in the street,
    # just return None, None
    if index == len(streetNodes):
        return None, None

    return currentNode, nextNode


def addNodeToCloserStreetByPoint(city, point):
    '''
    Add a node to the closest projected point in a street given a point

    Return the value and a indicator of SUCCESS or NO_SUCCESS.
    If SUCCESS, the value is the nodeID
    If NO_SUCCESS, the value can be the projected point if the function
    achieved to project the point but it's outside the street or invalid.
    And None as a value if the function couldn't calculate even the projection
    of the point.
    '''
    # Given that the boundings box is done with min and max values,
    # construct a real polygon.
    bb = city.getStreetsBoundingBox()

    polygon = [[bb[0], bb[1]], # minX, minY
               [bb[2], bb[1]], # maxX, minY
               [bb[2], bb[3]], # maxX, maxY
               [bb[0], bb[3]]] # minX, maxY
    if (not PointInPolygon.pointInPolygon(point[0], point[1], polygon)):
        raise Exception('Point ' + str(point) + ' outside city street boundaries ' + str(polygon))
    try:
        closestStreet = city.getPointNearestStreetCloserThan(point[0],
                                                             point[1])[0]
    except Exception:
        raise Exception("City getPointNearestStreetCloserThan exception")

    # Project point to the street line nearest to the generated point
    line = [[city.getNodeLat(node1), city.getNodeLon(node1)],
            [city.getNodeLat(node2), city.getNodeLon(node2)]]
    try:
        projectedPoint = projectionOnLine(point, line)
    except Exception:
        raise Exception("Couldn't project point " +str(point) + " on line " + str(
            line))
    # Check if the projection remains outside the line itself.
    # If so, just use the nearest node location as the projection
    # point.
    if (not pointInSegment(line[0], line[1], projectedPoint)):
        # Sadly we can't have two nodes in the same exact position
        # so we need to skip nodes which remain outside the street
        # when projected
        raise PointOutsideSegment("Projected point outside segment ", projectedPoint)

    # Add the point as a new node of the street in the required
    # position
    nodeId = addPointBetweenNodes(node1, node2,
                                  projectedPoint, closestStreet,
                                  city)
    return nodeId

def getMatchingStreetName(city, name):
    '''
    Matchs the closer name to a street, similar to what spelling
    engines does, and return its id.
    Params:
        - city: The city instance o which the streets are defined
        - name: Street name
    Return:
        The street id to which the name is closest. None if there is not a
        street with a "enough good"[0] matching result.
        [0] http://docs.python.org/2/library/difflib.html#difflib.get_close_matches
    '''
    streets = city.getStreetWays()
    streetNames = {}
    for street in streets:
        info = city.getWayTags_d(street)
        if 'name' in info:
            streetNames[info['name']] = street
    matchingNames = difflib.get_close_matches(name, streetNames.keys(), len(streetNames.keys()))

    return streetNames[matchingNames[0]] if len(matchingNames) > 0 else None


def getRandomPointInsideEdge(point1, point2):
    length = vecModule(vecSub(point1, point2))
    randomLength = random.random() * length
    direction = (point2 - point1) / length
    directionWithMagnitude = vecScalarProduct(direction, randomLength)
    point = vecSum(point1, directionWithMagnitude)

    return point


def getRandomPointInsideRect(polygon):
    '''
    Rigth hand defined polygon using latitude and longitude, which is reverse
    as normal (x, y) system
    '''
    minCornerIndex = findMinCornerIndex(polygon)

    u = vecSub(polygon[minCornerIndex], polygon[int(math.fmod(minCornerIndex + 1, len(polygon)))])
    previousMinIndex = len(polygon) - 1 if minCornerIndex == 0 else minCornerIndex - 1
    v = vecSub(polygon[minCornerIndex], polygon[previousMinIndex])

    uLength = vecModule(u)
    vLength = vecModule(v)

    uRandomValue = random.random() * uLength
    vRandomValue = random.random() * vLength
    point = vecSum([uRandomValue, vRandomValue], polygon[minCornerIndex])

    return point


def generateRandomNodeInEdge(edge, city):
    edgePoint1 = numpy.array([city.getNodeLat(edge[City.NODES][0]),
                              city.getNodeLon(edge[City.NODES][0])])
    edgePoint2 = numpy.array([city.getNodeLat(edge[City.NODES][1]),
                              city.getNodeLon(edge[City.NODES][1])])

    if (vecModule(vecSub(edgePoint1, edgePoint2)) < EPSILON):
        raise Exception("Edge with modul 0 " + str([edgePoint1, edgePoint2]))

    randomPoint = getRandomPointInsideEdge(edgePoint1, edgePoint2)
    nodeId = city.addNode(None, randomPoint[0], randomPoint[1])
    wayNodes = city.getWayNodes(edge[City.WAY])

    # Find node positions, so we can add the new node in the way
    posNode0 = None
    posNode1 = None
    pos = 0

    for node in wayNodes:
        if (node == edge[City.NODES][0]):
            posNode0 = pos;
        if (node == edge[City.NODES][1]):
            posNode1 = pos;
        if (posNode0 != None and posNode1 != None):
            break;
        pos += 1

    #Insert position is between pos -1 and pos, so take the biggest
    # to insert between them
    insertPosition = posNode0 if (posNode0 > posNode1) else posNode1
    city.addWayNode(edge[City.WAY], nodeId, insertPosition)

    return nodeId


def generateRandomNodeInWay(way, city):
    nodes = city.getWayNodes(way)
    nodeIndex1 = random.randint(0, len(nodes) - 2)
    nodeIndex2 = nodeIndex1 + 1;

    edgePoint1 = numpy.array([city.getNodeLat(nodes[nodeIndex1]),
                              city.getNodeLon(nodes[nodeIndex1])])
    edgePoint2 = numpy.array([city.getNodeLat(nodes[nodeIndex2]),
                              city.getNodeLon(nodes[nodeIndex2])])

    randomPoint = getRandomPointInsideEdge(edgePoint1, edgePoint2)
    nodeId = city.addNode(None, randomPoint[0], randomPoint[1])

    #Insert position is between pos -1 and pos, so take the biggest
    # to insert between them
    city.addWayNode(way, nodeId, nodeIndex2)

    return nodeId


def addPointBetweenNodes(node1, node2, pointToAdd, street, city):
    nodeId = city.addNode(None, pointToAdd[0], pointToAdd[1])
    wayNodes = city.getWayNodes(street)

    # Find node positions, so we can add the new node in the way
    posNode0 = None
    posNode1 = None
    pos = 0

    for node in wayNodes:
        if (node == node1):
            posNode0 = pos;
        if (node == node2):
            posNode1 = pos;
        if (posNode0 != None and posNode1 != None):
            break;
        pos += 1

    #Insert position is between pos -1 and pos, so take the biggest
    # to insert between them
    insertPosition = posNode0 if (posNode0 > posNode1) else posNode1
    city.addWayNode(street, nodeId, insertPosition)

    return nodeId


def findMinCornerIndex(polygon):
    minCorner = polygon[0]
    index = 0
    count = 0
    for point in polygon:
        if point[0] < minCorner[0] and point[1] < minCorner[1]:
            minCorner = point
            index = count
        count += 1

    return index


def rectangleArea(polygon):
    '''
    Area of a polygon defined in latitude and longitude points. The area
    is calculated in square meters using the harvesine formula to convert
    from distances between latitude longitude points to meters.
    '''
    minCornerIndex = findMinCornerIndex(polygon)

    u = numpy.array([polygon[minCornerIndex], polygon[int(math.fmod(minCornerIndex + 1, len(polygon)))]])
    previousMinIndex = len(polygon) - 1 if minCornerIndex == 0 else minCornerIndex - 1
    v = numpy.array([polygon[minCornerIndex], polygon[previousMinIndex]])

    uLength = numpy.linalg.norm(u)
    vLength = numpy.linalg.norm(v)

    return uLength * vLength


def distance(latitude1, longitude1, latitude2, longitude2):
    '''
    Calculate the distance in meters between points defined in latitude and
    longitude using harvesine formula.
    http://en.wikipedia.org/wiki/Haversine_formula
    '''
    dLat = math.radians(latitude1 - latitude2)
    dLon = math.radians(longitude1 - longitude2)
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + \
        math.cos(math.radians(latitude1)) * math.cos(math.radians(latitude2)) * \
	    math.sin(dLon / 2) * math.sin(dLon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = EARTH_RADIUS * c
    return d


def centerOfPoints(points):
    sum = [0, 0]
    for point in points:
        sum = vecSum(sum, point)
    return vecScalarProduct(sum, 1. / len(points))


def vecModule(vec):
    return math.sqrt(vec[0] * vec[0] + vec[1] * vec[1])


def vecScalarProduct(vec, scalar):
    return [vec[0] * scalar, vec[1] * scalar]


def vecSum(vec1, vec2):
    return [vec1[0] + vec2[0], vec1[1]+ vec2[1]]


def vecSub(vec1, vec2):
    return [vec1[0] - vec2[0], vec1[1] - vec2[1]]


def vecDotProduct(vec1, vec2):
    return vec1[0] * vec2[0] + vec1[1] * vec2[1]


def vecNormalize(vec):
    module = vecModule(vec)
    return [vec[0] / module, vec[1] / module]


def pointInSegment(p1, p2, pIO, epsilon=None):
    '''
    >>> p1 = [0,0,0]
    >>> p2 = [0,1,0]
    >>> p3 = [0, 0.5, 0]
    >>> pointInSegment(p1, p2, p3)
    True

    >>> p1 = [1,0,0]
    >>> p2 = [0,1,0]
    >>> p3 = [0.5, 0.5, 0]
    >>> pointInSegment(p1, p2, p3)
    True
    '''

    if(not epsilon):
        epsilon = EPSILON

    vec12 = vecSub(p2, p1)
    vec1IO = vecSub(pIO, p1)
    vec21 = vecSub(p1, p2)
    vec2IO = vecSub(pIO, p2)

    dotProduct1 = vecDotProduct(vec12, vec1IO)
    dotProduct2 = vecDotProduct(vec21, vec2IO)

    proj1 = dotProduct1 / vecModule(vec12)
    proj2 = dotProduct2 / vecModule(vec12)
    if(proj1 < 0):
        # Extrem case
        if(vecModule(vec1IO) > epsilon):
            return False
    if(proj2 < 0):
        # Extrem case
        if(vecModule(vec2IO) > epsilon):
            return False

    distance = vecModule(
        vecSub(pIO, vecSum(p1, vecScalarProduct(vecNormalize(vec12), proj1))))

    if(distance > epsilon):
        return False
    return True


def projectionOnLine(pointToProject, line):
    vectorToPoint = vecSub(pointToProject, line[0])
    lineVector = vecSub(line[1], line[0])
    distanceToProjection = vecDotProduct(vectorToPoint, lineVector) / vecModule(lineVector)

    return vecSum(line[0], vecScalarProduct(vecNormalize(lineVector), distanceToProjection))


class PointOutsideSegment(Exception):

    def __init__(self, msg, value):
        self.message = msg
        self.value = value

    def __str__(self):
        return self.message + repr(self.value)