# -*- coding: utf-8 -*-
from collective.singing.async import IQueue
try:
    # Plone < 4.3
    from zope.app.component.hooks import getSiteManager
except ImportError:
    # Plone >= 4.3
    from zope.component.hooks import getSiteManager
from Products.Five import BrowserView
from zope import component
from collective.dancefloor import logger
from Products.CMFCore.utils import getToolByName


class ClearDefaultQueueView(BrowserView):
    """
    This view remove default queue that cause conflict problems with local channels
    """

    def __call__(self):
        """
        """
        utility_name = 'collective.dancing.jobs'
        sm = getSiteManager()
        message = ""
        queue = component.queryUtility(IQueue, utility_name)
        if queue:
            if sm.unregisterUtility(provided=IQueue, name=utility_name):
                message = 'Utility removed from portal_newsletters'
                logger.info(message)
            else:
                message = 'Utility not removed from portal_newsletters. Are you in the right place?'
                logger.error(message)
        else:
            message = 'Utility not removed from portal_newsletters. Are you in the right place?'
            logger.error(message)
        pu = getToolByName(self.context, "plone_utils")
        pu.addPortalMessage(message)
        return self.request.response.redirect(self.context.portal_url())
