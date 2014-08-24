# -*- coding: utf-8 -*-
# Copyright 2014 Carlos Soriano Sánchez <carlos.soriano89@gmail.com


from tools import XMLParser


class XMLDensityParser(XMLParser.XMLParser):


    def getAllCells(self):
        return self.read('cell')


    def getCellId(self, cell):
        id = cell.getElementsByTagName('id')[0]
        value = id.childNodes[0].nodeValue.encode('latin')
        return value


    def getCellDensity(self, cell):
        id = cell.getElementsByTagName('density')[0]
        value = id.childNodes[0].nodeValue.encode('latin')
        return value

    def getDivisions(self):
        divisions = self.read('divisions')[0]
        value = divisions.childNodes[0].nodeValue.encode('latin')
        return int(value)


    def getParentNode(self, node):
        return node.parentNode
