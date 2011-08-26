from plone.indexer.decorator import indexer
from collective.dancefloor.interfaces import IDanceFloor,IDanceFloorParty

@indexer(IDanceFloorParty)
def dancefloor_enabled(object, **kw):
    dancefloor_enabled_field=object.getField('dancefloor_enabled')
    if dancefloor_enabled_field:
        return dancefloor_enabled_field.get(object)
    return False
            