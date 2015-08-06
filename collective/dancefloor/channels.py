# -*- coding: utf-8 -*-
from Acquisition import Explicit, aq_inner, aq_parent
from collective.dancefloor import logger
from collective.dancefloor.interfaces import ILocalNewsletterLookup
from collective.dancefloor.utils import get_name_for_site
from collective.dancing.utils import fix_request
from collective.singing.interfaces import IChannelLookup
from OFS.SimpleItem import SimpleItem
from zope import component
from zope import interface
try:
    # Plone < 4.3
    from zope.app.component.hooks import getSite
except ImportError:
    # Plone >= 4.3
    from zope.component.hooks import getSite


class ChannelLookupDelegator(object):
    interface.implements(IChannelLookup)

    def __call__(self):
        site = getSite()
        name = get_name_for_site(site)
        lookup_utility = None
        try:
            lookup_utility = component.queryUtility(
                ILocalNewsletterLookup,
                name=name)
        except KeyError:
            logger.exception('Error looking up utility: %s ' % name)
        except AttributeError:
            logger.exception('Error looking up utility: %s ' % name)
        if lookup_utility:
            local_lookup_utility = lookup_utility.get(
                'newsletter_lookup',
                None)
            if local_lookup_utility:
                for channel in local_lookup_utility.local_channels():
                    channel = fix_request(channel, 0)
                    yield channel


class LocalNewsletterLookup(Explicit, SimpleItem):
    interface.implements(ILocalNewsletterLookup)

    def local_channels(self):
        parent = aq_parent(aq_inner(self))
        channels = parent.get("channels")
        if channels is not None:
            return channels.values()
        return []

    def local_collectors(self):
        parent = aq_parent(aq_inner(self))
        collectors = parent.get("collectors")
        if collectors is not None:
            return collectors.values()
        return []

    def __repr__(self):
        return "<LocalNewsletterLookup at %s>" % id(self)
