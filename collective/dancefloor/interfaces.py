# -*- coding: utf-8 -*-
#
# File: interfaces.py
#
# Copyright (c) InQuant GmbH
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

__author__ = 'Ramon Bartl <ramon.bartl@inquant.de>'
__docformat__ = 'plaintext'

from zope.interface import Interface

class IDanceFloor(Interface):
    """ we can make parties on this dancefloor
    """

class IDanceFloorParty(Interface):
    """ there is a party on the floor
    """

class ILocalNewsletterLookup(Interface):
    """ a utility which returns local channels """

    def local_channels():
        """ return local channels """

    def local_collectors():
        """ return local collectors """

# vim: set ft=python ts=4 sw=4 expandtab :
