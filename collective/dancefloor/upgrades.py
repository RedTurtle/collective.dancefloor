from Products.CMFCore.utils import getToolByName
from collective.dancefloor import logger
from collective.dancefloor.interfaces import IDanceFloor, ILocalNewsletterLookup
from collective.dancefloor.events.local_newsletter import enable_party
from zope.app.component.interfaces import ISite
default_profile = 'profile-collective.dancefloor:default'


def upgrade(upgrade_product, version):
    """ Decorator for updating the QuickInstaller of a upgrade """
    def wrap_func(fn):
        def wrap_func_args(context, *args):
            p = getToolByName(context, 'portal_quickinstaller').get(upgrade_product)
            setattr(p, 'installedversion', version)
            return fn(context, *args)
        return wrap_func_args
    return wrap_func


@upgrade('collective.dancefloor', '1.0.0')
def to_1000(context):
    """
    Replace old named utilites based on path with new based on uid
    """
    logger.info('Upgrading collective.dancefloor to version 1.0.0')
    pc = getToolByName(context, 'portal_catalog', None)
    newsletters = pc(dancefloor_enabled=True, object_provides=IDanceFloor.__identifier__)
    for newsletter in newsletters:
        nl_obj = newsletter.getObject()
        disable_old_parties(nl_obj)
        enable_party(nl_obj)
        logger.info('Updated named utility for: %s' % newsletter.getPath())
    logger.info('Upgrades old named utilities.')


def disable_old_parties(newsletter):
    """
    remove old named utilities based on path
    """
    if ISite.providedBy(newsletter):
        sm = newsletter.getSiteManager()
        name = get_name_for_site_old(newsletter)
        lookup = newsletter.get("newsletter_lookup")
        if lookup is not None:
            sm.unregisterUtility(name=name, provided=ILocalNewsletterLookup)


def get_name_for_site_old(site):
    if not site:
        return ""
    path = site.getPhysicalPath()[1:]
    return ".".join(path)
