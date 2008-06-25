from zope import interface
from zope import component

from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender

from Products.Archetypes.public import BooleanField
from Products.Archetypes.public import BooleanWidget

from collective.dancefloor.interfaces import IDanceFloor
from collective.dancefloor.interfaces import IDanceFloorParty

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


class InterfaceMarkerField(ExtensionField, BooleanField):

    def get(self, instance, **kwargs):
        return IDanceFloorParty.providedBy(instance)

    def getRaw(self, instance, **kwargs):
        return IDanceFloorParty.providedBy(instance)

    def set(self, instance, value, **kwargs):
        if value:
            addMarkerInterface(instance, IDanceFloorParty)
        else:
            removeMarkerInterface(instance, IDanceFloorParty)


class FolderExtender(object):
    component.adapts(IDanceFloor)
    interface.implements(ISchemaExtender)

    fields = [
        InterfaceMarkerField("job_container",
            schemata="settings",
            default=False,
            widget = BooleanWidget(
                label=_("Use as Job Container"))),
            ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

# vim: set ft=python ts=4 sw=4 expandtab :
