'''
Created on 11/12/2013

@author: oriol
'''
import sys,os.path
if not os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) in sys.path:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import math
import numpy as np

def polygonConvexHull(vs_l, keepOrder=True):
    """
    Returns the polygon vertices subset that get its convex hull.
    If keepOrder parameter is True the convex hull vertices will keep the clockwise or counter-clockwise order
    equal to the vs_l order, otherwise the convex hull result will be always on counter-clockwise order.
    PRE-CONTIDION: polygon (vs_l parameter) should be  closed (first and last vs_l element are the same)
                   coordinate tuples are (x,y), where x is the horizontal aix and y the vertical one.
    """

    # check the vs_l order, clockwise or counter-clockwise:
    if isClockwise(vs_l):
        clockwise = True
        # we revert the order of the vertices
        vs_l.reverse()
    else:
        clockwise = False


    ch_l = []
    vs_len = len(vs_l)
    # Get min and max lat and lon vertices to make the search shorter
    minLatV = vs_l[0]
    maxLatV = vs_l[0]
    minLonV = vs_l[0]
    maxLonV = vs_l[0]
    for v in vs_l[1:-1]:
        if v[0]<minLatV[0]:
            minLatV = v
        if v[0]>maxLatV[0]:
            maxLatV = v
        if v[1]<minLonV[1]:
            minLonV = v
        if v[1]>maxLonV[1]:
            maxLonV = v
            
    # we start the convex hull process from the minimum longitude value vertex and search the convex hull nodes counter-clockwise
    # _____ from minLat to maxLon _____
    ch_l.append(minLonV)
    actPos = vs_l.index(minLonV)
    if actPos>0:
        fromPos = actPos-1
    else:
        fromPos = len(vs_l)-1
    lastPos = vs_l.index(maxLatV)
    while actPos!=lastPos:
        # we go vertices towards until we find an angle bigger than the minimum found at the moment.
        minAngle = 400.
        minPos = actPos+1
        i = actPos
        while i != lastPos:
            if i<vs_len-2:
                nextPos = i+1
                i+=1
            else:
                nextPos = 0
                i=0
            nextAngle = angle_between_positiveDegrees(vs_l[fromPos],vs_l[actPos],vs_l[nextPos])  
            if nextAngle<minAngle:
                minAngle = nextAngle
                minPos = nextPos
        if ch_l[-1]!=vs_l[minPos]: # We don't want repeated nodes in the convex hull. This could happend with polygons having an inside bucle.
            ch_l.append(vs_l[minPos])
        fromPos = actPos
        actPos = minPos
    # _____ from maxLat to maxLon _____
    lastPos = vs_l.index(maxLonV)
    while actPos!=lastPos:
        # we go vertices towards until we find an angle bigger than the minimum found at the moment.
        minAngle = 400.
        minPos = actPos+1
        i = actPos
        while i != lastPos:
            if i<vs_len-2:
                nextPos = i+1
                i+=1
            else:
                nextPos = 0
                i=0
            nextAngle = angle_between_positiveDegrees(vs_l[fromPos],vs_l[actPos],vs_l[nextPos])  
            if nextAngle<minAngle:
                minAngle = nextAngle
                minPos = nextPos
        if ch_l[-1]!=vs_l[minPos]: # We don't want repeated nodes in the convex hull. This could happend with polygons having an inside bucle.
            ch_l.append(vs_l[minPos])
        fromPos = actPos
        actPos = minPos
    # _____ from maxLon to minLat _____
    lastPos = vs_l.index(minLatV)
    while actPos!=lastPos:
        # we go vertices towards until we find an angle bigger than the minimum found at the moment.
        minAngle = 400.
        minPos = actPos+1
        i = actPos
        while i != lastPos:
            if i<vs_len-2:
                nextPos = i+1
                i+=1
            else:
                nextPos = 0
                i=0
            nextAngle = angle_between_positiveDegrees(vs_l[fromPos],vs_l[actPos],vs_l[nextPos])  
            if nextAngle<minAngle:
                minAngle = nextAngle
                minPos = nextPos
        if ch_l[-1]!=vs_l[minPos]: # We don't want repeated nodes in the convex hull. This could happend with polygons having an inside bucle.
            ch_l.append(vs_l[minPos])
        fromPos = actPos
        actPos = minPos
    # _____ from minLat to minLon _____
    lastPos = vs_l.index(minLonV)
    while actPos!=lastPos:
        # we go vertices towards until we find an angle bigger than the minimum found at the moment.
        minAngle = 400.
        minPos = actPos+1
        i = actPos
        while i != lastPos:
            if i<vs_len-2:
                nextPos = i+1
                i+=1
            else:
                nextPos = 0
                i=0
            nextAngle = angle_between_positiveDegrees(vs_l[fromPos],vs_l[actPos],vs_l[nextPos])  
            if nextAngle<minAngle:
                minAngle = nextAngle
                minPos = nextPos
        if ch_l[-1]!=vs_l[minPos]: # We don't want repeated nodes in the convex hull. This could happend with polygons having an inside bucle.
            ch_l.append(vs_l[minPos])
        fromPos = actPos
        actPos = minPos
    
    if (keepOrder==True) and (clockwise==True):
        # revert ch_l order
        ch_l.reverse()

    return ch_l

