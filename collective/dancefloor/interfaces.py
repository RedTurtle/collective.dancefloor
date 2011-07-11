# -*- coding: utf-8 -*-
__author__ = 'Ramon Bartl <ramon.bartl@inquant.de>'
__docformat__ = 'plaintext'

from zope.interface import Interface

class IDanceFloor(Interface):
    """ we can make parties on this dancefloor
    """
class IDanceFloorParty(Interface):
    """ there is a party on the floor
    """
class IDanceFloorChannels(Interface):
    """ Marker interface for local channels. Used for browser:defaultView registration """

class IDanceFloorCollectors(Interface):
    """ Marker interface for local collectors. Used for browser:defaultView registration """

class ILocalNewsletterLookup(Interface):
    """ a utility which returns local channels """

    def local_channels():
        """ return local channels """

    def local_collectors():
        """ return local collectors """

class IDanceFloorLayer(Interface):
    """a marker interface for browserlayer"""
