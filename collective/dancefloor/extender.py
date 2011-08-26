# -*- coding: utf-8 -*-
from Products.Archetypes.public import BooleanField, BooleanWidget
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender, \
    IBrowserLayerAwareExtender
from collective.dancefloor import dancefloorMessageFactory as _
from collective.dancefloor.interfaces import IDanceFloor, IDanceFloorLayer
from zope import component, interface

class InterfaceMarkerField(ExtensionField, BooleanField):
    """
    """

class DanceFloorExtender(object):
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
    
    def getOrder(self, schematas):
        """ Manipulate the order in which fields appear.
        @param schematas: Dictonary of schemata name -> field lists
        @return: Dictionary of reordered field lists per schemata.
        """

        return schematas
