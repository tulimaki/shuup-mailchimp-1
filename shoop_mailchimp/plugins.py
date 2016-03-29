# -*- coding: utf-8 -*-
# This file is part of Shoop.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from shoop.xtheme import TemplatedPlugin
from shoop.xtheme.plugins.forms import TranslatableField
from shoop.xtheme.resources import add_resource


class NewsletterPlugin(TemplatedPlugin):
    identifier = "shoop_mailchimp.newsletter"
    name = _("Subscribe Newsletter")
    template_name = "shoop_mailchimp/newsletter.jinja"

    fields = [
        ("title", TranslatableField(label=_("Title"), required=True, initial="")),
        ("lead", TranslatableField(label=_("Lead text"), required=True, initial="")),
        ("link_title", TranslatableField(label=_("Link title"), required=True, initial="")),
        ("input_placeholder_text", TranslatableField(label=_("Input placeholder text"), required=True, initial="")),
        ("success_message", TranslatableField(label=_("Success message"), required=True, initial="")),
        ("error_message", TranslatableField(label=_("Error message"), required=True, initial="")),
    ]

    def render(self, context):
        """
        Custom render for to add css resource for carousel
        :param context: current context
        :return: html content for the plugin
        """
        add_resource(context, "head_end", "%sshoop_mailchimp/css/style.css" % settings.STATIC_URL)
        add_resource(context, "body_end", "%sshoop_mailchimp/js/script.js" % settings.STATIC_URL)
        return super(NewsletterPlugin, self).render(context)

    def get_context_data(self, context):
        return {
            "title": self.get_translated_value("title"),
            "lead": self.get_translated_value("lead"),
            "link_title": self.get_translated_value("link_title"),
            "input_placeholder_text": self.get_translated_value("input_placeholder_text"),
            "success_message": self.get_translated_value("success_message"),
            "error_message": self.get_translated_value("error_message"),
        }
