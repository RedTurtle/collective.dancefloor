import unittest

from zope import interface
from zope import component

from zope.app.component.interfaces import ISite
from five.localsitemanager import make_objectmanager_site

from collective.dancefloor.tests.base import DanceFloorTestCase
from collective.dancefloor.interfaces import *

from collective.dancefloor.handlers import dancefloor_changed

from Products.ATContentTypes.content.folder import ATFolder

class TestLocalSite(DanceFloorTestCase):
    """ Test enable/disable dancefloor
    """

    def afterSetUp(self):
        _ = self.folder.invokeFactory("Folder", "dancefloor")
        self.dancefloor = self.folder.get(_)
        pass

    def test_local_site(self):
        dancefloor = ATFolder("dancefloor")
        self.failUnless(not ISite.providedBy(dancefloor))
        make_objectmanager_site(dancefloor)
        self.failUnless(ISite.providedBy(dancefloor))

    def test_enable_party(self):
        from collective.dancefloor.handlers import LocalNewsletterLookup
        from collective.dancefloor.extender import enable_party
        from collective.singing.interfaces import IChannelLookup

        dancefloor = self.dancefloor
        self.assertEqual(len(component.getAllUtilitiesRegisteredFor(IChannelLookup)), 1)

        # setSite() needed in tests due to traversal adapter not called
        from zope.app.component import hooks
        hooks.setSite(dancefloor)

        enable_party(dancefloor)
        self.assertEqual(len(component.getAllUtilitiesRegisteredFor(IChannelLookup)), 2)

        util = component.getUtility(IChannelLookup)
        self.failUnless(isinstance(util, LocalNewsletterLookup))



def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestLocalSite))
    return suite

# vim: set ft=python ts=4 sw=4 expandtab :
