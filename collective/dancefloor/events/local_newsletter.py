# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from zope.app.component.interfaces import ISite
from five.localsitemanager import make_objectmanager_site
from collective.dancefloor.utils import get_name_for_site
from collective.dancefloor.tools import add_tools
from zope import interface
from collective.dancefloor.interfaces import IDanceFloor
from collective.dancefloor.interfaces import IDanceFloorParty
from collective.dancefloor.interfaces import ILocalNewsletterLookup


def manageLocalNewsletter(obj, event):
    """
    @author: andrea cecchi
    manda una mail all'autore del commento, alla pubblicazione dello stesso
    """
    dancefloor_enabled_field=obj.getField('dancefloor_enabled')
    if dancefloor_enabled_field:
        dancefloor_enabled=dancefloor_enabled_field.get(obj)
        if dancefloor_enabled:
            addMarkerInterface(obj, IDanceFloorParty)
            enable_party(obj)
        else:
            removeMarkerInterface(obj, IDanceFloorParty)
            disable_party(obj)
        obj.reindexObject()

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
        name = get_name_for_site(context)
        lookup = context.get("newsletter_lookup")
        if lookup is not None:
            sm.unregisterUtility(lookup, name=name, provided=ILocalNewsletterLookup)
