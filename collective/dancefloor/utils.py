# -*- coding: utf-8 -*-
#
# File: .py
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

__author__    = """Stefan Eletzhofer <stefan.eletzhofer@inquant.de>"""
__docformat__ = 'plaintext'
__revision__  = "$Revision$"
__version__   = '$Revision$'[11:-2]

import logging

from zope import component
from zope import interface

from Products.CMFCore.interfaces import ISiteRoot

from zope.app.component.interfaces import ISite
from zope.app.component.hooks import getSite


info = logging.getLogger("collective.dancefloor").info


def get_context_from_request(request):
    plone = component.getUtility(ISiteRoot)
    path = "/".join(request.physicalPathFromURL(request.getURL()))
    return plone.restrictedTraverse(path)

def get_site():
    """ Find the next Site iff we're not "on" a site already.  """
    site = getSite()
    request = site.REQUEST
    context = get_context_from_request(request)

    if ISite.providedBy(context):
        return context

    return site


def get_name_for_site(site):
    path = site.getPhysicalPath()[1:]
    return ".".join(path)

# vim: set ft=python ts=4 sw=4 expandtab :
