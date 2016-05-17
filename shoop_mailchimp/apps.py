# This file is part of Shoop.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from django.db.models.signals import post_save

import shoop.apps
from shoop.core.order_creator.signals import order_creator_finished
from shoop.core.models import CompanyContact, PersonContact
from shoop_mailchimp.configuration_keys import (
    MC_CONTACT_SIGNAL_DISPATCH_UID, MC_ORDER_SIGNAL_DISPATCH_UID
)
from shoop_mailchimp.interface import (
    update_or_create_contact, update_or_create_contact_from_order
)


class AppConfig(shoop.apps.AppConfig):
    name = "shoop_mailchimp"
    provides = {
        "admin_module": ["shoop_mailchimp.admin:MailchimpAdminModule"],
        "admin_shop_form_part": [
            "shoop_mailchimp.admin.forms:ConfigurationFormPart"
        ],
        "xtheme_plugin": ["shoop_mailchimp.plugins:NewsletterPlugin"],
        "front_urls": [
            "shoop_mailchimp.urls:urlpatterns"
        ],
    }

    def ready(self):
        post_save.connect(update_or_create_contact, sender=CompanyContact, dispatch_uid=MC_CONTACT_SIGNAL_DISPATCH_UID)
        post_save.connect(update_or_create_contact, sender=PersonContact, dispatch_uid=MC_CONTACT_SIGNAL_DISPATCH_UID)
        order_creator_finished.connect(update_or_create_contact_from_order, dispatch_uid=MC_ORDER_SIGNAL_DISPATCH_UID)
