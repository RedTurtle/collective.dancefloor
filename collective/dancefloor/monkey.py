from zope import component
from collective.dancing import utils
from Products.CMFPlone.interfaces import IPloneSiteRoot
from collective.dancing.composer import template_var
from collective.dancefloor.interfaces import IDanceFloorParty

def composer_more_vars(self, subscription, items):
        """Less generic variables.
        """
        vars = {}
        channel = subscription.channel
        site = component.getUtility(IPloneSiteRoot)
        site = utils.fix_request(site, 0)
        secret_var = '$%s' % template_var('secret')
        subscription_channel_url=''
        for item in channel.aq_chain:
            if IDanceFloorParty.providedBy(item):
                subscription_channel_url=channel.absolute_url()
        if not subscription_channel_url:
            subscription_channel_url=channel.portal_newsletters.absolute_url()
        vars['confirm_url'] = (
            '%s/confirm-subscription.html?secret=%s' %
            (subscription_channel_url, secret_var))
        vars['unsubscribe_url'] = (
            '%s/unsubscribe.html?secret=%s' %
            (channel.absolute_url(), secret_var))
        vars['my_subscriptions_url'] = (
            '%s/../../my-subscriptions.html?secret=%s' %
            (channel.absolute_url(), secret_var))
        vars['to_addr'] = '$%s' % template_var('to_addr')
        return vars
