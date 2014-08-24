'''
Created on 22/04/2013

@author: oriol
'''
import sys,os.path
if not os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) in sys.path:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
# Determine the area of a 2D polygons represented as a list of (x,y) vertex coordinates

def polygonArea(vs_l):
    area = 0.5 * abs(sum(x0*y1 - x1*y0 for ((x0, y0), (x1, y1)) in segments(vs_l)))
    return area

def segments(p):
    return zip(p, p[1:] + [p[0]])

#=================================================================
#=================================================================
#=================================================================

if __name__=="__main__":
    
    polygon = [(0,10),(10,10),(10,0),(0,0)]
    print polygonArea(polygon)
    polygon.insert(1, (5,15))
    print polygonArea(polygon)
    
    print
    print 'DONE'
    
