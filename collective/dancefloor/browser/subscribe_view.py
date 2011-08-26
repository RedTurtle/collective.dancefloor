# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from collective.dancefloor import dancefloorMessageFactory as _
from collective.dancefloor.interfaces import IDanceFloor,IDanceFloorParty
from plone.memoize.view import memoize
from Products.CMFCore.utils import getToolByName

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
        local_newsletters=pc(dancefloor_enabled=True)
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
        return channels
    
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
