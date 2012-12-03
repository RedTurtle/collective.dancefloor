import zope
from zope import component
from zope import interface
from Products.CMFPlone.interfaces import IPloneSiteRoot

from collective.dancefloor.utils import get_site, get_name_for_site
from collective.dancefloor.interfaces import ILocalNewsletterLookup

# Customized vocabulary for list of collectors which supports local collectors.
def collector_vocabulary(context):
    terms = []
    # get local floor first
    site = get_site()
    # do not process local configuration if the current site is PloneSite
    if not IPloneSiteRoot.providedBy(site):
        utility = component.queryUtility(ILocalNewsletterLookup, name=get_name_for_site(site))
        if utility is not None:
            local_lookup_utility=utility.get('newsletter_lookup',None)
            if local_lookup_utility:
                for collector in local_lookup_utility.local_collectors():
                    terms.append(
                        zope.schema.vocabulary.SimpleTerm(
                            value=collector,
                            token='/'.join(collector.getPhysicalPath()),
                            title=collector.title))
            
    # get global collectors (original vocabulary code)
    root = component.getUtility(IPloneSiteRoot)
    collectors = root['portal_newsletters']['collectors'].objectValues()
    for collector in collectors:
        terms.append(
            zope.schema.vocabulary.SimpleTerm(
                value=collector,
                token='/'.join(collector.getPhysicalPath()),
                title=collector.title))
    return zope.schema.vocabulary.SimpleVocabulary(terms)

interface.alsoProvides(collector_vocabulary,
                       zope.schema.interfaces.IVocabularyFactory)