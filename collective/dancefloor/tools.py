# -*- coding: utf-8 -*-
#
# File: tools.py
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

__author__ = """Stefan Eletzhofer <stefan.eletzhofer@inquant.de>"""
__docformat__ = 'plaintext'

import logging

from collective.dancing.channel import ChannelContainer
from collective.dancing.collector import CollectorContainer
from collective.dancefloor.channels import LocalNewsletterLookup


info = logging.getLogger("collective.dancefloor").info


def add_tools(container):

    if "channels" not in container.keys():
        info("channels container added.")
        container["channels"] = ChannelContainer("channels")
        channels = container.get("channels")
        del channels['default-channel']

    if "collectors" not in container.keys():
        container["collectors"] = CollectorContainer("collectors")
        info("collector container added.")

    if "newsletter_lookup" not in container.keys():
        container["newsletter_lookup"] = LocalNewsletterLookup("collectors")

# vim: set ft=python ts=4 sw=4 expandtab :
