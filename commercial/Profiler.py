# -*- coding: utf-8 -*-
# Copyright 2014 Carlos Soriano Sánchez <carlos.soriano89@gmail.com>


import cProfile
import pstats


class Profiler:
    '''
    Class to profile a function and save its stats.
    Usage:
    profiler = Profiler.Profiler('commercialGenerator.processSimulationTemplate()')
    profiler.profile()
    profiler.printStats()

    The stats can also be shown with https://code.google.com/p/jrfonseca/wiki/Gprof2Dot
    For example: python gprof2dot.py -f pstats filePath.pstats | dot -Tpng -o output.png
    '''
    def __init__(self, funcName, globals, locals, filePath = None):
        self.funcName = funcName
        if (filePath is None):
            filePath = funcName + '.pstats'
        self.filePath = filePath
        self.locals = locals
        self.globals = globals


    def profile(self):
        cProfile.runctx(self.funcName, self.globals, self.locals, self.filePath)


    def printStats(self, filePath = None):
        p = pstats.Stats(self.filePath)
        if (filePath is None):
            p.strip_dirs().sort_stats('time').print_stats(10)
        else:
            p.strip_dirs().sort_stats('time').dump_stats(filePath)

    def profileAndPrint(self):
        self.profile()
        self.printStats()