# -*- coding: utf-8 -*-
# Copyright 2014 Carlos Soriano Sánchez <carlos.soriano89@gmail.com>

import sys,os.path
from commercial.Market import Market

from commercial.Shop import Shop
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import Tkinter
import ToolsExt
from city import City
from tools import Colors
from tools import ParseParameters
import math
# For size constants. If not buildings used, this dependency can be deleted
from commercial import Building
import datetime

DRAW_MARGIN = 10
WINDOW_TITLE_HEIGHT = 50
SCROLLBARS_MARGIN = 30

DOT_SIZE_AGENT = 1
MIN_DOT_SIZE = 2
MAX_DOT_SIZE = 10

LABEL_TEXT_SIZE = 11
LABEL_TEXT_SIZE_BIG = 100
# Little less than MAX_DOT_SIZE / 2 + LABEL_TEXT_SIZE
LABEL_Y_OFFSET = - (MAX_DOT_SIZE / 2 + LABEL_TEXT_SIZE + 2)
LABEL_AGENTS_WIDTH = 40
LABEL_MARKET_WIDTH = 80
# Half of the width, so the label is centered
LABEL_AGENTS_X_OFFSET = - LABEL_AGENTS_WIDTH / 2
# Half of the width, so the label is centered
LABEL_MARKET_X_OFFSET = - LABEL_MARKET_WIDTH / 2

TIME_LABEL_Y_OFFSET = 10
TIME_LABEL_X_OFFSET = 10
TIME_LABEL_WIDTH = 140


