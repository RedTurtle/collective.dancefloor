# -*- coding: utf-8 -*-

from zope.interface import implements
from plone.app.workflow.interfaces import ISharingPageRole
from collective.dancefloor import config
from collective.dancefloor import dancefloorMessageFactory as _

class LocalNewsletterManagerRole(object):
    implements(ISharingPageRole)
    
    title = _(u"title_local_newsletter_manager", default="Manage LocalNewsletters")
    required_permission = config.DelegateLocalNewsletterManager
