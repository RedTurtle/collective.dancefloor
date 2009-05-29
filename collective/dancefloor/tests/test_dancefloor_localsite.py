import unittest

from zope import interface
from zope import component

from zope.app.component import hooks

from zope.app.component.interfaces import ISite
from five.localsitemanager import make_objectmanager_site

from collective.singing.interfaces import IChannelLookup

from Products.ATContentTypes.content.folder import ATFolder

from collective.dancefloor.tests.base import DanceFloorTestCase
from collective.dancefloor.interfaces import *
from collective.dancefloor.utils import *
from collective.dancefloor.channels import LocalNewsletterLookup
from collective.dancefloor.extender import enable_party


class TestLocalSite(DanceFloorTestCase):
    """ Test enable/disable dancefloor
    """

    def afterSetUp(self):
        _ = self.folder.invokeFactory("Folder", "dancefloor")
        self.dancefloor = self.folder.get(_)
        _ = self.dancefloor.invokeFactory("Folder", "subfloor")
        self.subfloor= self.dancefloor.get(_)

    def beforeTearDown(self):
        hooks.clearSite()

    def test_local_site(self):
        dancefloor = ATFolder("dancefloor")
        self.failUnless(not ISite.providedBy(dancefloor))
        make_objectmanager_site(dancefloor)
        self.failUnless(ISite.providedBy(dancefloor))

    def test_enable_party(self):

        dancefloor = self.dancefloor
        self.assertEqual(len(component.getAllUtilitiesRegisteredFor(IChannelLookup)), 2)

        enable_party(dancefloor)

        # setSite() needed in tests due to traversal adapter not called
        hooks.setSite(dancefloor)

        # we still have the same number if IChannelLookup utitities
        self.assertEqual(len(component.getAllUtilitiesRegisteredFor(IChannelLookup)), 2)

        # ... but now we have a ILocalNewsletterLookup named after the site
        # registered
        name = get_name_for_site(dancefloor)
        self.assertEqual(name, "plone.Members.test_user_1_.dancefloor")
        util = component.getUtility(ILocalNewsletterLookup, name=name)
        self.failUnless(isinstance(util, LocalNewsletterLookup))

class TestTwoDancefloors(DanceFloorTestCase):
    """ Test enable/disable dancefloor """

    def afterSetUp(self):
        _ = self.folder.invokeFactory("Folder", "dancefloor")
        self.dancefloor = self.folder.get(_)
        _ = self.dancefloor.invokeFactory("Folder", "subfloor")
        self.subfloor= self.dancefloor.get(_)

    def beforeTearDown(self):
        hooks.clearSite()

    def test_subfloor_gets_own_utility(self):
        enable_party(self.dancefloor)
        enable_party(self.subfloor)

        self.assertEqual(len(component.getAllUtilitiesRegisteredFor(IChannelLookup)), 2)

        hooks.setSite(self.subfloor)

        name = get_name_for_site(self.dancefloor)
        util1 = component.getUtility(ILocalNewsletterLookup, name=name)
        self.failUnless(isinstance(util1, LocalNewsletterLookup))

        name = get_name_for_site(self.subfloor)
        util2 = component.getUtility(ILocalNewsletterLookup, name=name)
        self.failUnless(isinstance(util2, LocalNewsletterLookup))

        self.failUnless(util2 is not util1)

class TestLocalChannels(DanceFloorTestCase):

    def afterSetUp(self):
        _ = self.folder.invokeFactory("Folder", "dancefloor")
        self.dancefloor = self.folder.get(_)
        _ = self.dancefloor.invokeFactory("Folder", "subfloor")
        self.subfloor= self.dancefloor.get(_)
        enable_party(self.dancefloor)
        enable_party(self.subfloor)
        self.add_channel(self.dancefloor, "df_channel1")
        self.add_channel(self.dancefloor, "df_channel2")
        self.add_channel(self.subfloor, "sf_channel1")
        self.add_channel(self.subfloor, "sf_channel2")

        self.add_collector(self.dancefloor, "df_collector1")
        self.add_collector(self.dancefloor, "df_collector2")
        self.add_collector(self.subfloor, "sf_collector1")
        self.add_collector(self.subfloor, "sf_collector2")
        
        from collective.dancing.channel import PortalNewsletters, tool_added
        news = PortalNewsletters("portal_newsletters")
        self.portal["portal_newsletters"] = news
        tool_added(news, None)

    def add_channel(self, floor, name):
        from collective.dancing.channel import Channel
        floor[name] = Channel(name)

    def add_collector(self, floor, name):
        from collective.dancing.collector import Collector
        floor[name] = Collector(name, name)

    def beforeTearDown(self):
        hooks.clearSite()

    def test_subfloor_channels(self):
        # we're on the subfloor
        hooks.setSite(self.subfloor)
        name = get_name_for_site(self.subfloor)
        util = component.getUtility(ILocalNewsletterLookup, name=name)

        channels = sorted([ c.name for c in util.local_channels()])
        self.assertEqual(channels, sorted(self.subfloor.channels.keys()))


    def test_dancefloor_channels(self):
        # we're on the dancefloor
        hooks.setSite(self.dancefloor)
        name = get_name_for_site(self.dancefloor)
        util = component.getUtility(ILocalNewsletterLookup, name=name)

        channels = sorted([ c.name for c in util.local_channels()])
        self.assertEqual(channels, sorted(self.dancefloor.channels.keys()))

    def test_subfloor_collectors(self):
        # we're on the subfloor
        hooks.setSite(self.subfloor)
        name = get_name_for_site(self.subfloor)
        util = component.getUtility(ILocalNewsletterLookup, name=name)

        collectors = sorted([ c.id for c in util.local_collectors()])
        self.assertEqual(collectors, sorted(self.subfloor.collectors.keys()))

    def test_dancefloor_collectors(self):
        # we're on the dancefloor
        hooks.setSite(self.dancefloor)
        name = get_name_for_site(self.dancefloor)
        util = component.getUtility(ILocalNewsletterLookup, name=name)

        collectors = sorted([ c.id for c in util.local_collectors()] )
        self.assertEqual(collectors, sorted(self.subfloor.collectors.keys()))

    #def test_lookup(self):
        #from collective.singing.channel import channel_lookup

        #for floor in self.dancefloor, self.subfloor:
            #hooks.setSite(floor)

            #channels = sorted([ c.name for c in channel_lookup()])
            #self.assertEqual(channels, sorted(floor.channels.keys()))

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestLocalSite))
    suite.addTest(unittest.makeSuite(TestTwoDancefloors))
    suite.addTest(unittest.makeSuite(TestLocalChannels))
    return suite

# vim: set ft=python ts=4 sw=4 expandtab :
