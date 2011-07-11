# -*- coding: utf-8 -*-
__author__ = 'Ramon Bartl <ramon.bartl@inquant.de>'
__docformat__ = 'plaintext'


from Products.Archetypes.public import BooleanField, BooleanWidget
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender, \
    IBrowserLayerAwareExtender
from collective.dancefloor import dancefloorMessageFactory as _
from collective.dancefloor.interfaces import IDanceFloor, IDanceFloorParty, \
    ILocalNewsletterLookup, IDanceFloorLayer
from collective.dancefloor.tools import add_tools
from collective.dancefloor.utils import get_name_for_site
from collective.singing.interfaces import IChannelLookup
from five.localsitemanager import make_objectmanager_site
from zope import component, interface
from zope.app.component.interfaces import ISite

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
    """
    """
#    def get(self, instance, **kwargs):
#        return IDanceFloorParty.providedBy(instance)
#
#    def getRaw(self, instance, **kwargs):
#        return IDanceFloorParty.providedBy(instance)
#
#    def set(self, instance, value, **kwargs):
#        if value:
#            addMarkerInterface(instance, IDanceFloorParty)
##            enable_party(instance)
#        else:
##            disable_party(instance)
#            removeMarkerInterface(instance, IDanceFloorParty)


class FolderExtender(object):
    component.adapts(IDanceFloor)
    interface.implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
    layer = IDanceFloorLayer
    
    fields = [
        InterfaceMarkerField("dancefloor_enabled",
            schemata="settings",
            default=False,
            widget = BooleanWidget(
                label=_("Enable local newsletter functionality"))),
            ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

# vim: set ft=python ts=4 sw=4 expandtab :
