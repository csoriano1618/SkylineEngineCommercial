'''
Created on 19/06/2012

@author: oriol
'''
import sys,os.path
if not os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) in sys.path:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs (x horizontal axis, y vertical axis) without repeating first and last vertex
# This function returns True or False.  The algorithm is called
# "Ray Casting Method".

def pointInPolygon(x,y,poly):

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

#=================================================================
#=================================================================
#=================================================================

if __name__=="__main__":
    
    polygon = [(0,10),(10,10),(10,0),(0,0)]
    point_x = 5
    point_y = 5
    print pointInPolygon(point_x,point_y,polygon)
    point_y = 20
    print pointInPolygon(point_x,point_y,polygon)
    
    print
    print 'DONE'
    
