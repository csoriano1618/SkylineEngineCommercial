'''
Created on 18/04/2013

@author: oriol
'''
import sys,os.path
if not os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) in sys.path:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from city import City
from copy import *
import random
import sys
import math
import copy

class MeanValueCoordinates:
    
    def __init__(self, cageCoords_l, queryCoords):
        """
        This class __init__ method will get:
        - a list of vertex coordinates defining a cage, a closed polygon in the counter clockwise direction.
        - a coordinates pair (x,y) of the query point (x horizontal aix and y vertical aix).
        And will fill the weights for the barycentric coordinates of the query point as baryCoords_l
        """
        self.baryCoords_l = []
        
        nSize = len(cageCoords_l)
        
        if nSize<3:
            print "the cage should have more than two vertices"
            raise Exception ('!!! ERROR !!! on MeanValueCoordinates.__init__ !!!')
        else:
            s_l = []
            # initialize relative coordinates and baryCoords_l weights
            for i,cageC in enumerate(cageCoords_l):
                dx = cageC[0]-queryCoords[0]
                dy = cageC[1]-queryCoords[1]
                s_l.append((dx,dy))
                self.baryCoords_l.append(0.)
            # get numeric limits
            eps = 10. * sys.float_info.min
            
            # check if any coordinates close to the cage point or lie on the cage boundary (special cases) if not normal:
            specialCase = False
            i = 0
            while (not specialCase) and (i<len(s_l)):
                ip = (i+1) % nSize        # next pos
                ri = math.sqrt( s_l[i][0]*s_l[i][0] + s_l[i][1]*s_l[i][1] )
                Ai = 0.5 * ( s_l[i][0]*s_l[ip][1] - s_l[ip][0]*s_l[i][1] )
                Di = s_l[ip][0]*s_l[i][0] + s_l[ip][1]*s_l[i][1]
                
                # Close to cage vertex?
                if ( ri <= eps ):
                    self.baryCoords_l[i] = 1.0
                    specialCase = True
                # Lie on cage boundary?
                elif ( math.fabs(Ai)<=0 and Di<0.0 ):
                    dx = cageCoords_l[ip][0] - cageCoords_l[i][0]
                    dy = cageCoords_l[ip][1] - cageCoords_l[i][1]
                    dl = math.sqrt( dx*dx + dy*dy )
                    if dl<eps:
                        pass
                    else:
                        dx = queryCoords[0] - cageCoords_l[i][0]
                        dy = queryCoords[1] - cageCoords_l[i][1]
                        mu = math.sqrt( dx*dx + dy*dy ) / dl
                        if (mu>=0.) and (mu<=1.):
                            self.baryCoords_l[i] = 1.-mu
                            self.baryCoords_l[ip] = mu
                            specialCase = True
                        else:
                            pass
                i += 1
                        
            # Normal cases
            if not specialCase:
                tanalpha_l = []
                wsum = 0.
                for i,v in enumerate(s_l):
                    ip = (i+1)%nSize        #next pos
                    im = (nSize-1+i)%nSize  #previous pos
                    ri = math.sqrt( s_l[i][0]*s_l[i][0] + s_l[i][1]*s_l[i][1] )
                    rp = math.sqrt( s_l[ip][0]*s_l[ip][0] + s_l[ip][1]*s_l[ip][1] )
                    Ai = 0.5 * ( s_l[i][0]*s_l[ip][1] - s_l[ip][0]*s_l[i][1] )
                    Di = s_l[ip][0]*s_l[i][0] + s_l[ip][1]*s_l[i][1]
                    
                    
                    if (Ai==0):
                        print 'STOP!!!'
                    
                    
                    tanalpha_l.append( (ri*rp - Di) / (2.0*Ai) )
                    if i>0:
                        wi = 2. * (tanalpha_l[i]+tanalpha_l[im]) / ri
                        wsum += wi
                        self.baryCoords_l[i] = wi
                r0 = math.sqrt( s_l[0][0]*s_l[0][0] + s_l[0][1]*s_l[0][1] )
                w0 = 2. * (tanalpha_l[0]+tanalpha_l[-1]) /r0
                wsum += w0
                self.baryCoords_l[0] = w0
                         
                if (math.fabs(wsum)>0.):
                    for i,c in enumerate(self.baryCoords_l):
                        self.baryCoords_l[i] = c/wsum
                        
    def getWeights(self):
        """
        This method returns the weights list baryCoords_l
        """
        return self.baryCoords_l
                        
    
          
#=================================================================
#=================================================================
#=================================================================

if __name__=="__main__":
    
    print '-----------------'
    print '| __main__ TEST |'
    print '-----------------'
    
    cage = [ (2,2) , (2,3) , (3,3) , (3,2) ]
    p1 = (2.5, 2.5)
    p2 = (2, 3)
    p3 = (3, 2.5)
    p4 = (2.75, 2.75)
    mvc = MeanValueCoordinates(cage,p1)
    w_l = mvc.getWeights()
    print 'Weights for point ', p1 ,': ', w_l
    mvc = MeanValueCoordinates(cage,p2)
    w_l = mvc.getWeights()
    print 'Weights for point ', p2 ,': ', w_l
    mvc = MeanValueCoordinates(cage,p3)
    w_l = mvc.getWeights()
    print 'Weights for point ', p3 ,': ', w_l
    mvc = MeanValueCoordinates(cage,p4)
    w_l = mvc.getWeights()
    print 'Weights for point ', p4 ,': ', w_l
    
    print
    print 'DONE'
      