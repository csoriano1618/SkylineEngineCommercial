# -*- coding: utf-8 -*-
# Copyright 2014 Carlos Soriano Sánchez <carlos.soriano89@gmail.com>


def parseParameters(parameters, defaultParameters):
    '''
    Given a dictionary of default parameters, parse a custom dictionary of
    parameters, being a subgroup of all default parameters; add the faulting
    parameters with default values to the user custom dictionary of parameters.

    i.e.
    >>> parameters = {'value_1': 2, 'value_3': 5}
    >>> defaultParameters = {'value_1': 1, 'value_2': 2, 'value_3': 3, 'value_4': 4}
    >>> parsedParameters = parseParameters(parameters, defaultParameters)
    >>> sorted(parsedParameters.items(), key = lambda parameter: parameter[0])
    [('value_1', 2), ('value_2', 2), ('value_3', 5), ('value_4', 4)]
    '''
    parsedParameters = {}
    for key in defaultParameters.keys():
        if(key in parameters.keys()):
            parsedParameters[key] = parameters[key]
        else:
            parsedParameters[key] = defaultParameters[key]
    return parsedParameters

def test():
    import doctest
    import ParseParameters
    doctest.testmod(ParseParameters, verbose = True)

if __name__ == "__main__":
    test()