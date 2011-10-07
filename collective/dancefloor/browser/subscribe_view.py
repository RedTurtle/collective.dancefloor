# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from collective.dancefloor import dancefloorMessageFactory as _
from collective.dancefloor.interfaces import IDanceFloor,IDanceFloorParty
from plone.memoize.view import memoize
from Products.CMFCore.utils import getToolByName
import datetime
from zope import component
from collective.dancing.browser.subscribe import SubscriptionAddForm
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from collective.singing.channel import channel_lookup

class SubscribeView(BrowserView):
    """Vista del modulo di richiesta"""
    
    @memoize    
    def getLocalNewsletter(self):
        for elem in self.context.aq_chain:
            if IDanceFloorParty.providedBy(elem):
                return elem
        return None
    
    def getLocalChannels(self):
        local_newsletter=self.getLocalNewsletter()
        if not local_newsletter:
            return []
        return self.getNewsletterChannels(local_newsletter)
    
    def getOtherChannels(self):
        """
        return a list of other channels in the portal, to subscribe
        """
        pc=getToolByName(self.context,'portal_catalog')
        this_newsletter=self.getLocalNewsletter()
        local_newsletters=pc(dancefloor_enabled=True,
                             object_provides=IDanceFloorParty.__identifier__)
        if not local_newsletters:
            return []
        channels=[]
        for newsletter in local_newsletters:
            if not this_newsletter or newsletter.UID != this_newsletter.UID():
                newsletter_channels=self.getNewsletterChannels(newsletter.getObject())
                if newsletter_channels:
                    newsletter_dict={'title':newsletter.Title,
                                     'link':newsletter.getURL(),
                                     'channels':newsletter_channels}
                    channels.append(newsletter_dict)
        
        global_newsletter=self.getGlobalChannels()
        if global_newsletter:
            channels.append(global_newsletter)
        return channels
    
    def getGlobalChannels(self):
        portal_newsletter=getToolByName(self.context,'portal_newsletters')
        global_channels=portal_newsletter.channels
        if not global_channels:
            return {}
        subscribeable_channels=[]
        for channel in global_channels.keys():
            if global_channels[channel].subscribeable:
                subscribeable_channels.append(global_channels[channel])
        if not subscribeable_channels:
            return {}
        return {'title':_("Global Newsletters"),
                'link':portal_newsletter.absolute_url(),
                'channels':subscribeable_channels}
                
                
    def getNewsletterChannels(self,local_newsletter):
        """
        return a list of local channels of a local_newsletter
        """
        lookup=local_newsletter.get("newsletter_lookup",None)
        if not lookup:
            return []
        channels=lookup.local_channels()
        if not channels:
            return []
        subscribeable_channels=[]
        for channel in channels:
            if channel.subscribeable:
                subscribeable_channels.append(channel)
        return subscribeable_channels