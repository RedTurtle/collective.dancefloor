# -*- coding: utf-8 -*-
#
# File: utils.py
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

__author__ = """Stefan Eletzhofer <stefan.eletzhofer@inquant.de>"""
__docformat__ = 'plaintext'


from zope import component

from Products.CMFCore.interfaces import ISiteRoot

from zope.app.component.interfaces import ISite
from zope.app.component.hooks import getSite


def get_context_from_request(request):
    plone = component.getUtility(ISiteRoot)
    path = "/".join(request.physicalPathFromURL(request.getURL()))
    return plone.restrictedTraverse(path)


def get_site():
    """ Find the next Site if we're not "on" a site already.  """
    site = context = getSite()
    # rewritten from old seletz's code with try/except-pdb. I hope this is how it should work [naro]
    # ...hm it does not.. do we really need context from request ? 
    # request = getattr(site, 'REQUEST', None)
    # if request is not None:
    #     request = site.REQUEST
    #     context = get_context_from_request(request)

    if ISite.providedBy(context):
        return context

    return site


def get_name_for_site(site):
    path = site.getPhysicalPath()[1:]
    return ".".join(path)
