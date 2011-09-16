# -*- coding: utf-8 -*-

from Products.CMFCore.permissions import setDefaultRoles
from AccessControl import ModuleSecurityInfo

security = ModuleSecurityInfo("collective.dancefloor")

PROJECTNAME = 'collective.dancefloor'

#permission to manage local newsletters
security.declarePublic("DelegateLocalNewsletterManager")
DelegateLocalNewsletterManager = "Sharing page: delegate Local Newsletter Manager role"
setDefaultRoles(DelegateLocalNewsletterManager, ('Manager',))

#permission to manage local newsletters
security.declarePublic("ManageLocalNewsletter")
ManageLocalNewsletter = "collective.dancefloor: Manage Local Newsletters"
setDefaultRoles(ManageLocalNewsletter, ('Manager',))