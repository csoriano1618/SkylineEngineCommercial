# -*- coding: utf-8 -*-
# Copyright 2014 Carlos Soriano Sánchez <carlos.soriano89@gmail.com>


debug = False


def setDebug(debugBool):
    global debug
    debug = debugBool


def isDebug():
    global debug
    return debug