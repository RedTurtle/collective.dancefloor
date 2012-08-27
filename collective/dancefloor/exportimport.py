# -*- coding: utf-8 -*-
from collective.dancefloor import logger

def import_various(context):
    if context.readDataFile('dancefloor-various.txt') is None:
        return
    
    portal = context.getSite()
    addKeyToCatalog(portal)

def addKeyToCatalog(portal):
    '''
    @summary: takes portal_catalog and adds a key to it
    @param context: context providing portal_catalog 
    '''
    pc = portal.portal_catalog
    
    indexes = pc.indexes()
    for idx in getKeysToAdd():
        if idx[0] in indexes:
            logger.info("Found the '%s' index in the catalog, nothing changed.\n" % idx[0])
        else:
            pc.addIndex(name=idx[0], type=idx[1], extra=idx[2])
            logger.info("Added '%s' (%s) to the catalog.\n" % (idx[0], idx[1]))
 
def getKeysToAdd():
    '''
    @author: andrea cecchi
    @summary: returns a tuple of keys that should be added to portal_catalog
    '''
    return (('dancefloor_enabled','FieldIndex',{'indexed_attrs': 'dancefloor_enabled', }),)