# ========= POLYGON ORDER ==========

def isClockwise(vs_l):
    """
    Returns True if the vs_l is ordered in clockwise, otherwise it returns False
    """
    sum = 0.0
    for i in range(len(vs_l)-1):
        edge = (vs_l[i+1][0] - vs_l[i][0]) * (vs_l[i+1][1] + vs_l[i][1])
        sum += edge
    return sum > 0.0

# ========== ANGLE METHODS ==========
def angle_between_positiveDegrees(A,O,B):
    """
    Return the angle between points A, O and B in this order, in counter-clockwise rotation always.
    Values go from 0 to 360
    """
    avD = angle_wrt_x_positiveDegrees(O,A)
    bvD = angle_wrt_x_positiveDegrees(O,B)
    angle = bvD - avD
    if angle>0.:
        return angle
    else:
        return (angle+360)%360

def angle_wrt_x(A,B):
    """Return the angle between B-A and the positive x-axis.
    Values go from 0 to pi in the upper half-plane, and from 
    0 to -pi in the lower half-plane.
    """
    ax, ay = A
    bx, by = B
    return math.atan2(by-ay, bx-ax)

def angle_wrt_x_degrees(A,B):
    """Return the angle between B-A and the positive x-axis.
    Values go from 0 to 180 in the upper half-plane, and from 
    0 to -180 in the lower half-plane.
    """
    ax, ay = A
    bx, by = B
    return math.atan2(by-ay, bx-ax)*180./math.pi

def angle_wrt_x_positiveDegrees(A,B):
    """Return the angle between B-A and the positive x-axis.
    Values go from 0 to 360.
    """
    ax, ay = A
    bx, by = B
    return ((math.atan2(by-ay, bx-ax)*180./math.pi)+360)%360

#=================================================================
#=================================================================
#=================================================================

if __name__=="__main__":
    
    polygon = [(2,7),(2,9),(0,8),(0,6),(3,5),(1,3),(3,1),(4,0),(6,2),(8,2),(8,5),(9,7),(7,7),(6,5),(5,5),(6,8),(4,7),(2,7)]
    print polygonConvexHull(polygon)
    
    polygon.reverse()
    print polygonConvexHull(polygon)
    print polygonConvexHull(polygon,False)
    
    poly2 = [(3,2),(2,1),(0,0),(2,3),(3,2)]
    print polygonConvexHull(poly2,False)
    
    poly3 = [(0,4),(2,5),(3,0),(3,2),(4,4),(4,6),(5,7),(6,8),(8,8),(9,7),(10,6),(11,9),(0,10),(0,4)]
    print polygonConvexHull(poly3)
    
    poly4 = [(2,0),(4,2),(5,3),(5,5),(3,5),(2,4),(1,3),(0,4),(0,2),(2,0)]
    print polygonConvexHull(poly4)
    
    
    print
    print 'DONE'
    
