#*********************************************************************************************#
#********                              OSMI to tree Class                              *******#
#*********************************************************************************************#
# This class converts a .OSMI file into a tree structure and gives methods to work with it.   #

import xml.dom.minidom as minidom
import codecs

class OsmiTree():
    """
    This class converts a .OSMI file into a tree structure and gives methods to work with it.
    
    * An OSMI (Open Street Map Information) file stores the interesting and/or important places
    o an OSM file.
    
    * The OSMI format:
    OSMI use XML format and tries to be similar to OSM.
    The OSMI header define to which OSM file is referencing places:
      <osmi version="0.1" osm="[OSM file path]">
        ... place primitives ...
      </osmi>
    Then there is a list of 'place' primitives.
    A 'place' is the basic element of OSMI and it structure is the following:
        <place id="[integer>=1]" role="[important/interesting]">
          <member type="[node/way]" ref="[OSMnodeId/OSMwayId]"/>
          <member ... />
          ...
          <tag k="appearW" v="[float[0,1]]"/>
          <tag k="modifyW" v="[float[0,1]]"/>
          <tag ... />
          ...
        </place>
    """

    def __init__(self,osmiFile):
        osmiMap=open(osmiFile,"r")
        self.root=minidom.parseString(self.clean(osmiMap))
        
    def clean(self,fileToClean):
        """
             Erase the possible \n, \t, and "    " elements in the text
        """
        openFile=fileToClean.read()
        without_n= openFile.replace('\n','')
        without_t= without_n.replace('\t','')
        without_s= without_t.replace('    ','')
        return without_s
    
    def getCellSize(self):
        """
        return the cellSize attribute if found. If not, return None
        """
        osmiHeader = self.root.getElementsByTagName('osmi')
        return osmiHeader[0].getAttribute('cellsize')

    def getPlaceList(self):
        """
            returs a List with all the Places (important or interesting)
        """
        return self.root.getElementsByTagName('place')
    
    def getPlace(self,placeID):
        """
            Return the place which have the given ID
        """
        pList=self.getPlaceList()
        for element in pList:
            if element.getAttribute('id')==placeID:
                return element

    def createOSMIFile(self,path,name='newmap.osmi'):
        """
            It converts the internal structure into a OSMI file and stores
            it in the Path and name given (the name should contain the extension .osmi).
            If the file exists it will overwrite it.
        """
        path=path + '\\'+ name
        f=codecs.open(path,'w',encoding='utf-8')
        self.root.writexml(f)
        f.close()





#
#    def deleteBuildings(self):
#        """
#           Given a Type, it deletes all the ways which have building tag key     
#        """
#        ways=self.getWayList()
#        i=0
#        while i<len(ways):
#            tags=ways[i].getElementsByTagName('tag')
#            j=0
#            while j<len(tags):
#                if(tags[j].getAttribute('k')==u'building'):
#                    self.eraseNode(ways[i])
#                    j=len(tags)
#                else:
#                    j +=1
#            i +=1
#
#
#    def eraseNoTypeElements(self,Type):
#        """
#            Given a Type, it deletes all the ways which don't have it
#        """
#        ways=self.getWayList()
#        isThisType= 0
#        i=0
#        while i<len(ways):
#            tags=ways[i].getElementsByTagName('tag')
#            j=0
#            while j<len(tags):
#                if(tags[j].getAttribute('k')==Type):
#                    isThisType= 1
#                    j=len(tags)
#                else:
#                    j +=1
#            if isThisType== 0:
#                self.eraseNode(ways[i])
#            else:
#                isThisType=0
#            i +=1
#
#    def erase(self,objectList):
#        """
#            erase from the structure the elements in objectList
#        """
#        father=''
#        for element in objectList:
#            father=element.parentNode
#            father.removeChild(element)
#            
#    def eraseNode(self,Node):
#        """
#            erase the given Node from the structure
#        """
#        father = Node.parentNode
#        father.removeChild(Node)
#    
#    def getIntersectionNodes(self):
#        """
#            Returns a List with all the intersection node IDs
#        """
#        ways=self.getWayList()
#        nodeList=[]
#        intersectionList=[]
#        for wayElement in ways:
#            nodes=wayElement.getElementsByTagName('nd')
#            for nodeElement in nodes:
#                nodeList.append(nodeElement.getAttribute('ref'))
#        for nodeElement in nodeList:
#            if nodeList.count(nodeElement)>1 and intersectionList.count(nodeElement)==0:
#                intersectionList.append(nodeElement)
#        return intersectionList
#
#    def deleteNodeMarks(self):
#        """
#            Delete all the marks from the map nodes: bus stops, Hospitals,....
#            but not the node having them.
#        """
#        nList=self.getNodeList()
#        childs=[]
#        for element in nList:
#            childs=element.childNodes
#            nChilds=len(childs)
#            if nChilds!=0:
#                while nChilds!=0:
#                    nChilds -=1
#                    element.removeChild(childs[nChilds])
#    
#    def createOSMFile(self,path,name='newmap.osm'):
#        """
#            It converts the internal structure into a OSM file and stores
#            it in the Path and name given, if the file exists it will overwrite it.
#        """
#        path=path + '\\'+ name
#        f=codecs.open(path,'w',encoding='utf-8')
#        self.root.writexml(f)
#        f.close()
#
#    def markNodes(self,list,key,value):
#        """
#            Given a list of Nodes it adds a given mark to this Nodes.
#        """
#        for element in list:
#            node=self.getNode(element)
#            mark=self.root.createElement('tag')
#            mark.setAttribute('k',key)
#            mark.setAttribute('v',value)
#            node.appendChild(mark)
#            
#    def getCoordinates(self,nodeID):
#        """
#            Given a nodeID it returns the Coordinates from that node in format [Longitude,Latitude]
#        """
#        if nodeID != '':
#            node=self.getNode(nodeID)
#            list=[node.getAttribute('lon'),node.getAttribute('lat')]
#        return list
#
#    def getNodesCoordinates(self):
#        """
#            Returns a Dictionary with node ID as the index with Lon and Lat values
#        """
#        nodes=self.getNodeList()
#        coordinates={}
#        for node in nodes:
#            id=node.getAttribute('id')
#            coordinates[id]=[node.getAttribute('lon'),node.getAttribute('lat')]
#        return coordinates


