import logging

from zope import interface
from zope import component

from zope.app.component.interfaces import ISite

from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender

from Products.Archetypes.public import BooleanField
from Products.Archetypes.public import BooleanWidget

from Products.Five.browser import BrowserView

from five.localsitemanager import make_objectmanager_site

from collective.singing.interfaces import IChannelLookup

from collective.dancefloor.interfaces import IDanceFloor
from collective.dancefloor.interfaces import IDanceFloorParty
from collective.dancefloor.interfaces import ILocalNewsletterLookup

from collective.dancefloor.utils import get_name_for_site
from collective.dancefloor.tools import add_tools

from collective.dancefloor import dancefloorMessageFactory as _


info = logging.getLogger("collective.dancefloor").info


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
    info("Local utility %s@%s registered" % (lookup, name))


def disable_party(context):
    if ISite.providedBy(context):
        sm = context.getSiteManager()
        name = get_name_for_site(sm)
        lookup = context.get("newsletter_lookup")
        if lookup is not None:
            sm.unregisterUtility(lookup, name=name, provided=IChannelLookup)
            info("Local utility %s@%s unregistered." % (lookup, name))


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


class TestView(BrowserView):

    def __call__(self):
        from collective.singing.interfaces import IChannelLookup
        return component.getAllUtilitiesRegisteredFor(IChannelLookup)


class NewsletterAvailableCondition(BrowserView):
    """ Returns True or False depending on whether the current context is a
    local newsletter aware
    """
    @property
    def _action_condition(self):
        context = self.context
        return IDanceFloorParty.providedBy(context)

    def __call__(self):
        return self._action_condition

# vim: set ft=python ts=4 sw=4 expandtab :
