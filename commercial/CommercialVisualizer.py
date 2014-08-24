# -*- coding: utf-8 -*-
# Copyright 2014 Carlos Soriano Sánchez <carlos.soriano89@gmail.com>

import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import math
import Tkinter
import datetime
import CommercialVisualizerWindow

class CommercialVisualizer():
    '''
    CommercialVisualizer
    ====================
    Class to generate a visualizer for multiple CommercialVisualizerWindows
    It generates and calculates the simulation selected
    '''
    def __init__(self, data):
        '''
        @param data: It's a list of list of needed data for generation. Each item will
        correspond to a button in the visualizer where you can choose which one
        is executed
        data parameters are:
        - commercial: The commercial data of the simulation
        - cityBackground: A gif image that will be displayed as background
        - title: The title for the button and the window
        - callback: The callback ran when clicked on the corresponding button.
        - densityPolygons: The polygons that define the density grid, if exists.
        Normally it will process the simulation. In this manner the simulation
        is not calculated for each city and each model, but just for the city
        and model selected.
        '''
        self.root = Tkinter.Tk()
        self.root.wm_title("Commercial Visualizer")
        self.windows = []
        self.showAgents = Tkinter.IntVar()
        self.showMarkets = Tkinter.IntVar()
        self.showShops = Tkinter.IntVar()
        self.showStreets = Tkinter.IntVar()
        self.showBackground = Tkinter.IntVar()

        self.showAgents.set(0)
        self.showShops.set(1)
        self.showMarkets.set(1)
        self.showBackground.set(1)
        self.showStreets.set(1)

        index = 0
        for dataItem in data:
            # Note the use of i = i. This provides a snapshot of i at the time
            # when each function object is created . If you leave out 'i=i'
            # from this example, then things don't work correctly. Each menu
            # command ends up processing the same value - the final value of the
            # loop variable. http://tkinter.unpythonic.net/wiki/CallbackConfusion
            if (dataItem['densityPolygons'] is not None):
                densityButton = Tkinter.Button(self.root, text = "Show density")
            else:
                densityButton = None
            selfCallback = lambda dataItem = dataItem, densityButton = densityButton : self.onClickedButton(dataItem, densityButton)
            b = Tkinter.Button(self.root, text = dataItem['title'],
                               command = selfCallback)

            if (densityButton is not None):
                b.grid(row = index, sticky = Tkinter.W + Tkinter.E + Tkinter.N + Tkinter.S,  column = 0)
                densityButton.grid(row = index, sticky = Tkinter.W + Tkinter.E + Tkinter.N + Tkinter.S, column = 1)
            else:
                b.grid(row = index, sticky = Tkinter.W + Tkinter.E + Tkinter.N + Tkinter.S, columnspan = 5)
            index += 1

            b = Tkinter.Checkbutton(self.root, text = "Agents", variable = self.showAgents, command = self.updateChecks)
            b.grid(row = index, column = 0, sticky = Tkinter.W + Tkinter.E + Tkinter.N + Tkinter.S, columnspan = 1)

            b = Tkinter.Checkbutton(self.root, text = "Shops", variable = self.showShops, command = self.updateChecks)
            b.grid(row = index, column = 1, sticky = Tkinter.W + Tkinter.E + Tkinter.N + Tkinter.S, columnspan = 1)

            b = Tkinter.Checkbutton(self.root, text = "Markets", variable = self.showMarkets, command = self.updateChecks)
            b.grid(row = index, column = 2, sticky = Tkinter.W + Tkinter.E + Tkinter.N + Tkinter.S, columnspan = 1)

            b = Tkinter.Checkbutton(self.root, text = "Streets", variable = self.showStreets, command = self.updateChecks)
            b.grid(row = index, column = 3, sticky = Tkinter.W + Tkinter.E + Tkinter.N + Tkinter.S, columnspan = 1)

            b = Tkinter.Checkbutton(self.root, text = "Background", variable = self.showBackground, command = self.updateChecks)
            b.grid(row = index, column = 4, sticky = Tkinter.W + Tkinter.E + Tkinter.N + Tkinter.S, columnspan = 1)
        Tkinter.mainloop()


    def updateChecks(self):
        for window in self.windows:
           if window.root.winfo_exists():
               window.updateChecks(self.showAgents.get(), self.showShops.get(), self.showMarkets.get(), self.showStreets.get(), self.showBackground.get())


    def onClickedButton(self, data, densityButton):
        # Calculate simulation
        timeBefore = datetime.datetime.now()
        data['callback']()
        timeDiff = datetime.datetime.now() - timeBefore
        # Show seconds
        timeDiff = str(math.trunc(timeDiff.microseconds / 1000)) + str(" s")

        # Set the city and the commercial visualizer window with calculated data
        cvw = CommercialVisualizerWindow.CommercialVisualizerWindow(self.root)
        self.windows.append(cvw)
        self.updateChecks()

        extraVisualizerData = { 'wmTitle': data['title'],
                                'calculationTime': timeDiff,
                                'densityPolygons': data['densityPolygons'],
                                'cityBackground': data['cityBackground'] }
        if (densityButton is not None):
            densityButton.config(command = lambda cvw = cvw: cvw.toogleDensityPolygons())
        cvw.spawn(data['commercial'].city, data['commercial'], extraData = extraVisualizerData )


if __name__=="__main__":
    from commercial import Commercial

    parent = os.path.join(os.path.dirname(__file__), '..')

    pathFirence = parent + '/../BigOsmFiles/Girona.osm'
    commercialSimFirenze = Commercial
    commercialSimFirenze.processSimulationTemplate(['UrbanDistance'], [pathFirence], 2, 3, 1, )
