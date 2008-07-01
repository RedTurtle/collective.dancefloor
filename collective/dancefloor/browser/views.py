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

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.dancing.browser import channel
from collective.dancing.browser import stats
from collective.dancing.browser import collector

from collective.dancefloor.interfaces import IDanceFloorParty
from collective.dancefloor import dancefloorMessageFactory as _


class ControlPanelView(BrowserView):
    __call__ = ViewPageTemplateFile('controlpanel.pt')
    contents = ViewPageTemplateFile('controlpanel-links.pt')
    label = _(u"Local Singing & Dancing configuration")


class ChannelAdministrationView(channel.ChannelAdministrationView):
    __call__ = ViewPageTemplateFile('controlpanel.pt')
    label = _(u'Local channel administration')


class CollectorAdministrationView(collector.CollectorAdministrationView):
    __call__ = ViewPageTemplateFile('controlpanel.pt')
    label = _(u'Local collector administration')


class ChannelStatsView(stats.StatsView):
    index = ViewPageTemplateFile('controlpanel.pt')


#class RootCollectorEditView(collector.RootCollectorEditView):
    #__call__ = ViewPageTemplateFile('controlpanel.pt')


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