class CommercialVisualizerWindow():


    def __init__(self, tkProccess):
        self.root = Tkinter.Toplevel(tkProccess)
        self.canvas = None


    def spawn(self, city, commercial, extraData = {}):
        '''

        :param city:
        :param commercial:
        :param dotList:
        :param paintCityNodes:
        :param wm_title:
        :param extraInformation: A dictionary of extra data for the visualizer.
        It has:
        - wmTitle: The window title. Default to 'Commercial visualizer'.
        - calculationTime: Time that the calculation took. Default to 0.
        - paintCityNodes: Where the visualizer paint city nodes or not. Default to False.
        - densityPolygons: The polygons that define the density grid, if exists.
        - cityBackground: A gif image that will be displayed as background.
        :return:
        '''
        # City definition
        self.city = city
        self.commercial = commercial
        defaultExtraData = { 'wmTitle': 'Commercial visualizer',
                             'calculationTime': 0,
                             'paintCityNodes': False}
        parsedExtraData = ParseParameters.parseParameters(extraData,
                                                          defaultExtraData)
        self.extraData = parsedExtraData
        self.direct = self.city.streetNWAdm.getDirectEdges()
        self.bb = self.city.getStreetsBoundingBox()
        self.minLat=self.bb[0]
        self.minLon=self.bb[1]
        self.maxLat=self.bb[2]
        self.maxLon=self.bb[3]
        self.objectsDrawn = {}
        self.objectsDrawnReverse = {}

        self.paintDensityPolygons = False
        self.densityPolygons = extraData['densityPolygons']
        self.cityBackground = extraData['cityBackground']

        self.zoom = 1
        self.dotSize = MIN_DOT_SIZE
        if ('wmTitle' in self.extraData):
            self.root.wm_title(extraData['wmTitle'])
        else:
            self.root.wm_title('Commercial Visualizer')

        # For now, window size = screen resolution
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()

        if (self.width / (self.maxLon - self.minLon) > self.height / (self.maxLat - self.minLat)):
            self.ratio = ((self.height - SCROLLBARS_MARGIN - WINDOW_TITLE_HEIGHT - DRAW_MARGIN * 2)/ (self.maxLat - self.minLat))
        else:
            self.ratio = ((self.width - SCROLLBARS_MARGIN - WINDOW_TITLE_HEIGHT - DRAW_MARGIN * 2) / (self.maxLon - self.minLon))

        self.canvasWidth = (self.maxLon - self.minLon) * self.ratio + DRAW_MARGIN * 2
        self.canvasHeight = (self.maxLat - self.minLat) * self.ratio + DRAW_MARGIN * 2
        self.canvas = Tkinter.Canvas(self.root,
                                     background = Colors.WHITE,
                                     width = self.canvasWidth,
                                     height = self.canvasHeight,
                                     confine = False)

        self.canvas.config(scrollregion = self.canvas.bbox(Tkinter.ALL))
        self.canvas.grid(row = 0, column = 0)
        # Scrollbars definition
        vscrollbar = Tkinter.Scrollbar(self.root, orient = Tkinter.VERTICAL, command = self.canvas.yview)
        vscrollbar.grid(row = 0, column = 1, sticky = Tkinter.N + Tkinter.S)
        hscrollbar = Tkinter.Scrollbar(self.root, orient = Tkinter.HORIZONTAL, command = self.canvas.xview)
        hscrollbar.grid(row = 1, column = 0, sticky = Tkinter.E + Tkinter.W)

        # Attach canvas to scrollbars
        self.canvas["yscrollcommand"] = vscrollbar.set
        self.canvas["xscrollcommand"] = hscrollbar.set

        # Listen to key presses
        self.root.bind("<Key>", self.keyListener)
        timeBefore = datetime.datetime.now()
        print "Beging paint "
        self.paint()
        timeDiff = datetime.datetime.now() - timeBefore
        print "End paint " + str(timeDiff)


    def paint(self):

        if (self.cityBackground != None and self.showBackground):
            self.backgroundPhotoImage = Tkinter.PhotoImage(file = self.cityBackground)
            self.backgroundPhotoId = self.canvas.create_image(self.canvasWidth / 2, self.canvasHeight / 2, image = self.backgroundPhotoImage)

        # Draw density polygons
        if (self.paintDensityPolygons and self.densityPolygons is not None):
            for polygon in self.densityPolygons:
                for index in range(len(polygon.latLngPolygon)):
                    edge = [polygon.latLngPolygon[index], polygon.latLngPolygon[math.trunc(math.fmod(index + 1, len(polygon.latLngPolygon)))]]
                    # Since X is longitude and Y is latitude and normally the order
                    # coordinates is latitude-longitude, we have to flip the order
                    # of the edge coordinates
                    edge = [[edge[0][1], edge[0][0]], [edge[1][1], edge[1][0]]]
                    self.drawEdgeLatLng(edge, color = Colors.YELLOW)

                for point in polygon.generatedPoints:
                    self.drawDot(point[0], point[1], Colors.AQUA)

                for point in polygon.debugPoints:
                    self.drawDot(point[0][0], point[0][1], Colors.YELLOW)
                    self.drawDot(point[1][0], point[1][1], Colors.MAROON)
                    self.drawEdgeLatLng([[point[0][1], point[0][0]], [point[1][1], point[1][0]] ], "first", Colors.BLACK)

                centerOfPolygon = ToolsExt.centerOfPoints(polygon.latLngPolygon)
                labelPos = []
                labelPos.append(self.lonToX(centerOfPolygon[1]))
                labelPos.append(self.latToY(centerOfPolygon[0]))

                # Draw polygon information
                labelId = self.canvas.create_text(labelPos[0],
                                                  labelPos[1],
                                                  anchor="nw", width = LABEL_AGENTS_WIDTH)

                self.canvas.insert(labelId, LABEL_TEXT_SIZE_BIG,
                                   str(polygon.id))

                # This is a hack since Tkinter canvas create_text doesn't allow
                # background color property
                textBackground = self.canvas.create_rectangle(self.canvas.bbox(labelId),
                                                              fill = Colors.SILVER)
                # Put the background below (in z) the text
                self.canvas.tag_lower(textBackground, labelId)

        # Draw edges
        if self.showStreets:
            for edge in self.direct:
                lineId = self.drawWay(edge)
                self.canvas.tag_bind(lineId, '<ButtonPress-1>', self.clickListener)
                self.objectsDrawn[lineId] = edge

                if (self.extraData['paintCityNodes']):
                    dotId1 = self.drawDot(self.city.getNodeLat(edge[City.NODES][0]),
                                          self.city.getNodeLon(edge[City.NODES][0]),
                                          Colors.GRAY)
                    dotId2 = self.drawDot(self.city.getNodeLat(edge[City.NODES][1]),
                                          self.city.getNodeLon(edge[City.NODES][1]),
                                          Colors.GRAY)
                    self.canvas.tag_bind(dotId1, '<ButtonPress-1>', self.clickListener)
                    self.canvas.tag_bind(dotId2, '<ButtonPress-1>', self.clickListener)
                    self.objectsDrawn[dotId1] = edge[City.NODES][0]
                    self.objectsDrawn[dotId2] = edge[City.NODES][1]

        # Draw agents
        if self.showAgents:
            for agent in self.commercial.agents:
                if (agent.getNearestbuildingData() == None):
                    color = Colors.RED
                else:
                    color = Colors.BLUE
                dotId = self.drawDot(agent.getLatitude(), agent.getLongitude(),
                                     color, size = DOT_SIZE_AGENT)
                self.canvas.tag_bind(dotId, '<ButtonPress-1>', self.clickListener)
                self.objectsDrawn[dotId] = agent
                self.objectsDrawnReverse[agent] = dotId

        # Draw buildings
        for building in self.commercial.buildings:
            dotSize = self.calculateDotSize(building.mass, Building.EXPECTED_MIN_AREA,
                                            Building.EXPECTED_MAX_AREA)
            if (type(building) == Market and self.showMarkets or type(building) == Shop and self.showShops):
                # Paint with another color if market
                color = Colors.OLIVE if type(building) == Market else Colors.FUCHSIA
                # Check if it is in bankruptcy
                color = Colors.BLACK if building.isBankruptcy() else color
                dotId = self.drawDot(building.getLatitude(), building.getLongitude(),
                                     color, dotSize)
                self.canvas.tag_bind(dotId, '<ButtonPress-1>', self.clickListener)
                self.objectsDrawn[dotId] = building
                self.objectsDrawnReverse[building] = dotId

                buildingPos = []
                buildingPos.append(self.lonToX(building.getLongitude()))
                buildingPos.append(self.latToY(building.getLatitude()))

                labelWidth = LABEL_MARKET_WIDTH if type(building) == Market else LABEL_AGENTS_WIDTH
                labelXOffset = LABEL_MARKET_X_OFFSET if type(building) == Market else LABEL_AGENTS_X_OFFSET
                label_id = self.canvas.create_text(buildingPos[0] + labelXOffset,
                                                   buildingPos[1] + LABEL_Y_OFFSET,
                                                   anchor="nw", width = labelWidth)
                text = str(building.getOwner()) if type(building) == Market else str(building.getNumberAgents())
                self.canvas.insert(label_id, LABEL_TEXT_SIZE, text)

                # This is a hack since Tkinter canvas create_text doesn't allow
                # background color property
                textBackground = self.canvas.create_rectangle(self.canvas.bbox(label_id),
                                                              fill = Colors.SILVER)
                # Put the background below (in z) the text
                self.canvas.tag_lower(textBackground, label_id)

        # Label to show calculation time information
        calculation_time_label = self.canvas.create_text(TIME_LABEL_X_OFFSET,
                                                         TIME_LABEL_Y_OFFSET,
                                                         anchor="nw",
                                                         width = TIME_LABEL_WIDTH)
        self.canvas.insert(calculation_time_label, LABEL_TEXT_SIZE,
                           "Calculation time: " + str(self.extraData['calculationTime']))
        # This is a hack since Tkinter canvas create_text doesn't allow
        # background color property
        textBackground = self.canvas.create_rectangle(self.canvas.bbox(calculation_time_label),
                                                      fill = Colors.SILVER)
        # Put the background below (in z) the text
        self.canvas.tag_lower(textBackground, calculation_time_label)


    def calculateDotSize(self, area, expectedMin, expectedMax):
        if (area == None):
            area = 0;

        areaBuildingRatio = area / float(expectedMax)
        dotRange = MAX_DOT_SIZE - MIN_DOT_SIZE
        dotSize = (areaBuildingRatio * dotRange) + MIN_DOT_SIZE

        return math.ceil(dotSize)

    def drawWay(self, edge, arrow_ = None, color = Colors.SILVER):
        nodeALat = float(self.city.getNodeLat(edge[City.NODES][0]))
        nodeALon = float(self.city.getNodeLon(edge[City.NODES][0]))
        nodeBLat = float(self.city.getNodeLat(edge[City.NODES][1]))
        nodeBLon = float(self.city.getNodeLon(edge[City.NODES][1]))

        return self.drawEdgeLatLng([[nodeALon, nodeALat], [nodeBLon, nodeBLat]], arrow_= arrow_, color = color)


    def drawEdge(self, edge, arrow_ = None, color = Colors.SILVER):
        nodeALat = float(self.city.getNodeLat(edge[0]))
        nodeALon = float(self.city.getNodeLon(edge[0]))
        nodeBLat = float(self.city.getNodeLat(edge[1]))
        nodeBLon = float(self.city.getNodeLon(edge[1]))

        return self.drawEdgeLatLng([[nodeALon, nodeALat], [nodeBLon, nodeBLat]], arrow_= arrow_, color = color)


    def drawEdgeLatLng(self, edge, arrow_ = None, color = Colors.SILVER):
        lineId = self.canvas.create_line(self.lonToX(edge[0][0]),
                                         self.latToY(edge[0][1]),
                                         self.lonToX(edge[1][0]),
                                         self.latToY(edge[1][1]),
                                         smooth = True,
                                         width = 2.0,
                                         fill = color)
        if (arrow_ != None):
            self.canvas.itemconfig(lineId, arrow = arrow_)

        return lineId


    def drawDot(self, lat, lon, color, size = None):
        if (size == None):
            size = self.dotSize
        size = size
        dotId = self.canvas.create_oval(self.lonToX(float(lon)) - size,
                                        self.latToY(float(lat)) - size,
                                        self.lonToX(float(lon)) + size,
                                        self.latToY(float(lat)) + size,
                                        fill = color)
        return dotId


    def lonToX(self, pointLon):
        return ( self.ratio * ((float(pointLon) - float(self.minLon))) *
                 self.zoom + DRAW_MARGIN )


    def latToY(self, pointLat):
        return ( self.ratio * ((self.maxLat - self.minLat) - (float(pointLat) - float(self.minLat))) *
                 self.zoom + DRAW_MARGIN )


    def clickListener(self, event):
        # Reset state
        self.clear()
        self.paint()

        widgetId = event.widget.find_closest(event.x, event.y)[0]

        itemClicked = self.objectsDrawn[widgetId]
        if (isinstance(itemClicked, Building.Building)):
            associatedAgents = itemClicked.agents
            self.highlightNodes(associatedAgents)

            # Draw arrows from building to agent
            for agent in associatedAgents:
                self.drawEdge([agent.associatedNode, itemClicked.associatedNode],
                              "first", Colors.GRAY)

        print "##### Showing information of the node #####\n"
        print self.objectsDrawn[widgetId]
        print "###########################################\n"


    def keyListener(self, event):
        if (event.char == '+'):
            self.zoom = self.zoom + 1 if self.zoom < 10 else self.zoom
        elif (event.char == '-'):
            self.zoom = self.zoom - 1 if self.zoom > 1 else self.zoom

        self.clear()
        self.paint()


    def highlightNodes(self, items):
        for item in items:
            if (item in self.objectsDrawnReverse.keys()):
                widgetId = self.objectsDrawnReverse[item]
                self.canvas.itemconfig(widgetId, fill = Colors.ORANGE)


    def toogleDensityPolygons(self):
        self.paintDensityPolygons = not self.paintDensityPolygons
        self.clear()
        self.paint()


    def clear(self):
        self.canvas.delete("all")


    def updateChecks(self, showAgents, showShops, showMarkets, showStreets, showBackground):
        self.showAgents = showAgents
        self.showMarkets = showMarkets
        self.showShops = showShops
        self.showStreets = showStreets
        self.showBackground = showBackground
        if self.canvas != None:
            self.clear()
            self.paint()


if __name__=="__main__":
    pass

