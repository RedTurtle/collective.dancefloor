# -*- coding: utf-8 -*-
#
# File: channels.py
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
from zope import interface

from zope.app.component.hooks import getSite

from Acquisition import Explicit, aq_inner, aq_parent

from collective.singing.interfaces import IChannelLookup
from collective.dancing.utils import fix_request

from collective.dancefloor.interfaces import ILocalNewsletterLookup

#from collective.dancefloor.utils import get_site
from collective.dancefloor.utils import get_name_for_site

from OFS.SimpleItem import SimpleItem
from logging import getLogger
logger = getLogger('collective.dancefloor')

class ChannelLookupDelegator(object):
    interface.implements(IChannelLookup)

    def __call__(self):
        #site = get_site()
        site = getSite()
        name = get_name_for_site(site)
        lookup_utility=None
        try:
            lookup_utility = component.queryUtility(ILocalNewsletterLookup, name=name)
        except KeyError:
            logger.exception('Error looking up utility: %s ' % name)
        except AttributeError:
            logger.exception('Error looking up utility: %s ' % name)
        if lookup_utility:
            local_lookup_utility=lookup_utility.get('newsletter_lookup',None)
            if local_lookup_utility:
                for channel in local_lookup_utility.local_channels():
                    channel = fix_request(channel, 0)
                    yield channel


class LocalNewsletterLookup(Explicit, SimpleItem):
    interface.implements(ILocalNewsletterLookup)

    def local_channels(self):
        parent = aq_parent(aq_inner(self))
        channels = parent.get("channels")
        if channels is not None:
            return channels.values()
        return []

    def local_collectors(self):
        parent = aq_parent(aq_inner(self))
        collectors = parent.get("collectors")
        if collectors is not None:
            return collectors.values()
        return []

    def __repr__(self):
        return "<LocalNewsletterLookup at %s>" % id(self)

# vim: set ft=python ts=4 sw=4 expandtab :
