# -*- coding: utf-8 -*-
#
# File: extender.py
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


from zope import interface
from zope import component

from zope.app.component.interfaces import ISite

from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender

from Products.Archetypes.public import BooleanField
from Products.Archetypes.public import BooleanWidget

from five.localsitemanager import make_objectmanager_site

from collective.singing.interfaces import IChannelLookup

from collective.dancefloor.interfaces import IDanceFloor
from collective.dancefloor.interfaces import IDanceFloorParty
from collective.dancefloor.interfaces import ILocalNewsletterLookup

from collective.dancefloor.utils import get_name_for_site
from collective.dancefloor.tools import add_tools

from collective.dancefloor import dancefloorMessageFactory as _


def addMarkerInterface(obj, *ifaces):
    """ add a marker interface
    """
    for iface in ifaces:
        if not iface.providedBy(obj):
            interface.alsoProvides(obj, iface)


def removeMarkerInterface(obj, *ifaces):
    """ remove a marker interface
    """
    for iface in ifaces:
        if iface.providedBy(obj):
            interface.noLongerProvides(obj, iface)


def enable_party(context):
    """ Make this container a local site and add all
        the needed tools, if they're not there yet.
    """
    if not ISite.providedBy(context):
        make_objectmanager_site(context)

    sm = context.getSiteManager()
    name = get_name_for_site(context)

    add_tools(context)

    lookup = context.get("newsletter_lookup")

    interface.directlyProvides(lookup, ILocalNewsletterLookup)
    sm.registerUtility(lookup, name=name, provided=ILocalNewsletterLookup)


def disable_party(context):
    if ISite.providedBy(context):
        sm = context.getSiteManager()
        name = get_name_for_site(sm)
        lookup = context.get("newsletter_lookup")
        if lookup is not None:
            sm.unregisterUtility(lookup, name=name, provided=IChannelLookup)


class InterfaceMarkerField(ExtensionField, BooleanField):

    def get(self, instance, **kwargs):
        return IDanceFloorParty.providedBy(instance)

    def getRaw(self, instance, **kwargs):
        return IDanceFloorParty.providedBy(instance)

    def set(self, instance, value, **kwargs):
        if value:
            addMarkerInterface(instance, IDanceFloorParty)
            enable_party(instance)
        else:
            disable_party(instance)
            removeMarkerInterface(instance, IDanceFloorParty)


class FolderExtender(object):
    component.adapts(IDanceFloor)
    interface.implements(ISchemaExtender)

    fields = [
        InterfaceMarkerField("dancefloor_enabled",
            schemata="settings",
            default=False,
            widget = BooleanWidget(
                label=_("Enable local news letter functionality"))),
            ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

# vim: set ft=python ts=4 sw=4 expandtab :
