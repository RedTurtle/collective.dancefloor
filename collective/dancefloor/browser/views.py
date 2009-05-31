# -*- coding: utf-8 -*-
#
# File: views.py
#
# Copyright (c) InQuant GmbH
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

__author__ = 'Ramon Bartl <ramon.bartl@inquant.de>'
__docformat__ = 'plaintext'

from zope import component
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.dancing.browser import channel
from collective.dancing.browser import stats
from collective.dancing.browser import collector
from collective.singing.interfaces import IChannelLookup

from collective.dancefloor.interfaces import IDanceFloorParty
from collective.dancefloor import dancefloorMessageFactory as _
from collective.dancefloor.utils import get_site

from plone.z3cform import z2
from plone.z3cform.crud import crud
from plone.z3cform import layout

def back_to_newsletter(self):
    root = get_site()
    return dict(label=_(u"Up to Local Singing & Dancing configuration"),
                url=root.absolute_url() + '/newsletter_administration_view')


class ControlPanelView(BrowserView):
    __call__ = ViewPageTemplateFile('controlpanel.pt')
    contents = ViewPageTemplateFile('controlpanel-links.pt')
    label = _(u"Local Singing & Dancing configuration")

class LocalChannelEditForm(channel.ChannelEditForm):
    def _update_subforms(self):
        self.subforms = []
        util = component.getUtility(IChannelLookup)
        for channel in util():
            subform = crud.EditSubForm(self, self.request)
            subform.content = channel
            subform.content_id = channel.name
            subform.update()
            self.subforms.append(subform)


class LocalManageChannelsForm(channel.ManageChannelsForm):
    editform_factory = LocalChannelEditForm
    def get_items(self):
        util = component.getUtility(IChannelLookup)
        return [x for x in util()]
    

class ChannelAdministrationView(channel.ChannelAdministrationView):
    __call__ = ViewPageTemplateFile('controlpanel.pt')
    label = _(u'Local channel administration')
    back_link = back_to_newsletter

    def contents(self):
        # use LocalManageChannelsForm to show local channels only 
        # A call to 'switch_on' is required before we can render z3c.forms.
        z2.switch_on(self)
        return LocalManageChannelsForm(self.context.channels, self.request)()

class CollectorAdministrationView(collector.CollectorAdministrationView):
    __call__ = ViewPageTemplateFile('controlpanel.pt')
    label = _(u'Local collector administration')
    back_link = back_to_newsletter


class ChannelStatsForm(stats.StatsForm):
    def get_items(self):
        util = component.getUtility(IChannelLookup)
        return [(channel.name, stats.ChannelStatistics(channel)) 
                for channel in util()]

ChannelStatsView = layout.wrap_form(
    ChannelStatsForm,
    index=ViewPageTemplateFile('controlpanel.pt'),
    label = _(u"Local newsletter statistics"),
    back_link = back_to_newsletter)



class NewsletterAvailableCondition(BrowserView):
    """ Returns True or False depending on whether the current context is a
    local newsletter aware
    """

    @property
    def _action_condition(self):
        context = self.context
        return IDanceFloorParty.providedBy(context)

    def __call__(self):
        return self._action_condition

# vim: set ft=python ts=4 sw=4 expandtab :
