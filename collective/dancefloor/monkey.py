from zope import component
from collective.dancing import utils
from Products.CMFPlone.interfaces import IPloneSiteRoot
from collective.dancing.composer import template_var
from collective.dancefloor.interfaces import IDanceFloorParty
from collective.dancing import MessageFactory as _

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

def status_already_subscribed(self):
    channel_url=""
    for item in self.context.aq_chain:
        if IDanceFloorParty.providedBy(item):
            channel_url="%s/portal_newsletters" %item.absolute_url()
    if not channel_url:
        channel_url=self.newslettertool.absolute_url()
    link_start = '<a href="%s/sendsecret.html">' % (channel_url)
    link_end = '</a>'
    # The link_start plus link_end construction is not very
    # pretty, but it is needed to avoid syntax errors in the
    # generated po files.
    return _(
        u'You are already subscribed to this newsletter. Click here to '
        '${link_start}edit your subscriptions${link_end}.',
        mapping={'link_start': link_start,
                 'link_end': link_end})