# -*- coding: utf-8 -*-
# Copyright 2011 Gustavo Patow
# Copyright 2014 Carlos Soriano Sánchez <carlos.soriano89@gmail.com>


from xml.dom import minidom
from xml.dom import  Node


class XMLParser:
    '''
    A simple XML parser. Use:
    xmlParser = XMLParser(path)
    item = xmlParser.read("tag")
    '''

    def __init__(self, path):
        openedFile = open(path).read()
        self.pT_File = self.clean(openedFile)
        self.pT_File = minidom.parseString(self.pT_File)


    def read(self, tag):
        elementsList = self.pT_File.getElementsByTagName(tag)
        nodes = self.keepNodesOnly(elementsList)
        return nodes


    def clean(self, fileToClean):
        without_n = fileToClean.replace('\n', '')
        without_t = without_n.replace('\t', '')
        return without_t


    def getNextNode(self, sibling, tagName):
        childNode = sibling
        while childNode != None:
            if childNode.nodeType == Node.ELEMENT_NODE and childNode.nodeName == tagName:
                return childNode
            childNode = childNode.nextSibling
        return childNode


    def keepNodesOnly(self, nodes):
        for n in nodes:
            if n.nodeType == Node.TEXT_NODE:
                nodes.remove(n)
        return nodes


    def getAttrib(self, node, attrib):
        return node.attributes.getNamedItem(attrib).nodeValue.encode('latin')
