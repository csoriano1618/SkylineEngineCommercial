#***********************************************************************************************************************************************************#
#********                                       OSM to tree Class                                                                                   ********#
#***********************************************************************************************************************************************************#
# This class converts a .OSM file into a tree structure and gives methods to work with it                                                                   #
import xml.dom.minidom as minidom
import codecs

class OsmTree():

    def __init__(self,osmFile):
        osmMap=open(osmFile,"r")
        self.root=minidom.parseString(self.clean(osmMap))
        (self.minLat, self.minLon, self.maxLat, self.maxLon) = self.getBoundingBox()

    def getBoundingBox(self):
        bounds = self.root.getElementsByTagName('bounds')
        if len(bounds)==0:
            return (None, None, None, None)
        else:
            for element in bounds:
                return (element.getAttribute('minlat'),element.getAttribute('minlon'),element.getAttribute('maxlat'),element.getAttribute('maxlon'))

    def clean(self,fileToClean):
        """
             Erase the possible \n, \t, and "    " elements in the text
        """
        openFile=fileToClean.read()
        without_n= openFile.replace('\n','')
        without_t= without_n.replace('\t','')
        without_s= without_t.replace('    ','')
        return without_s

    def getWayList(self):
        """
            returs a List with all the Ways (streets and other elements)
        """
        return self.root.getElementsByTagName('way')

    def getNodeList(self):
        """
            returns a List of all Nodes
        """
        return self.root.getElementsByTagName('node')

    def deleteBuildings(self):
        """
           Given a Type, it deletes all the ways which have building tag key     
        """
        ways=self.getWayList()
        i=0
        while i<len(ways):
            tags=ways[i].getElementsByTagName('tag')
            j=0
            while j<len(tags):
                if(tags[j].getAttribute('k')==u'building'):
                    self.eraseNode(ways[i])
                    j=len(tags)
                else:
                    j +=1
            i +=1


    def eraseNoTypeElements(self,Type):
        """
            Given a Type, it deletes all the ways which don't have it
        """
        ways=self.getWayList()
        isThisType= 0
        i=0
        while i<len(ways):
            tags=ways[i].getElementsByTagName('tag')
            j=0
            while j<len(tags):
                if(tags[j].getAttribute('k')==Type):
                    isThisType= 1
                    j=len(tags)
                else:
                    j +=1
            if isThisType== 0:
                self.eraseNode(ways[i])
            else:
                isThisType=0
            i +=1

    def erase(self,objectList):
        """
            erase from the structure the elements in objectList
        """
        father=''
        for element in objectList:
            father=element.parentNode
            father.removeChild(element)
            
    def eraseNode(self,Node):
        """
            erase the given Node from the structure
        """
        father = Node.parentNode
        father.removeChild(Node)
    
    def getIntersectionNodes(self):
        """
            Returns a List with all the intersection node IDs
        """
        ways=self.getWayList()
        nodeList=[]
        intersectionList=[]
        for wayElement in ways:
            nodes=wayElement.getElementsByTagName('nd')
            for nodeElement in nodes:
                nodeList.append(nodeElement.getAttribute('ref'))
        for nodeElement in nodeList:
            if nodeList.count(nodeElement)>1 and intersectionList.count(nodeElement)==0:
                intersectionList.append(nodeElement)
        return intersectionList

    def getWay(self,wayID):
        """
            Return the Way which have the given ID
        """
        wList=self.getWayList()
        for element in wList:
            if element.getAttribute('id')==wayID:
                return element
            
    def getNode(self,nodeID):
        """
            Return the Node which have the given ID
        """
        nList=self.getNodeList()
        for element in nList:
            if element.getAttribute('id')==nodeID:
                return element

    def getNodeHeaderInfo(self,nodeID):
        """
            Return the Node which have the given ID header info 
        """
        nList=self.getNodeList()
        for element in nList:
            if element.getAttribute('id')==nodeID:
                return element.getAttributes()
            
    def deleteNodeMarks(self):
        """
            Delete all the marks from the map nodes: bus stops, Hospitals,....
            but not the node having them.
        """
        nList=self.getNodeList()
        childs=[]
        for element in nList:
            childs=element.childNodes
            nChilds=len(childs)
            if nChilds!=0:
                while nChilds!=0:
                    nChilds -=1
                    element.removeChild(childs[nChilds])
    
    def createOSMFile(self,path,name='newmap.osm'):
        """
            It converts the internal structure into a OSM file and stores
            it in the Path and name given, if the file exists it will overwrite it.
        """
        path=path + '\\'+ name
        f=codecs.open(path,'w',encoding='utf-8')
        self.root.writexml(f)
        f.close()

    def markNodes(self,list,key,value):
        """
            Given a list of Nodes it adds a given mark to this Nodes.
        """
        for element in list:
            node=self.getNode(element)
            mark=self.root.createElement('tag')
            mark.setAttribute('k',key)
            mark.setAttribute('v',value)
            node.appendChild(mark)
            
    def getCoordinates(self,nodeID):
        """
            Given a nodeID it returns the Coordinates from that node in format [Longitude,Latitude]
        """
        if nodeID != '':
            node=self.getNode(nodeID)
            list=[node.getAttribute('lon'),node.getAttribute('lat')]
        return list

    def getNodesCoordinates(self):
        """
            Returns a Dictionary with node ID as the index with Lon and Lat values
        """
        nodes=self.getNodeList()
        coordinates={}
        for node in nodes:
            id=node.getAttribute('id')
            coordinates[id]=[node.getAttribute('lon'),node.getAttribute('lat')]
        return coordinates


