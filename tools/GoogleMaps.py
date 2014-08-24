# -*- coding: utf-8 -*-
# Copyright 2014 Carlos Soriano Sánchez <carlos.soriano89@gmail.com>

import urllib
from xml.dom import minidom

MAPS_URL = 'https://maps.googleapis.com/maps/api/geocode/xml?'


def latlngForAddress(address):
    '''
    Given a string, query Google Maps to return its latitude and
    longitude.
    If the name is not found it returns None.

    i.e.
    >>> print latlngForAddress("Carrer del carme, Girona, 147")
    [41.9759412, 2.8244718]
    >>> print latlngForAddress("lorem ipsum dolor est")
    None
    '''
    url = MAPS_URL + 'address=' + urllib.quote_plus(address) + '&sensor=false&output=xml'
    print url
    dom = minidom.parse(urllib.urlopen(url))
    geocodeResponse = dom.getElementsByTagName('GeocodeResponse')[0]
    status = geocodeResponse.getElementsByTagName('status')[0].firstChild.data

    if status == 'OK':
        result = geocodeResponse.getElementsByTagName('result')[0]
        geometry = result.getElementsByTagName('geometry')[0]
        location = geometry.getElementsByTagName('location')[0]
        lat = float(location.getElementsByTagName('lat')[0].firstChild.data)
        lng = float(location.getElementsByTagName('lng')[0].firstChild.data)

        return [lat, lng]
    else:
        return None


if __name__ == "__main__":
    import doctest
    import GoogleMaps

    doctest.testmod(GoogleMaps, verbose = True)
